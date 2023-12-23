# wordcloud_script.py

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd

def generate_wordcloud(csv_file):
    df = pd.read_csv(csv_file, encoding="latin-1")

    comment_words = ''
    stopwords = set(STOPWORDS)

    for val in df.CONTENT:
        val = str(val)
        tokens = val.split()

        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()

        comment_words += " ".join(tokens) + " "

    wordcloud = WordCloud(width=800, height=800,
                          background_color='white',
                          stopwords=stopwords,
                          min_font_size=10).generate(comment_words)

    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    plt.show()

# Example usage:
# generate_wordcloud("Youtube04-Eminem.csv")
