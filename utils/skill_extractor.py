# utils/skill_extractor.py
import json, os
from rake_nltk import Rake
from rapidfuzz import process, fuzz

BASE = os.path.dirname(__file__)

def load_skills(path=None):
    if path is None:
        path = os.path.join(BASE, "skills.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return [d.strip() for d in data if d]

def extract_keywords_with_rake(text, max_keywords=30):
    r = Rake()
    r.extract_keywords_from_text(text)
    phrases = r.get_ranked_phrases()
    out = [p.strip().lower() for p in phrases[:max_keywords] if p]
    return out

def extract_skills_and_matches(text, skills_db=None, fuzzy_threshold=75):
    if skills_db is None:
        skills_db = load_skills()
    rake_phrases = extract_keywords_with_rake(text, max_keywords=80)
    tokens = [t.lower() for t in text.split() if len(t) > 2]
    candidates = list(dict.fromkeys(rake_phrases + tokens))
    matches = []
    for cand in candidates:
        best = process.extractOne(cand, skills_db, scorer=fuzz.ratio)
        if best:
            name, score, _ = best
            if score >= fuzzy_threshold:
                matches.append((name, int(score), cand))
    # dedupe keep highest
    best_map = {}
    for name,score,cand in matches:
        if name not in best_map or score > best_map[name][0]:
            best_map[name] = (score, cand)
    out = [(name,score, best_map[name][1]) for name in best_map]
    out.sort(key=lambda x: x[1], reverse=True)
    return out, out
