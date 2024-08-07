import streamlit as st
import os

from skills_extraction import unique_skills, get_skills
from ResumeProcess import extract_text_from_pdf, extract_Identity


# Initialize session_state to store job description
if "job_description" not in st.session_state:
    st.session_state.job_description = None

# Function to upload job description
def upload_job_description():
    st.subheader("Upload Job Description")
    job_description = st.text_area("Job Description")
    submit_button = st.button("Submit Job Description")
    if submit_button:
        st.session_state.job_description = job_description  # Store job description in session state
        st.success("Job Description submitted successfully.")
    return job_description

# Function to upload resumes
def upload_resumes():
    st.subheader("Upload Resumes")
    uploaded_files = st.file_uploader("Upload Resumes", accept_multiple_files=True)
    submit_button = st.button("Submit Resumes")
    if submit_button:
        st.success("Resumes submitted successfully.")
        return uploaded_files
    return None

jd_skills = None 

# Main function
def main():
    st.set_page_config(layout="wide")
    st.title("Resume Processing App")
    st.markdown("""
        <style>
        .main {
            background-color: #1a1a2e;
            padding: 20px;
        }
        h1, h2, h3, label {
            color: #eaeaea;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
        }
        .stTextArea>label, .stFileUploader>label {
            color: #eaeaea;
        }
        .stTextArea textarea, .stFileUploader input {
            background-color: #2e2e3a;
            color: #eaeaea;
        }
        .stTextArea, .stFileUploader {
            margin-top: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Create two columns
    col1, col2 = st.columns(2)

    # Upload job description in the first column
    with col1:
        job_description = upload_job_description()

    jd_skills = None
    if job_description:
        with st.spinner("Extracting skills from job description..."):
            jd_skills = unique_skills(get_skills(job_description))
        
        # Display unique skills in the first column
        with st.expander("📋 Unique Skills in Job Description"):
            st.write("These are the skills extracted from the job description:")
            st.write(", ".join(jd_skills))

    # Upload resumes in the second column
    with col2:
        uploaded_files = upload_resumes()

    ranked_resumes = []
    missing_skills = []
    if uploaded_files:
        for resume_path in uploaded_files:
            resume_text = extract_text_from_pdf(resume_path)
            emails, names = extract_Identity(resume_text)
            resume_skills = unique_skills(get_skills(resume_text.lower()))

            score = 0
            for x in jd_skills:
                if x in resume_skills:
                    score += 1
            req_skills_len = len(jd_skills)
            match = round(score / req_skills_len * 100, 1)
            ranked_resumes.append((names, emails, match))

            for skill in jd_skills:
                if skill not in resume_skills:
                    missing_skills.append(skill)
        
        st.success("Resumes processed successfully! 🎉")

        # Display ranked resumes
        st.header("Your Resumes Match Score")
        for i, (names, emails, match) in enumerate(ranked_resumes):
            st.write(f"Skill Match Score: {match}%")
            st.write("--------------")

        # Display the missing skills
        st.subheader("Missing Skills")
        if missing_skills:
            for skill in missing_skills:
                st.write(skill)
        else:
            st.write("No missing skills. Congratulations!")

if __name__ == "__main__":
    main()
