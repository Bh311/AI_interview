from Services.job_roles import JOB_ROLES

def calculate_match(resume_skills, job_role):
    required = JOB_ROLES.get(job_role.lower(), [])

    if not required:
        return 0, []

    matched = []

    # flatten resume skills
    all_skills = []
    for category in resume_skills.values():
        all_skills.extend(category)

    for skill in required:
        if skill in all_skills:
            matched.append(skill)

    score = int((len(matched) / len(required)) * 100)

    return score, matched