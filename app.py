from fastapi import FastAPI, File, UploadFile, Form
import shutil
import os

from parser import extract_resume_data
from scorer import score_resume

app = FastAPI()

UPLOAD_FOLDER = "resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def home():
    return {"message": "AI Resume Feedback System Running"}

@app.post("/analyze")
async def analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    file_path = os.path.join(UPLOAD_FOLDER, resume.filename)

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    parsed_data = extract_resume_data(file_path)
    score = score_resume(parsed_data, job_description)

    return {
        "parsed_resume": parsed_data,
        "score": score
    }