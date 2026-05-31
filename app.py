import streamlit as st
import json

from parser import (
    extract_text_from_pdf,
    extract_email,
    extract_name,
    extract_skills,
    extract_experience
)

from matcher import (
    calculate_match_score,
    recommendation,
    hiring_insight
)

from report_generator import save_report


st.set_page_config(page_title="Resume Analyzer")

st.title("📄 Intelligent Resume Analyzer")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

job_skills_input = st.text_area(
    "Enter Required Skills (comma separated)"
)

if uploaded_file and st.button("Analyze Resume"):

    text = extract_text_from_pdf(uploaded_file)

    name = extract_name(text)
    email = extract_email(text)
    skills = extract_skills(text)
    experience = extract_experience(text)

    required_skills = [
        skill.strip()
        for skill in job_skills_input.split(",")
        if skill.strip()
    ]

    score, matched, missing = calculate_match_score(
        skills,
        required_skills
    )

    result = recommendation(score) 

    col1, col2, col3 = st.columns(3)

    col1.metric("Match Score", f"{score}%")
    col2.metric("Skills Found", len(skills))
    col3.metric("Missing Skills", len(missing))

    report = {
        "candidate_name": name,
        "email": email,
        "skills": skills,
        "experience_years": experience,
        "match_score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "recommendation": result
    }

    save_report(
        report,
        "reports/report.json"
    )

    st.success("Analysis Complete")

    st.subheader("Candidate Details")

    st.write(f"**Name:** {name}")
    st.write(f"**Email:** {email}")
    st.write(f"**Skills:** {', '.join(skills)}")
    st.write(f"**Experience:** {experience} years")

    st.subheader("Match Analysis")

    st.subheader("ATS Match Score")

    st.progress(score / 100)

    st.metric("Score", f"{score}%")
    
    st.write(f"**Matched Skills:** {matched}")
    st.write(f"**Missing Skills:** {missing}")

    st.success(result)
    st.info(hiring_insight(score)) 
