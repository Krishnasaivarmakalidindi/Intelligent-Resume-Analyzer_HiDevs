import re
from PyPDF2 import PdfReader


SKILLS_DB = [
    "Python","Java","C++","SQL",
    "Machine Learning","Deep Learning",
    "Data Analysis","Data Cleaning","EDA",
    "Pandas","NumPy","Scikit-learn",
    "TensorFlow","PyTorch",
    "Git","GitHub",
    "HTML","CSS","JavaScript",
    "React","Flutter",
    "MongoDB","MySQL","PostgreSQL",
    "Firebase","Supabase",
    "REST API",
    "Prompt Engineering",
    "LLM",
    "OpenAI",
    "AI",
    "ML"
]


def extract_text_from_pdf(pdf_file):
    text = ""

    reader = PdfReader(pdf_file)

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text


def extract_email(text):

    pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'

    emails = re.findall(pattern, text)

    if emails:
        return emails[0]

    return "Not Found"
   
    


def extract_name(text):
    lines = text.split("\n")

    for line in lines[:5]:
        if len(line.split()) <= 4:
            return line.strip()

    return "Unknown"


def extract_skills(text):
    found_skills = []

    for skill in SKILLS_DB:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    return found_skills


def extract_experience(text):
    pattern = r'(\d+)\+?\s*years'

    match = re.search(pattern, text.lower())

    if match:
        return int(match.group(1))

    return 0