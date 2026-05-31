def calculate_match_score(candidate_skills, required_skills):

    if not required_skills:
        return 0, [], []

    matched = []

    for skill in required_skills:

        if skill.lower() in [
            s.lower()
            for s in candidate_skills
        ]:
            matched.append(skill)

    missing = list(
        set(required_skills) - set(matched)
    )

    score = int(
        (len(matched) / len(required_skills))
        * 100
    )

    return score, matched, missing


def recommendation(score):

    if score >= 80:
        return "Highly Recommended"

    elif score >= 60:
        return "Recommended"

    return "Not Recommended"


def hiring_insight(score):

    if score >= 80:
        return (
            "Candidate is a strong fit for this role."
        )

    elif score >= 60:
        return (
            "Candidate meets most requirements."
        )

    return (
        "Candidate lacks critical skills."
    )