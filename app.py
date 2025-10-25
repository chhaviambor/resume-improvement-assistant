# app.py
import streamlit as st
import json, os
from io import BytesIO
import pdfplumber

# Ensure NLP data available on first run
import nltk
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('wordnet', quiet=True)

# Import our utilities (these files must be in utils/)
from utils.text_utils import clean_text, get_word_count, flesch_reading_ease
from utils.skill_extractor import load_skills, extract_skills_and_matches, extract_keywords_with_rake
from utils.scoring import calculate_tfidf_similarity, compute_ats_score_and_diagnostics
from utils.summarizer import extractive_summary
from utils.visuals import make_wordcloud
from PIL import Image

st.set_page_config(page_title="Resume Improvement Assistant", layout="wide")
st.title("📝 Resume Improvement Assistant")

# Sidebar demo buttons
with st.sidebar:
    st.header("Instructions")
    st.write("Paste resume text or upload PDF. Paste job description. Click Analyze.")
    if st.button("Load demo resume"):
        st.session_state.demo_resume = True
    if st.button("Load demo job"):
        st.session_state.demo_job = True

col1, col2 = st.columns(2)
with col1:
    st.subheader("Resume")
    uploaded_file = st.file_uploader("Upload PDF (optional)", type=["pdf"])
    resume_text = st.text_area("Or paste resume text here", height=250)
    if st.session_state.get("demo_resume"):
        demo_path = os.path.join("sample_data", "demo_resume.txt")
        if os.path.exists(demo_path):
            resume_text = open(demo_path, encoding="utf-8").read()
            st.session_state.demo_resume = False
            st.experimental_rerun()

with col2:
    st.subheader("Job Description")
    job_text = st.text_area("Paste job description here", height=250)
    if st.session_state.get("demo_job"):
        demo_j = os.path.join("sample_data", "demo_job.txt")
        if os.path.exists(demo_j):
            job_text = open(demo_j, encoding="utf-8").read()
            st.session_state.demo_job = False
            st.experimental_rerun()

if st.button("Analyze"):
    if uploaded_file:
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                resume_text = "\n".join([p.extract_text() or "" for p in pdf.pages])
        except Exception as e:
            st.error("PDF extraction failed. Please paste text. Error: " + str(e))
            st.stop()

    if not resume_text or not job_text:
        st.error("Please provide both resume and job description.")
        st.stop()

    # Clean
    resume_clean = clean_text(resume_text)
    job_clean = clean_text(job_text)

    # Load skills DB
    skills_db = load_skills(os.path.join("utils", "skills.json"))

    # Keyword extraction
    job_keywords = extract_keywords_with_rake(job_clean, max_keywords=40)
    resume_skills, resume_matches = extract_skills_and_matches(resume_clean, skills_db, fuzzy_threshold=72)

    # Matching with job keywords (fuzzy)
    matched = []
    for s_name, score, phrase in resume_matches:
        for jk in job_keywords:
            from rapidfuzz import fuzz
            if fuzz.ratio(s_name.lower(), jk.lower()) >= 75 or fuzz.ratio(phrase.lower(), jk.lower()) >= 75:
                matched.append((s_name, score, phrase))
                break
    # dedupe matched names
    matched_names = list({m[0].lower(): m for m in matched}.values())

    # missing = job keywords not covered by matched names
    matched_lower = [m[0].lower() for m in matched_names]
    missing = [jk for jk in job_keywords if jk.lower() not in matched_lower]

    # header presence
    header_text = "\n".join(resume_text.splitlines()[:6])
    header_present = any(jk.lower() in header_text.lower() for jk in job_keywords[:6])

    # tfidf sim
    tfidf_sim = calculate_tfidf_similarity(resume_clean, job_clean)

    # score
    diagnostics = compute_ats_score_and_diagnostics(len(matched_names), max(1, len(job_keywords)), header_present, get_word_count(resume_clean), tfidf_sim)

    # summary
    summary = extractive_summary(resume_text, sentence_count=2)

    # suggestions
    suggestions = []
    if missing:
        suggestions.append("Consider adding top missing keywords in summary/top lines: " + ", ".join(missing[:8]))
    if get_word_count(resume_clean) < 80:
        suggestions.append("Resume is short (<80 words). Add project details and achievements.")
    if "%" not in resume_text and "percent" not in resume_text:
        suggestions.append("Quantify achievements where possible (e.g., 'reduced time by 30%').")
    suggestions.append("Place most important keywords in the first 3 lines (summary/header).")

    # UI display
    left, right = st.columns([2,1])
    with left:
        st.metric("ATS Score", f"{diagnostics['ats_score']}/100")
        st.write("Explanation: ", diagnostics['explanation'])
        st.subheader("Summary (extractive)")
        st.write(summary)
        st.subheader("Matched skills (name, confidence, phrase)")
        if matched_names:
            for name,score,phrase in matched_names:
                st.write(f"- {name} (confidence {score}%) — matched phrase: '{phrase}'")
        else:
            st.write("No matched skills found.")
        st.subheader("Missing / recommended keywords")
        st.write(", ".join(missing) if missing else "None")

        st.subheader("Suggestions")
        for s in suggestions:
            st.write("•", s)

    with right:
        st.write("Resume word count:", get_word_count(resume_clean))
        st.write("Flesch reading ease:", flesch_reading_ease(resume_clean))
        st.write("TF-IDF similarity:", round(tfidf_sim,3))
        st.write("Top job keywords:", job_keywords[:20])

        try:
            wc_res = make_wordcloud(resume_clean)
            st.image(wc_res, caption="Resume word cloud")
        except Exception as e:
            st.write("Wordcloud error:", e)

    with st.expander("Advanced diagnostics"):
        st.json(diagnostics)
        st.write("All extracted resume skills (raw):", resume_skills)
        st.write("Job keywords (top):", job_keywords[:40])
