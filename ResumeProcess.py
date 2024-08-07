import PyPDF2
import spacy
import re
import pandas as pd
import numpy as np
import tempfile
import os

from skills_extraction import unique_skills
from skills_extraction import get_skills




# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    text = ""
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as file:
            file.write(uploaded_file.read())
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
    return text

# Extract emails and names 
def extract_Identity(text):
    # Extract emails using regular expression
    emails = re.findall(r'\S+@\S+', text)
    # Extract names using a simple pattern (assuming "First Last" format)
    names = re.findall(r'^([A-Z][a-z]+)\s+([A-Z][a-z]+)', text)
    if names:
        names = [" ".join(names[0])]

    return emails, names



