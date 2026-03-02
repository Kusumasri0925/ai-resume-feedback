import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/analyze"

st.title("📄 AI Resume Feedback System")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description")

if st.button("Analyze Resume"):

    if uploaded_file and job_description:
        files = {
            "resume": (uploaded_file.name, uploaded_file, "application/pdf")
        }

        data = {
            "job_description": job_description
        }

        response = requests.post(API_URL, files=files, data=data)

        if response.status_code == 200:
            result = response.json()

            parsed = result["parsed_resume"]
            score = result["score"]

            st.subheader("Candidate Info")
            st.write(parsed)

            st.subheader("Matched Skills")
            st.success(score["matched_skills"])

            st.subheader("Missing Skills")
            st.error(score["missing_skills"])

            st.subheader("Score")
            st.progress(int(score["score_percentage"]))
            st.write(f'{score["score_percentage"]:.2f}%')

            st.info(score["feedback"])
        else:
            st.error("Backend error.")
    else:
        st.warning("Upload resume and enter job description.")