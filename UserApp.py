import gradio as gr
import fitz  # PyMuPDF
from skills_extraction import unique_skills, get_skills
from ResumeProcess import extract_Identity

# Function to process job description
def process_job_description(job_description):
    jd_skills = unique_skills(get_skills(job_description))
    return ", ".join(jd_skills)

# Function to extract text from PDF using PyMuPDF
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to process resumes and rank them
def process_resumes(job_description, uploaded_files):
    jd_skills = unique_skills(get_skills(job_description))
    ranked_resumes = []
    missing_skills_list = []

    for uploaded_file in uploaded_files:
        # Extract text from the PDF file
        resume_text = extract_text_from_pdf(uploaded_file.name)
        
        emails, names = extract_Identity(resume_text)
        resume_skills = unique_skills(get_skills(resume_text.lower()))

        score = 0
        for x in jd_skills:
            if x in resume_skills:
                score += 1
        req_skills_len = len(jd_skills)
        match = round(score / req_skills_len * 100, 1)
        ranked_resumes.append((names, emails, match))

        missing_skills = [skill for skill in jd_skills if skill not in resume_skills]
        missing_skills_list.append(missing_skills)
    
    return display_results(ranked_resumes), display_missing_skills(missing_skills_list)

def display_results(results):
    result_display = []
    for i, (names, emails, match) in enumerate(results):
        result_display.append(f"**Resume {i+1}:**\n**Names:** {names}\n**Emails:** {emails}\n**Skill Match Score:** {match}%")
    return "\n\n".join(result_display)

def display_missing_skills(missing_skills_list):
    missing_skills_display = []
    for i, missing_skills in enumerate(missing_skills_list):
        if missing_skills:
            missing_skills_display.append(f"**Resume {i+1} Missing Skills:**\n" + ", ".join(missing_skills))
        else:
            missing_skills_display.append(f"**Resume {i+1}:** No missing skills. Congratulations!")
    return "\n\n".join(missing_skills_display)

# Interface for job description input
job_desc_interface = gr.Interface(
    fn=process_job_description,
    inputs=gr.Textbox(lines=10, placeholder="Enter the job description here..."),
    outputs=gr.Textbox(label="Unique Skills in Job Description")
)

# Interface for resume upload and ranking
resume_interface = gr.Interface(
    fn=process_resumes,
    inputs=[gr.Textbox(lines=10, placeholder="Enter the job description here..."), gr.File(file_count="multiple", type="filepath")],
    outputs=[gr.Textbox(label="Ranked Resumes"), gr.Textbox(label="Missing Skills")]
)

# Combine the interfaces
demo = gr.TabbedInterface(
    [job_desc_interface, resume_interface],
    ["Job Description", "Resumes"]
)

if __name__ == "__main__":
    demo.launch()
