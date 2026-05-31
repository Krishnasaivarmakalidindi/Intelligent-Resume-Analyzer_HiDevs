import streamlit as st
import json
import matplotlib.pyplot as plt

from ai_analyzer import ai_resume_analysis

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


# Page Configuration
st.set_page_config(
    page_title="Intelligent Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# Sidebar
st.sidebar.title("📄 Resume Analyzer")
st.sidebar.info(
    """
    AI-Powered Resume Screening System

    Features:
    - Resume Parsing
    - ATS Score
    - Skill Matching
    - AI Analysis
    - Hiring Recommendation
    - Interview Questions
    - JSON Report Export
    """
)

# Main Title
st.title("📄 Intelligent Resume Analyzer")

st.write(
    "Upload a resume and compare it against job requirements."
)

# Resume Upload
uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

# Job Skills Input
job_skills_input = st.text_area(
    "Enter Required Skills (comma separated)",
    placeholder="Python, SQL, Machine Learning, Git, Pandas"
)

# Analyze Button
if uploaded_file and st.button("Analyze Resume"):

    try:

        # Extract Resume Text
        text = extract_text_from_pdf(uploaded_file)

        if not text.strip():
            st.error(
                "Unable to extract text from resume."
            )
            st.stop()

        # Extract Details
        name = extract_name(text)
        email = extract_email(text)
        skills = extract_skills(text)
        experience = extract_experience(text)

        # Process Skills
        required_skills = [
            skill.strip()
            for skill in job_skills_input.split(",")
            if skill.strip()
        ]

        if not required_skills:
            st.error(
                "Please enter required skills."
            )
            st.stop()

        # Match Analysis
        score, matched, missing = calculate_match_score(
            skills,
            required_skills
        )

        result = recommendation(score)

        # Dashboard
        st.subheader("📊 Dashboard")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Match Score",
            f"{score}%"
        )

        col2.metric(
            "Skills Found",
            len(skills)
        )

        col3.metric(
            "Missing Skills",
            len(missing)
        )

        # Report Object
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

        # Save Report
        save_report(
            report,
            "reports/report.json"
        )

        # Download Button
        json_report = json.dumps(
            report,
            indent=4
        )

        st.download_button(
            label="📥 Download JSON Report",
            data=json_report,
            file_name="resume_report.json",
            mime="application/json"
        )

        st.success(
            "Analysis Complete"
        )

        # Candidate Details
        st.subheader(
            "👤 Candidate Details"
        )

        st.write(
            f"**Name:** {name}"
        )

        st.write(
            f"**Email:** {email}"
        )

        st.write(
            f"**Skills:** {', '.join(skills)}"
        )

        st.write(
            f"**Experience:** {experience} years"
        )

        # ATS Score
        st.subheader(
            "🎯 ATS Match Score"
        )

        st.progress(
            score / 100
        )

        st.metric(
            "ATS Score",
            f"{score}%"
        )

        # Match Analysis
        st.subheader(
            "📋 Match Analysis"
        )

        st.write(
            f"**Matched Skills:** {matched}"
        )

        st.write(
            f"**Missing Skills:** {missing}"
        )

        # Recommendation
        st.subheader(
            "🏆 Recommendation"
        )

        st.success(
            result
        )

        st.info(
            hiring_insight(score)
        )

        # Resume Strengths
        st.subheader(
            "💪 Resume Strengths"
        )

        strengths = []

        if "Python" in skills:
            strengths.append(
                "Strong Python Programming"
            )

        if "SQL" in skills:
            strengths.append(
                "Database Knowledge"
            )

        if "Git" in skills:
            strengths.append(
                "Version Control Experience"
            )

        if "Data Analysis" in skills:
            strengths.append(
                "Data Analytics Skills"
            )

        if strengths:

            for item in strengths:
                st.success(
                    f"✓ {item}"
                )

        else:

            st.warning(
                "No major strengths detected."
            )

        # Skill Gap Analysis
        st.subheader(
            "⚠️ Skill Gap Analysis"
        )

        if missing:

            for skill in missing:

                st.warning(
                    f"✗ {skill}"
                )

        else:

            st.success(
                "No Skill Gaps Found"
            )

        # Pie Chart
        st.subheader(
            "📈 Skill Match Visualization"
        )

        fig, ax = plt.subplots()

        ax.pie(
            [
                len(matched),
                len(missing)
            ],
            labels=[
                "Matched Skills",
                "Missing Skills"
            ],
            autopct="%1.1f%%"
        )

        st.pyplot(fig)

        # AI Analysis
        st.subheader(
            "🤖 AI Recruiter Analysis"
        )

        try:

            with st.spinner(
                "Generating AI Analysis..."
            ):

                ai_report = ai_resume_analysis(
                    text,
                    job_skills_input
                )

            st.markdown(
                ai_report
            )

        except Exception as e:

            st.error(
                f"AI Analysis Error: {str(e)}"
            )

    except Exception as e:

        st.error(
            f"Application Error: {str(e)}"
        ) 
