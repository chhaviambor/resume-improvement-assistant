# utils/summarizer.py
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

def extractive_summary(text, sentence_count=2):
    if not text:
        return ""
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        sents = summarizer(parser.document, sentence_count)
        return " ".join(str(s) for s in sents) or text[:300]
    except Exception:
        return text[:300]
