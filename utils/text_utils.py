# utils/text_utils.py
import re
import spacy

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = str(text)
    text = text.replace('\r', ' ').replace('\n', ' ')
    text = re.sub(r'https?:\/\/\S+', '', text)
    text = re.sub(r'[^A-Za-z0-9%.,;:\'\"()&\- ]+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower()

def get_word_count(text: str) -> int:
    return len(re.findall(r'\w+', text)) if text else 0

def estimate_syllables(word: str) -> int:
    word = word.lower()
    vowels = "aeiouy"
    count = 0
    prev = False
    for ch in word:
        is_v = ch in vowels
        if is_v and not prev:
            count += 1
        prev = is_v
    if word.endswith('e') and count > 1:
        count -= 1
    return count or 1

def flesch_reading_ease(text: str) -> float:
    words = get_word_count(text)
    sentences = max(1, text.count('.') + text.count('!') + text.count('?'))
    syllables = sum(estimate_syllables(w) for w in re.findall(r'\w+', text))
    try:
        flesch = 206.835 - 1.015*(words/sentences) - 84.6*(syllables/words)
    except Exception:
        flesch = 0.0
    return round(flesch, 2)
