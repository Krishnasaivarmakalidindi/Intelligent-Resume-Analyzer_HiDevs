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
            text += page_text + "\n"

    return text


def extract_email(text):

    pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'

    emails = re.findall(pattern, text)

    if emails:
        return emails[0]

    return "Not Found"


def extract_name(text):

    lines = text.split("\n")

    clean_lines = [
        line.strip()
        for line in lines
        if line.strip()
    ]

    if len(clean_lines) >= 2:
        first_name = clean_lines[0]
        second_name = clean_lines[1]

        if len(first_name.split()) <= 3:
            return first_name + " " + second_name

    return clean_lines[0]


def extract_skills(text):

    found_skills = []

    for skill in SKILLS_DB:

        if skill.lower() in text.lower():

            found_skills.append(skill)

    return list(set(found_skills))


def extract_experience(text):

    years = re.findall(r'20\d{2}', text)

    if len(years) >= 2:

        oldest_year = min(map(int, years))

        current_year = 2025

        return current_year - oldest_year

    return 0