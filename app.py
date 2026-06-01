import os
import json
import streamlit as st
import plotly.graph_objects as go

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


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="ResumeIQ — AI Resume Analyzer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# DESIGN TOKENS
# =========================================================
T = {
    "bg": "#0a0f1a",
    "surface": "rgba(255,255,255,0.04)",
    "surface_hover": "rgba(255,255,255,0.07)",
    "border": "rgba(255,255,255,0.08)",
    "text": "#f0f2f5",
    "text_secondary": "#8b95a5",
    "accent": "#6c5ce7",
    "accent_light": "#a29bfe",
    "success": "#00cec9",
    "warning": "#fdcb6e",
    "danger": "#ff6b6b",
    "gradient": "linear-gradient(135deg, #6c5ce7, #a29bfe)",
}


# =========================================================
# GLOBAL CSS
# =========================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* ---- Reset & Base ---- */
    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    .stApp {{
        background: {T["bg"]};
        color: {T["text"]};
    }}

    /* Hide default sidebar & header */
    section[data-testid="stSidebar"] {{ display: none; }}
    header[data-testid="stHeader"] {{ background: transparent; }}

    .block-container {{
        padding: 2rem 3rem 3rem 3rem;
        max-width: 1100px;
    }}

    /* ---- Container borders → glass panels ---- */
    div[data-testid="stVerticalBlockBorder"] {{
        background: {T["surface"]} !important;
        border: 1px solid {T["border"]} !important;
        border-radius: 16px !important;
        padding: 24px !important;
        backdrop-filter: blur(20px) !important;
        transition: all 0.3s ease !important;
    }}

    div[data-testid="stVerticalBlockBorder"]:hover {{
        background: {T["surface_hover"]} !important;
        border-color: rgba(255,255,255,0.12) !important;
    }}

    /* ---- Equal-height input cards ---- */
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] > div > div > div[data-testid="stVerticalBlockBorder"] {{
        min-height: 280px;
    }}

    div[data-testid="stFileUploader"] {{
        min-height: 80px;
    }}

    /* ---- Nav / brand bar ---- */
    .nav-bar {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 0 2rem 0;
    }}

    .brand {{
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.25rem;
        font-weight: 800;
        letter-spacing: -0.3px;
    }}

    .brand-icon {{
        width: 32px;
        height: 32px;
        border-radius: 10px;
        background: {T["gradient"]};
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.95rem;
    }}

    .nav-links {{
        display: flex;
        gap: 28px;
        font-size: 0.88rem;
        color: {T["text_secondary"]};
        font-weight: 500;
    }}

    .nav-links span {{
        cursor: default;
        transition: color 0.2s;
    }}

    .nav-links span:hover {{
        color: {T["text"]};
    }}

    /* ---- Hero ---- */
    .hero {{
        text-align: center;
        padding: 1rem 0 2.5rem 0;
        animation: fadeUp 0.6s ease;
    }}

    .hero-badge {{
        display: inline-block;
        padding: 6px 16px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        background: rgba(108,92,231,0.15);
        color: {T["accent_light"]};
        border: 1px solid rgba(108,92,231,0.25);
        margin-bottom: 20px;
    }}

    .hero h1 {{
        font-size: 2.8rem;
        font-weight: 900;
        letter-spacing: -1.2px;
        line-height: 1.1;
        margin: 0 0 16px 0;
        background: linear-gradient(135deg, {T["text"]} 0%, {T["text_secondary"]} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    .hero p {{
        font-size: 1.08rem;
        color: {T["text_secondary"]};
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.7;
        font-weight: 400;
    }}

    /* ---- Section titles ---- */
    .section-label {{
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: {T["accent_light"]};
        margin-bottom: 6px;
    }}

    .section-heading {{
        font-size: 1.05rem;
        font-weight: 700;
        color: {T["text"]};
        margin-bottom: 4px;
    }}

    .section-sub {{
        font-size: 0.85rem;
        color: {T["text_secondary"]};
        margin-bottom: 16px;
        line-height: 1.5;
    }}

    /* ---- Metric cards ---- */
    .metric-row {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 1.5rem;
    }}

    .m-card {{
        background: {T["surface"]};
        border: 1px solid {T["border"]};
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
    }}

    .m-card:hover {{
        transform: translateY(-3px);
        border-color: rgba(108,92,231,0.3);
        box-shadow: 0 12px 32px rgba(108,92,231,0.08);
    }}

    .m-card .label {{
        font-size: 0.78rem;
        font-weight: 600;
        color: {T["text_secondary"]};
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 8px;
    }}

    .m-card .value {{
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }}

    .m-card .sub {{
        font-size: 0.78rem;
        color: {T["text_secondary"]};
        margin-top: 4px;
    }}

    /* ---- Pills / Tags ---- */
    .tag {{
        display: inline-block;
        padding: 6px 14px;
        border-radius: 999px;
        margin: 4px 6px 4px 0;
        font-size: 0.82rem;
        font-weight: 600;
        border: 1px solid transparent;
    }}

    .tag-default {{
        background: rgba(108,92,231,0.12);
        color: {T["accent_light"]};
        border-color: rgba(108,92,231,0.2);
    }}

    .tag-success {{
        background: rgba(0,206,201,0.12);
        color: {T["success"]};
        border-color: rgba(0,206,201,0.2);
    }}

    .tag-danger {{
        background: rgba(255,107,107,0.12);
        color: {T["danger"]};
        border-color: rgba(255,107,107,0.2);
    }}

    .tag-warning {{
        background: rgba(253,203,110,0.1);
        color: {T["warning"]};
        border-color: rgba(253,203,110,0.2);
    }}

    /* ---- Info / alert boxes ---- */
    .hint-box {{
        padding: 12px 16px;
        border-radius: 10px;
        font-size: 0.84rem;
        line-height: 1.55;
        margin: 8px 0;
        border: 1px solid transparent;
    }}

    .hint-blue {{
        background: rgba(108,92,231,0.08);
        color: {T["text_secondary"]};
        border-color: rgba(108,92,231,0.15);
    }}

    .hint-green {{
        background: rgba(0,206,201,0.08);
        color: {T["success"]};
        border-color: rgba(0,206,201,0.15);
    }}

    .hint-red {{
        background: rgba(255,107,107,0.08);
        color: {T["danger"]};
        border-color: rgba(255,107,107,0.15);
    }}

    .hint-yellow {{
        background: rgba(253,203,110,0.08);
        color: {T["warning"]};
        border-color: rgba(253,203,110,0.15);
    }}

    /* ---- Detail row ---- */
    .detail {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 0;
        border-bottom: 1px solid {T["border"]};
    }}

    .detail:last-child {{
        border-bottom: none;
    }}

    .detail .dt {{
        font-size: 0.84rem;
        color: {T["text_secondary"]};
        font-weight: 500;
    }}

    .detail .dd {{
        font-size: 0.92rem;
        color: {T["text"]};
        font-weight: 600;
    }}

    /* ---- Buttons ---- */
    .stButton > button {{
        width: 100%;
        border: none;
        border-radius: 12px;
        padding: 0.85rem 1.2rem;
        background: {T["gradient"]};
        color: white;
        font-size: 0.95rem;
        font-weight: 700;
        letter-spacing: -0.2px;
        box-shadow: 0 8px 24px rgba(108,92,231,0.3);
        transition: all 0.25s ease;
    }}

    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 14px 32px rgba(108,92,231,0.4);
    }}

    .stDownloadButton > button {{
        width: 100%;
        border: none;
        border-radius: 12px;
        padding: 0.85rem 1.2rem;
        background: linear-gradient(135deg, {T["success"]}, #00b894);
        color: white;
        font-size: 0.95rem;
        font-weight: 700;
        letter-spacing: -0.2px;
        box-shadow: 0 8px 24px rgba(0,206,201,0.25);
    }}

    /* ---- File uploader ---- */
    div[data-testid="stFileUploader"] {{
        border: 2px dashed {T["border"]};
        border-radius: 12px;
        padding: 4px;
        transition: border-color 0.3s ease;
    }}

    div[data-testid="stFileUploader"]:hover {{
        border-color: rgba(108,92,231,0.35);
    }}

    /* ---- Text area ---- */
    .stTextArea textarea {{
        border-radius: 12px !important;
        border-color: {T["border"]} !important;
        background: rgba(255,255,255,0.03) !important;
        color: {T["text"]} !important;
        font-family: 'Inter', sans-serif !important;
        min-height: 120px !important;
    }}

    .stTextArea textarea:focus {{
        border-color: {T["accent"]} !important;
        box-shadow: 0 0 0 3px rgba(108,92,231,0.15) !important;
    }}

    /* ---- Tabs ---- */
    [data-testid="stTabs"] button {{
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: -0.2px !important;
    }}

    /* ---- Banner ---- */
    .result-banner {{
        padding: 16px 20px;
        border-radius: 12px;
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 1.2rem;
        animation: fadeUp 0.5s ease;
    }}

    .banner-excellent {{
        background: rgba(0,206,201,0.1);
        border: 1px solid rgba(0,206,201,0.2);
        color: {T["success"]};
    }}

    .banner-good {{
        background: rgba(108,92,231,0.1);
        border: 1px solid rgba(108,92,231,0.2);
        color: {T["accent_light"]};
    }}

    .banner-moderate {{
        background: rgba(253,203,110,0.1);
        border: 1px solid rgba(253,203,110,0.2);
        color: {T["warning"]};
    }}

    .banner-low {{
        background: rgba(255,107,107,0.1);
        border: 1px solid rgba(255,107,107,0.2);
        color: {T["danger"]};
    }}

    /* ---- Footer ---- */
    .footer {{
        text-align: center;
        padding: 2.5rem 0 1rem 0;
        color: {T["text_secondary"]};
        font-size: 0.8rem;
        opacity: 0.7;
    }}

    /* ---- Animations ---- */
    @keyframes fadeUp {{
        from {{ opacity: 0; transform: translateY(14px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
</style>
""", unsafe_allow_html=True)


# =========================================================
# HELPERS
# =========================================================
def render_tags(items, tag_class="tag-default"):
    if not items:
        st.markdown(f'<span class="tag {tag_class}">None detected</span>', unsafe_allow_html=True)
        return
    html = "".join([f'<span class="tag {tag_class}">{item}</span>' for item in items])
    st.markdown(html, unsafe_allow_html=True)


def detect_strengths(skills):
    patterns = {
        "python": "Python programming",
        "sql": "Database & query proficiency",
        "git": "Version control workflows",
        "machine learning": "Machine learning fundamentals",
        "pandas": "Data wrangling with Pandas",
        "streamlit": "Rapid prototyping & dashboards",
        "data analysis": "Analytical thinking",
        "react": "Frontend development",
        "javascript": "Web development",
        "tensorflow": "Deep learning frameworks",
        "pytorch": "Deep learning frameworks",
    }
    norm = [s.lower().strip() for s in skills]
    seen = set()
    strengths = []
    for skill in norm:
        desc = patterns.get(skill)
        if desc and desc not in seen:
            strengths.append(desc)
            seen.add(desc)
    return strengths


def score_band(score):
    if score >= 85:
        return "Excellent Match", "banner-excellent"
    elif score >= 65:
        return "Good Match", "banner-good"
    elif score >= 45:
        return "Moderate Match", "banner-moderate"
    return "Needs Improvement", "banner-low"


def score_color(score):
    if score >= 85:
        return T["success"]
    elif score >= 65:
        return T["accent_light"]
    elif score >= 45:
        return T["warning"]
    return T["danger"]


def build_gauge(score):
    color = score_color(score)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"suffix": "%", "font": {"size": 44, "color": T["text"], "family": "Inter"}},
        title={"text": "ATS Compatibility", "font": {"size": 14, "color": T["text_secondary"], "family": "Inter"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "rgba(255,255,255,0.1)", "tickwidth": 1},
            "bar": {"color": color, "thickness": 0.25},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 45], "color": "rgba(255,107,107,0.08)"},
                {"range": [45, 65], "color": "rgba(253,203,110,0.08)"},
                {"range": [65, 85], "color": "rgba(108,92,231,0.08)"},
                {"range": [85, 100], "color": "rgba(0,206,201,0.08)"},
            ],
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=10),
        height=280,
    )
    return fig


def build_donut(matched_count, missing_count):
    values = [matched_count, missing_count]
    labels = ["Matched", "Missing"]
    if matched_count == 0 and missing_count == 0:
        values, labels = [1], ["No data"]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.65,
        textinfo="label+percent",
        textfont=dict(size=12, family="Inter"),
        marker=dict(colors=[T["success"], T["danger"]][:len(values)]),
    )])
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=T["text"], family="Inter"),
        legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center"),
        margin=dict(l=5, r=5, t=5, b=5),
        height=280,
    )
    return fig


def build_bar(found, missing):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Matched", "Missing"],
        y=[found, missing],
        marker_color=[T["success"], T["danger"]],
        text=[found, missing],
        textposition="outside",
        textfont=dict(family="Inter", size=13, color=T["text"]),
        width=0.4,
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=T["text"], family="Inter"),
        margin=dict(l=10, r=10, t=10, b=10),
        height=280,
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)", title=""),
        xaxis=dict(title=""),
    )
    return fig


# =========================================================
# NAV BAR
# =========================================================
st.markdown("""
<div class="nav-bar">
    <div class="brand">
        <div class="brand-icon">⚡</div>
        ResumeIQ
    </div>
    <div class="nav-links">
        <span>Screen</span>
        <span>How it works</span>
        <span>For HR Teams</span>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# HERO
# =========================================================
st.markdown("""
<div class="hero">
    <div class="hero-badge">✦  HR TECHNOLOGY · AI-POWERED SCREENING</div>
    <h1>Screen candidates faster.<br>Hire with confidence.</h1>
    <p>
        Upload a candidate's resume, define the role requirements, and instantly
        get an ATS compatibility score, skill gap analysis, and AI-generated
        hiring recommendation — so your team can make data-driven decisions.
    </p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# INPUT SECTION
# =========================================================
col_left, col_right = st.columns(2, gap="large")

with col_left:
    with st.container(border=True):
        st.markdown('<div class="section-label">STEP 1</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">Upload candidate resume</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Drop the applicant\'s PDF resume here. Text-based PDFs yield the best results.</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload Resume (PDF)",
            type=["pdf"],
            label_visibility="collapsed"
        )

with col_right:
    with st.container(border=True):
        st.markdown('<div class="section-label">STEP 2</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">Define role requirements</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">List the must-have skills for this position, separated by commas.</div>', unsafe_allow_html=True)
        job_skills_input = st.text_area(
            "Required Skills",
            placeholder="e.g. Python, SQL, Machine Learning, Git, Pandas, React",
            label_visibility="collapsed",
            height=120,
        )

st.markdown("")
analyze_clicked = st.button("⚡  Screen Candidate")


# =========================================================
# MAIN LOGIC
# =========================================================
if analyze_clicked and not uploaded_file:
    st.markdown(
        '<div class="hint-box hint-yellow">Please upload a candidate\'s PDF resume to begin screening.</div>',
        unsafe_allow_html=True,
    )

elif analyze_clicked and uploaded_file:
    try:
        with st.spinner("Parsing resume, matching skills, and generating AI insights…"):
            text = extract_text_from_pdf(uploaded_file)

            if not text or not text.strip():
                st.error("Could not extract text from this PDF. Try a text-based resume.")
                st.stop()

            name = extract_name(text)
            email = extract_email(text)
            skills = extract_skills(text)
            experience = extract_experience(text)

            required_skills = [
                s.strip() for s in job_skills_input.split(",") if s.strip()
            ]

            if not required_skills:
                st.error("Please enter at least one required skill.")
                st.stop()

            score, matched, missing = calculate_match_score(skills, required_skills)
            result = recommendation(score)
            insight = hiring_insight(score)

            report = {
                "candidate_name": name,
                "email": email,
                "skills": skills,
                "experience_years": experience,
                "match_score": score,
                "matched_skills": matched,
                "missing_skills": missing,
                "recommendation": result,
            }

            os.makedirs("reports", exist_ok=True)
            save_report(report, "reports/report.json")
            json_report = json.dumps(report, indent=4)

            band_text, band_class = score_band(score)
            strengths = detect_strengths(skills)

            ai_report = None
            ai_error = None
            try:
                ai_report = ai_resume_analysis(text, job_skills_input)
            except Exception as e:
                ai_error = str(e)

        # =========================================================
        # RESULTS
        # =========================================================
        st.markdown("---")

        # ---- Result banner ----
        st.markdown(
            f'<div class="result-banner {band_class}">'
            f'<strong>{band_text}</strong> — {result}. {insight}'
            f'</div>',
            unsafe_allow_html=True,
        )

        # ---- Metric cards ----
        st.markdown(f"""
        <div class="metric-row">
            <div class="m-card">
                <div class="label">ATS Score</div>
                <div class="value" style="color:{score_color(score)}">{score}%</div>
                <div class="sub">role compatibility</div>
            </div>
            <div class="m-card">
                <div class="label">Skills Found</div>
                <div class="value" style="color:{T["text"]}">{len(skills)}</div>
                <div class="sub">on candidate profile</div>
            </div>
            <div class="m-card">
                <div class="label">Matched</div>
                <div class="value" style="color:{T["success"]}">{len(matched)}</div>
                <div class="sub">meets requirements</div>
            </div>
            <div class="m-card">
                <div class="label">Gaps</div>
                <div class="value" style="color:{T["danger"]}">{len(missing)}</div>
                <div class="sub">candidate gaps</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ---- Tabs ----
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋  Overview",
            "🎯  Skills",
            "🤖  AI Insights",
            "📄  Resume Text",
            "📥  Export",
        ])

        # ---- TAB 1: Overview ----
        with tab1:
            c1, c2 = st.columns([1, 1], gap="large")

            with c1:
                with st.container(border=True):
                    st.markdown('<div class="section-label">APPLICANT</div>', unsafe_allow_html=True)
                    st.markdown('<div class="section-heading">Candidate Profile</div>', unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="detail"><span class="dt">Name</span><span class="dd">{name or 'Not detected'}</span></div>
                    <div class="detail"><span class="dt">Email</span><span class="dd">{email or 'Not detected'}</span></div>
                    <div class="detail"><span class="dt">Experience</span><span class="dd">{experience} years</span></div>
                    <div class="detail"><span class="dt">Skills detected</span><span class="dd">{len(skills)}</span></div>
                    <div class="detail"><span class="dt">Recommendation</span><span class="dd">{result}</span></div>
                    """, unsafe_allow_html=True)

                    st.markdown("")
                    st.markdown('<div class="section-label">DETECTED SKILLS</div>', unsafe_allow_html=True)
                    render_tags(skills, "tag-default")

            with c2:
                with st.container(border=True):
                    st.markdown('<div class="section-label">ATS SCORE</div>', unsafe_allow_html=True)
                    st.plotly_chart(build_gauge(score), use_container_width=True)

                    if strengths:
                        st.markdown('<div class="section-label" style="margin-top:8px;">KEY STRENGTHS</div>', unsafe_allow_html=True)
                        for s in strengths:
                            st.markdown(f'<div class="hint-box hint-green">✓  {s}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(
                            '<div class="hint-box hint-yellow">No major strength patterns detected from extracted skills.</div>',
                            unsafe_allow_html=True,
                        )

        # ---- TAB 2: Skills ----
        with tab2:
            s1, s2 = st.columns([1, 1], gap="large")

            with s1:
                with st.container(border=True):
                    st.markdown('<div class="section-label">SKILL GAP ANALYSIS</div>', unsafe_allow_html=True)
                    st.markdown('<div class="section-heading">Matched Skills</div>', unsafe_allow_html=True)
                    render_tags(matched, "tag-success")

                    st.markdown("")
                    st.markdown('<div class="section-heading">Missing Skills</div>', unsafe_allow_html=True)
                    render_tags(missing, "tag-danger")

                    st.markdown("")
                    st.markdown('<div class="section-heading">Required by Job</div>', unsafe_allow_html=True)
                    render_tags(required_skills, "tag-warning")

            with s2:
                with st.container(border=True):
                    st.markdown('<div class="section-label">VISUAL BREAKDOWN</div>', unsafe_allow_html=True)
                    st.plotly_chart(build_donut(len(matched), len(missing)), use_container_width=True)
                    st.plotly_chart(build_bar(len(matched), len(missing)), use_container_width=True)

        # ---- TAB 3: AI Insights ----
        with tab3:
            with st.container(border=True):
                st.markdown('<div class="section-label">AI RECRUITER</div>', unsafe_allow_html=True)
                st.markdown('<div class="section-heading">Detailed Hiring Analysis</div>', unsafe_allow_html=True)
                st.markdown('<div class="section-sub">AI-generated evaluation based on the candidate\'s resume and your role requirements.</div>', unsafe_allow_html=True)

                if ai_error:
                    st.markdown(
                        f'<div class="hint-box hint-red">AI analysis unavailable: {ai_error}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(ai_report)

        # ---- TAB 4: Resume Text ----
        with tab4:
            with st.container(border=True):
                st.markdown('<div class="section-label">RAW TEXT</div>', unsafe_allow_html=True)
                st.markdown('<div class="section-heading">Extracted Resume Content</div>', unsafe_allow_html=True)
                st.markdown('<div class="section-sub">Full text extracted from the candidate\'s uploaded PDF for your review.</div>', unsafe_allow_html=True)
                st.text_area(
                    "Resume Content",
                    value=text,
                    height=400,
                    label_visibility="collapsed",
                )

        # ---- TAB 5: Export ----
        with tab5:
            e1, e2 = st.columns(2, gap="large")

            with e1:
                with st.container(border=True):
                    st.markdown('<div class="section-label">EXPORT</div>', unsafe_allow_html=True)
                    st.markdown('<div class="section-heading">Download Report</div>', unsafe_allow_html=True)
                    st.markdown(
                        '<div class="section-sub">Structured JSON report with candidate data, ATS score, skill analysis, and hiring recommendation for your records.</div>',
                        unsafe_allow_html=True,
                    )
                    st.download_button(
                        label="📥  Download JSON Report",
                        data=json_report,
                        file_name="resume_report.json",
                        mime="application/json",
                    )

            with e2:
                with st.container(border=True):
                    st.markdown('<div class="section-label">SUMMARY</div>', unsafe_allow_html=True)
                    st.markdown('<div class="section-heading">Quick Overview</div>', unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="detail"><span class="dt">Candidate</span><span class="dd">{name or 'Unknown'}</span></div>
                    <div class="detail"><span class="dt">ATS Score</span><span class="dd" style="color:{score_color(score)}">{score}%</span></div>
                    <div class="detail"><span class="dt">Recommendation</span><span class="dd">{result}</span></div>
                    <div class="detail"><span class="dt">Skills gaps</span><span class="dd">{len(missing)}</span></div>
                    """, unsafe_allow_html=True)

    except Exception as e:
        st.markdown(
            f'<div class="hint-box hint-red"><strong>Error:</strong> {str(e)}</div>',
            unsafe_allow_html=True,
        )


# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div class="footer">
    ResumeIQ — HR Technology  ·  AI-Powered Screening  ·  ATS Intelligence  ·  Skill Gap Analysis  ·  Built for Hiring Teams
</div>
""", unsafe_allow_html=True)
