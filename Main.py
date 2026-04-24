from flask import Flask, request, jsonify

import PyPDF2
from Services.resume_parser import extract_skills
from Services.match_parser import calculate_match
from Services.interview import generate_questions
from Services.evaluator import evaluate_answers
from Services.predictor import predict_selection
    
import os



from flask_cors import CORS

CORS(app, resources={
    r"/*": {
        "origins": [
            "https://ai-interview-sage-iota.vercel.app"
        ]
    }
})

from Services.evaluator import evaluate_answers
from Services.ai_services import ai_evaluate   # 🔥 import AI



@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json

    questions = data.get("questions")
    answers = data.get("answers")

    score, result = evaluate_answers(questions, answers)

    return jsonify({
        "score": score,
        "result": result
    })
# @app.route('/evaluate', methods=['POST'])
# def evaluate():
#     data = request.json

#     questions = data.get("questions")
#     answers = data.get("answers")

#     if not questions or not answers:
#         return jsonify({"error": "Missing data"}), 400

#     # ✅ Rule-based evaluation
#     score, details = evaluate_answers(questions, answers)

#     # 🤖 OPTIONAL AI evaluation
#     try:
#         ai_feedback = ai_evaluate(questions, answers)
#     except:
#         ai_feedback = "AI evaluation not available"

#     return jsonify({
#         "score": score,
#         "details": details,
#         "ai_feedback": ai_feedback   # 🔥 NEW
#     })

@app.route('/match', methods=['POST'])
def match_role():
    data = request.json

    resume_skills = data.get("skills")
    role = data.get("role")

    score, matched = calculate_match(resume_skills, role)

    return jsonify({
        "role": role,
        "match_score": score,
        "matched_skills": matched
    })

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    resume_score = data.get("resume_score")
    interview_score = data.get("interview_score")

    if resume_score is None or interview_score is None:
        return jsonify({"error": "Missing scores"}), 400

    final_score, decision, probability = predict_selection(
        resume_score,
        interview_score
    )

    return jsonify({
        "final_score": final_score,
        "decision": decision,
        "probability": probability
    })

# @app.route('/evaluate', methods=['POST'])
# def evaluate():
#     data = request.json

#     questions = data.get("questions")
#     answers = data.get("answers")

#     if not questions or not answers:
#         return jsonify({"error": "Missing data"}), 400

#     score, details = evaluate_answers(questions, answers)

#     return jsonify({
#         "score": score,
#         "details": details
#     })

@app.route('/questions', methods=['POST'])
def get_questions():
    data = request.json

    skills = data.get("skills")

    questions = generate_questions(skills)

    return jsonify({
        "questions": questions
    })

@app.route('/upload', methods=['POST'])
def upload_resume():
    file = request.files.get('resume')

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    text = ""

    # ✅ Handle PDF properly
    if file.filename.endswith('.pdf'):
        pdf = PyPDF2.PdfReader(file)
        for page in pdf.pages:
            text += page.extract_text()

    # ✅ Handle TXT
    else:
        text = file.read().decode('utf-8', errors='ignore')

    skills = extract_skills(text)

    return jsonify({
        "skills": skills,
        "preview": text[:200]
    })
@app.route('/')
def home():
    return "AI Interview Backend is Running 🚀"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))   # 🔥 IMPORTANT
    app.run(host="0.0.0.0", port=port)