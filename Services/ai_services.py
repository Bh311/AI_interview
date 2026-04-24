import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()   # 🔥 THIS LINE IS MISSING

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ai_generate_questions(skills):
    prompt = f"""
    Generate 5 technical interview questions based on these skills:
    {skills}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.choices[0].message.content
    return text.split("\n")


# 🔥 ADD THIS FUNCTION
def ai_evaluate(questions, answers):
    prompt = f"""
    Evaluate the following interview answers.

    Questions: {questions}
    Answers: {answers}

    Give:
    - Score out of 100
    - Short feedback
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content