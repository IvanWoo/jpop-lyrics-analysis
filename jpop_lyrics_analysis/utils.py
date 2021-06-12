import uuid
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from wordcloud import WordCloud

from jpop_lyrics_analysis.databases import Sqlite
from jpop_lyrics_analysis.scrapers import UtaNet
from jpop_lyrics_analysis.splitters import SentenceSplitter

CURRENT_DIR = Path(__file__).resolve()
ROOT_DIR = CURRENT_DIR.parents[1]
PACKAGE_DIR = CURRENT_DIR.parent
TMP_DIR = ROOT_DIR / "tmp"
TMP_DIR.mkdir(parents=True, exist_ok=True)
TMP_AFFIX = f"{datetime.now().strftime('%Y-%m-%d')}-{str(uuid.uuid1())}"
WORD_FEED_FILE = TMP_DIR / f"word-feed-{TMP_AFFIX}.txt"
MASK_FILE = PACKAGE_DIR / "resources" / "ebichu-2x.png"
OUTPUT_FILE = TMP_DIR / f"word-cloud-{TMP_AFFIX}.png"


def get_lyrics(url):
    scraper = UtaNet()
    with Sqlite() as db:
        for jpop in scraper.parse(url):
            if db.is_exist(jpop.title, jpop.artist):
                print(f"{jpop} EXISTED in the database")
                continue
            # get_lyrics is very expensive, call it when the entry is not exist
            jpop.lyrics = scraper.get_lyrics(jpop.lyric_url)
            db.insert(jpop)
    return


def get_artists():
    with Sqlite() as db:
        return db.artists()


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
