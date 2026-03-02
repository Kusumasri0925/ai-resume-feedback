import spacy

nlp = spacy.load("en_core_web_sm")

def extract_job_skills(job_description: str):
    return list(set([token.text.lower() for token in nlp(job_description)
                     if not token.is_stop and token.is_alpha]))

def score_resume(parsed_resume: dict, job_description: str):
    resume_skills = [s.lower() for s in parsed_resume.get("skills", [])]
    job_skills = extract_job_skills(job_description)

    matched = list(set(resume_skills) & set(job_skills))
    missing = list(set(job_skills) - set(resume_skills))

    score = (len(matched) / len(job_skills) * 100) if job_skills else 0

    if score > 75:
        feedback = "Strong match for this role."
    elif score > 40:
        feedback = "Moderate match. Consider improving missing skills."
    else:
        feedback = "Low match. Resume needs optimization."

    return {
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "score_percentage": score,
        "feedback": feedback
    }