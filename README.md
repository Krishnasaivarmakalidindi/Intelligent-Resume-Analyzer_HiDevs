# Intelligent Resume Analyzer

Intelligent Resume Analyzer is an AI-powered resume screening tool that parses PDF resumes, matches candidate skills against job requirements, computes an ATS-style score, generates hiring recommendations, and produces JSON reports.

## Features

- Resume parsing (PDF → text)
- Skill extraction and experience estimation
- Skill matching vs. job requirements with match scoring
- AI-powered summary and hiring recommendation
- Visual dashboard with charts (Streamlit)
- Exportable JSON report

## Tech Stack

- Python 3.8+
- Streamlit (UI)
- PyPDF2 (PDF parsing)
- pandas, matplotlib (data processing & visualization)
- groq (optional API integration)
- python-dotenv (env management)

## Project Architecture

- `app.py` — Streamlit UI and orchestration
- `ai_analyzer.py` — AI prompt wrapper and analysis functions
- `parser.py` — PDF text extraction and resume field parsers
- `matcher.py` — skill matching, scoring, and recommendations
- `report_generator.py` — save/export JSON reports into `reports/`
- `resumes/` — example input resumes (PDF)
- `reports/` — saved JSON reports (e.g. `reports/report.json`)

## Installation

1. Create a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a local `.env` from `.env.example` and set secrets:

```bash
cp .env.example .env
# then edit .env to set GROQ_API_KEY and other secrets
```

## How to Run

Start the Streamlit app:

```bash
streamlit run app.py
```

Upload a PDF resume, enter required skills (comma separated), and click "Analyze Resume".

## Sample Output

Example JSON report saved to `reports/report.json`:

```json
{
	"candidate_name": "Krishna SaiVarmaKalidindi Junior Data Analyst | B.Tech CSE StudentHyderabad, India",
	"email": "Envelopevarmatowork8642@gmail.com",
	"skills": ["SQL","CSS","Flutter","React","EDA","Python","Data Cleaning","Supabase","LLM","PostgreSQL","Pandas","Git","REST API","OpenAI","AI","Data Analysis","Prompt Engineering","MySQL","Scikit-learn","ML","GitHub","Firebase","MongoDB","NumPy"],
	"experience_years": 2,
	"match_score": 80,
	"matched_skills": ["Python","SQL","Git","Pandas"],
	"missing_skills": ["Machine Learning"],
	"recommendation": "Highly Recommended"
}
```

## Future Improvements

- Add CI checks and unit tests for parser and matcher modules
- Integrate secure secret management (Vault/Secrets Manager)
- Add job-description ingestion and automatic skill extraction
- Add user authentication and role-based access control
- Provide batch processing for multiple resumes and CSV export

---

If you need, I can also add a CONTRIBUTING guide, tests, or a minimal Dockerfile to run the app in a container.
