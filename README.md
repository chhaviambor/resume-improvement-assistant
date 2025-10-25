# Resume Improvement Assistant (NLP)

A Streamlit web app that analyzes a resume against a job description and produces an ATS compatibility score, matched/missing skills, a concise extractive summary, and prioritized suggestions to improve the resume.

## Demo
Open `app.py` with Streamlit:

## Features
- Upload resume (PDF) or paste resume text
- Paste job description
- Extract keywords and skills using RAKE + fuzzy matching against a local skills database
- Compute TF–IDF similarity and an interpretable ATS score (0–100)
- Generate extractive summary (LexRank)
- Produce matched skills, missing keywords, suggestions, and wordclouds
- Download analysis as JSON or text report

## Repository Structure
- `app.py` — Streamlit application
- `utils/` — helper modules (text processing, skill extraction, scoring, summarizer, visuals)
- `skills.json` — skill database used for matching
- `sample_data/` — sample resume and job posts for testing
- `REPORT.md` — full project report (convert to PDF for submission)
- `requirements.txt` — Python dependencies

## How to run (local)
1. Create a virtual environment:
2. Activate the venv:
- Windows (CMD): `venv\Scripts\activate`
- PowerShell: `.\venv\Scripts\Activate.ps1` (may need to allow execution policy temporarily)
- macOS / Linux: `source venv/bin/activate`
3. Install dependencies:
4. Download NLTK & spaCy models (first run, or run `download_data.py` if included):
5. Run the app:

## How to use
- Paste or upload a resume.
- Paste the job description.
- Click **Analyze** and view results. Use “Advanced diagnostics” to inspect internal metrics.

## Notes
- The repo uses only free libraries and runs on Replit or locally.
- For scanned PDFs, the app needs OCR (not included).

## License
This project is released under the MIT License. See the LICENSE file.

## Contact
Chhavi Ambor — email: chhavijain2264@gmail.com
