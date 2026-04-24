def predict_selection(resume_score, interview_score):
    # weights
    resume_weight = 0.4
    interview_weight = 0.6

    final_score = int(
        (resume_score * resume_weight) +
        (interview_score * interview_weight)
    )

    # decision logic
    if final_score >= 70:
        decision = "Selected"
        probability = "High"
    elif final_score >= 50:
        decision = "Maybe"
        probability = "Medium"
    else:
        decision = "Rejected"
        probability = "Low"

    return final_score, decision, probability