# Resume Improvement Assistant — Project Report

## 1. Project Title
Resume Improvement Assistant (NLP)

## 2. Problem Statement
Many job applicants fail initial screening by Applicant Tracking Systems (ATS) because their resumes do not contain the keywords or format the ATS expects. The goal of this project is to build an NLP-based tool that analyzes a candidate's resume against a job description and produces a clear, actionable ATS score and suggestions to improve the resume.

## 3. Dataset
- No external proprietary dataset was required. The app accepts user-provided resumes and job descriptions.
- A local `skills.json` of ~100–200 commonly required skills (programming languages, tools, soft skills) is bundled for matching.
- Demo inputs provided in `sample_data/` for testing.

## 4. Methodology / System Design
Pipeline:
1. **Input** — Resume (PDF upload or pasted text) and Job Description (pasted).
2. **Preprocessing** — Clean text, remove URLs/punctuation, lowercase, basic tokenization.
3. **Keyword Extraction** — RAKE (Rapid Automatic Keyword Extraction) extracts candidate phrases; also use token candidates.
4. **Skill Matching** — Fuzzy matching (RapidFuzz) against `skills.json`. Exact matches from resume are also detected.
5. **Vectorization & Similarity** — TF–IDF vectorization and cosine similarity between resume and job description to capture overall semantic similarity.
6. **Scoring** — A deterministic ATS scoring function combines:
   - Keyword match ratio (main factor)
   - Header/summary keyword presence (bonus)
   - Resume length/readability (minor weight)
   - TF–IDF semantic similarity (minor weight)
7. **Summary** — Extractive summarization using LexRank (Sumy) to produce a 1–3 sentence resume summary.
8. **Suggestions** — Rule-based suggestions that explain which keywords to add, where to place them (top of resume), and encourage quantifying achievements.

## 5. Key NLP Concepts Used
- Text preprocessing (tokenization, normalization)
- Keyword extraction (RAKE)
- Fuzzy matching (RapidFuzz)
- Vectorization (TF–IDF) and cosine similarity
- Extractive summarization (LexRank)
- Readability heuristics

## 6. Implementation Details
- Language: Python 3.10+
- Framework: Streamlit for UI
- Libraries: spaCy, nltk, rake-nltk, rapidfuzz, scikit-learn, sumy, pdfplumber, wordcloud, matplotlib
- All processing performed locally; no third-party paid APIs.

## 7. Results
Example test (demo resume vs. demo job):
- Matched skills: Python, SQL, Power BI, Tableau
- Missing keywords: Predictive Analytics, Communication Skills
- ATS Score: 85/100
- Suggestions:
  - Add “Predictive Analytics” to the summary if relevant.
  - Quantify achievements (e.g., “reduced reporting time by 30%”).
  
Screenshots of UI, diagnostics, and wordclouds are included in the `screenshots/` folder.

## 8. Evaluation & Limitations
- The system is deterministic and explainable — each contribution to the ATS score is shown in diagnostics.
- Limitations:
  - RAKE + fuzzy matching depends on surface forms; synonyms may be missed unless skill DB is extended.
  - Scanned PDFs require OCR to extract text.
  - Scoring weights are heuristic and require tuning for different roles.

## 9. Future Work
- Integrate semantic embeddings (Sentence-BERT) for better synonym detection.
- Add OCR for scanned resumes (Tesseract).
- Provide templates & auto-rewrite suggestions (rephrase bullets to include keywords).
- Add user accounts to save analyses.

## 10. How to run (repeated)
(See README.md steps)

## 11. Appendix
- `skills.json` – list of skills used for matching
- sample inputs and outputs included in `sample_data/`
- contact: Chhavi Ambor — chhavijain2264@gmail.com
