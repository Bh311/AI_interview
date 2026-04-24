import random
from Services.questions import QUESTION_BANK
from Services.ai_services import ai_generate_questions

def generate_questions(skills, num_per_skill=2, use_ai=False):
    all_skills = []

    # flatten skills
    for category in skills.values():
        all_skills.extend(category)

    final_questions = []

    # ✅ Rule-based questions (your current system)
    for skill in all_skills:
        if skill in QUESTION_BANK:
            questions = QUESTION_BANK[skill]

            random.shuffle(questions)
            selected = questions[:num_per_skill]

            final_questions.extend(selected)

    # 🔥 remove duplicates
    final_questions = list(set(final_questions))

    # 🔥 limit total questions
    final_questions = final_questions[:6]

    # 🤖 OPTIONAL AI enhancement
    if use_ai:
        try:
            ai_questions = ai_generate_questions(all_skills)
            final_questions.extend(ai_questions)
        except:
            pass  # fallback safe

    return final_questions