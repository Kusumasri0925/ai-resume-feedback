import pdfplumber
import re
import spacy

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Predefined skill list
SKILLS_DB = [
    "python", "java", "sql", "aws", "docker", "react",
    "machine learning", "data science", "flask", "fastapi",
    "mongodb", "tensorflow", "pandas", "numpy"
]

def extract_resume_data(file_path: str) -> dict:
    text = ""

    # Extract text from PDF
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except Exception:
        return {}

    doc = nlp(text)

    # Extract name (first PERSON entity)
    name = None
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break

    # Extract email
    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    email = email_match.group(0) if email_match else None

    # Extract skills
    text_lower = text.lower()
    skills = [skill for skill in SKILLS_DB if skill in text_lower]

    return {
        "name": name,
        "email": email,
        "skills": skills
    }