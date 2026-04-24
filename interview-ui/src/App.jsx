import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import Camera from "./Camera";

function App() {
  const [file, setFile] = useState(null);
  const [skills, setSkills] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [result, setResult] = useState(null);
  const [timeLeft, setTimeLeft] = useState(30);
  const [shouldSubmit, setShouldSubmit] = useState(false);

  const recognitionRef = useRef(null);
  const timerRef = useRef(null);
  const currentIndexRef = useRef(0);
  const finalTranscriptRef = useRef("");

  // keep ref updated
  useEffect(() => {
    currentIndexRef.current = currentIndex;
  }, [currentIndex]);

  // 🔊 Speak
  const speakQuestion = (text) => {
    window.speechSynthesis.cancel();
    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-US";
    window.speechSynthesis.speak(speech);
  };

  // 🎤 Voice
  const startListening = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) return alert("Use Chrome");

    if (recognitionRef.current) recognitionRef.current.stop();

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = true;
    recognition.continuous = true;

    recognitionRef.current = recognition;
    finalTranscriptRef.current = answers[currentIndex] || "";

    recognition.start();

    recognition.onresult = (event) => {
      let interim = "";

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const text = event.results[i][0].transcript;

        if (event.results[i].isFinal) {
          finalTranscriptRef.current += text + " ";
        } else {
          interim += text;
        }
      }

      const newAns = [...answers];
      newAns[currentIndex] = finalTranscriptRef.current + interim;
      setAnswers(newAns);
    };
  };

  const stopListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      recognitionRef.current = null;
    }
  };

  // ⏱ TIMER
  const startTimer = () => {
    clearInterval(timerRef.current);
    setTimeLeft(30);

    timerRef.current = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timerRef.current);

          const index = currentIndexRef.current;
          const isLast = index === questions.length - 1;

          if (isLast) {
            setShouldSubmit(true);   // 🔥 safe submit trigger
          } else {
            setCurrentIndex(index + 1);
          }

          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  };

  // 🔁 Question flow
  useEffect(() => {
    if (questions.length === 0 || result) return;

    const q = questions[currentIndex];

    const t = setTimeout(() => {
      speakQuestion(q);
      startListening();
      startTimer();
    }, 800);

    return () => {
      clearTimeout(t);
      stopListening();
      clearInterval(timerRef.current);
    };
  }, [currentIndex, questions]);

  // 🔥 FINAL SUBMIT HANDLER
  useEffect(() => {
    if (shouldSubmit) {
      submitAnswers();
      setShouldSubmit(false);
    }
  }, [shouldSubmit]);

  // ➡️ Button click
  const handleNext = () => {
    stopListening();
    clearInterval(timerRef.current);

    const index = currentIndexRef.current;
    const isLast = index === questions.length - 1;

    if (isLast) {
      setShouldSubmit(true);
    } else {
      setCurrentIndex(index + 1);
    }
  };

  // Upload
const uploadResume = async () => {
  const formData = new FormData();
  formData.append("resume", file);

  const res = await axios.post(
    "https://aiinterview-production-902c.up.railway.app/upload",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  setSkills(res.data.skills);
};

  // Get Questions
  const getQuestions = async () => {
    const res = await axios.post("https://aiinterview-production-902c.up.railway.app/questions", { skills });

    setQuestions(res.data.questions);
    setAnswers(Array(res.data.questions.length).fill(""));
    setCurrentIndex(0);
  };

  // Submit
  const submitAnswers = async () => {
    console.log("✅ FINAL SUBMIT");

    const res = await axios.post("https://aiinterview-production-902c.up.railway.app/evaluate", {
      questions,
      answers,
    });

    setResult(res.data);
    setQuestions([]);
  };

  const handleAnswerChange = (value) => {
    const newAns = [...answers];
    newAns[currentIndex] = value;
    setAnswers(newAns);
    finalTranscriptRef.current = value;
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6 flex justify-center">
      <div className="w-full max-w-5xl bg-white p-6 rounded shadow">

        <h1 className="text-3xl text-center text-blue-600 mb-6">
          AI Interview Assistant
        </h1>

        {/* RESULT */}
        {result && (
          <div className="text-center">
            <h2 className="text-2xl text-green-600 font-bold">
              Final Score: {result.score}
            </h2>

            <button
              onClick={() => window.location.reload()}
              className="mt-4 bg-gray-500 text-white px-4 py-2 rounded"
            >
              Restart
            </button>
          </div>
        )}

        {/* INTERVIEW */}
        {!result && questions.length > 0 && (
          <div className="flex gap-6">

            <div className="w-1/3">
              <Camera />
            </div>

            <div className="w-2/3">
              <h3>
                Question {currentIndex + 1} / {answers.length}
              </h3>

              <p className="mt-2">{questions[currentIndex]}</p>

              <p className="text-red-500 mt-2">
                Time Left: {timeLeft}s
              </p>

              <textarea
                value={answers[currentIndex] || ""}
                onChange={(e) => handleAnswerChange(e.target.value)}
                className="w-full mt-3 p-2 border rounded"
                rows="4"
              />

              <button
                onClick={handleNext}
                className="mt-3 bg-purple-500 text-white px-4 py-2 rounded"
              >
                {currentIndex === questions.length - 1 ? "Submit" : "Next"}
              </button>
            </div>
          </div>
        )}

        {/* SKILLS */}
        {!result && questions.length === 0 && skills && (
          <div>
            <h3>Extracted Skills:</h3>

            <div className="flex flex-wrap gap-2">
              {Object.values(skills).flat().map((skill, i) => (
                <span key={i} className="bg-blue-100 px-2 py-1 rounded">
                  {skill}
                </span>
              ))}
            </div>

            <button
              onClick={getQuestions}
              className="mt-4 bg-green-500 text-white px-4 py-2 rounded"
            >
              Start Interview
            </button>
          </div>
        )}

        {/* UPLOAD */}
        {!result && !skills && (
          <div className="text-center">
            <input type="file" onChange={(e) => setFile(e.target.files[0])} />
            <br /><br />
            <button
              onClick={uploadResume}
              className="bg-blue-500 text-white px-4 py-2 rounded"
            >
              Upload Resume
            </button>
          </div>
        )}

      </div>
    </div>
  );
}

export default App;