# utils/scoring.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_tfidf_similarity(text1, text2):
    if not text1 or not text2:
        return 0.0
    vect = TfidfVectorizer(stop_words='english', max_features=2000)
    try:
        X = vect.fit_transform([text1, text2])
        sim = cosine_similarity(X[0:1], X[1:2])[0][0]
        return float(sim)
    except Exception:
        return 0.0

def compute_ats_score_and_diagnostics(matched_count, job_keyword_count, header_keyword_bonus, resume_word_count, tfidf_sim):
    if job_keyword_count <= 0:
        base_ratio = 0.0
    else:
        base_ratio = matched_count / job_keyword_count

    # weights
    w_keywords = 0.60
    w_header = 0.15
    w_length = 0.10
    w_tfidf = 0.15

    header_score = 1.0 if header_keyword_bonus else 0.0

    if resume_word_count < 80:
        length_score = 0.0
    elif resume_word_count < 200:
        length_score = 0.5
    else:
        length_score = 1.0

    raw = (w_keywords*base_ratio) + (w_header*header_score) + (w_length*length_score) + (w_tfidf*tfidf_sim)
    score = int(max(0, min(100, round(raw*100))))
    explanation = f"Keywords {matched_count}/{job_keyword_count} => ratio {base_ratio:.2f}; header_bonus={header_keyword_bonus}; length_score={length_score}; tfidf={tfidf_sim:.3f}"
    return {
        "matched_count": matched_count,
        "job_keyword_count": job_keyword_count,
        "base_keyword_ratio": round(base_ratio,3),
        "header_bonus": header_keyword_bonus,
        "length_score": length_score,
        "tfidf_similarity": round(tfidf_sim,4),
        "raw_fraction": round(raw,4),
        "ats_score": score,
        "explanation": explanation
    }
