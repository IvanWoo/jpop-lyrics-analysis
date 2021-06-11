from pathlib import Path

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

from jpop_lyrics_analysis.databases import Sqlite
from jpop_lyrics_analysis.scrapers import UtaNet
from jpop_lyrics_analysis.splitters import SentenceSplitter

CURRENT_DIR = Path(__file__).resolve()
WORD_FEED_FILE = CURRENT_DIR.parents[1] / "tmp" / "word_feed.txt"
MASK_FILE = CURRENT_DIR.parent / "resources" / "ebichu-2x.png"
OUTPUT_FILE = CURRENT_DIR.parents[1] / "tmp" / "word_cloud.png"


def get_lyrics(url):
    scraper = UtaNet()
    # TODO: use contextmanager for db
    db = Sqlite()
    for jpop in scraper.parse(url):
        db.insert(jpop)
    db.close()
    return


def morphological_analysis(artist):
    # TODO: Try different extraction criteria.
    criterias = ["名詞-一般", "動詞-自立", "名詞-代名詞-一般"]
    splitter = SentenceSplitter(criterias)
    words_feed = splitter.get_word_feed(artist)

    with open(WORD_FEED_FILE, "w") as file:
        file.write(" ".join(words_feed))
    print(f"{WORD_FEED_FILE} is generated")


# https://github.com/amueller/word_cloud/blob/master/examples/simple.py
def generate_word_cloud():
    # Read the whole text
    text = WORD_FEED_FILE.read_text()
    ebichu_mask = np.array(Image.open(MASK_FILE))

    # Generate a word cloud image
    wordcloud = WordCloud(
        font_path="/System/Library/Fonts/PingFang.ttc",
        background_color="white",
        max_words=200,
        mask=ebichu_mask,
    ).generate(text)

    # Generate the image
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(OUTPUT_FILE, dpi=300)
    print(f"{OUTPUT_FILE} is generated")
