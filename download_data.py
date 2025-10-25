# download_data.py
import nltk, subprocess, sys

# NLTK resources
resources = ['punkt', 'punkt_tab', 'stopwords', 'averaged_perceptron_tagger', 'wordnet']
for r in resources:
    try:
        nltk.data.find(r)
    except LookupError:
        print("Downloading", r)
        nltk.download(r)

# spaCy model
try:
    import spacy
    spacy.load("en_core_web_sm")
except Exception:
    print("Downloading spaCy model en_core_web_sm")
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True)
print("All data downloaded.")
