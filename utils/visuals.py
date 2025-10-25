# utils/visuals.py
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
from PIL import Image

def make_wordcloud(text, width=600, height=300, max_words=100):
    if not text:
        text = "empty"
    wc = WordCloud(width=width, height=height, background_color="white", max_words=max_words)
    wc.generate(text)
    fig = plt.figure(figsize=(6,3))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    buf = io.BytesIO()
    plt.tight_layout(pad=0)
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)
