import argparse
import sqlite3

import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString


class JpopLyrics:
    def __init__(self, data_base):
        self.connection = sqlite3.connect(data_base)
        self.cursor = self.connection.cursor()
        self.DOMAIN = "http://www.uta-net.com"

    def _initialize_database(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS jpop
            (title text, artist text, lyricist text, composer text, lyric_url text, lyrics text)
            """
        )

    def _save_to_database(self, title, artist, lyricist, composer, lyric_url, lyrics):
        self.cursor.execute(
            "INSERT INTO jpop VALUES "
            + str((title, artist, lyricist, composer, lyric_url, lyrics))
        )

    @staticmethod
    def get_lyrics(url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        contents = soup.find("div", {"id": "kashi_area"}).contents
        lyrics = " ".join(filter(lambda x: type(x) == NavigableString, contents))

        # replace full-width space with half-width one
        return lyrics.replace("\u3000", " ").replace("　", " ")

    def _is_exist(self, title):
        self.cursor.execute("SELECT title FROM jpop WHERE title=?", (title,))
        return self.cursor.fetchone() is not None

    def parse_lyrics(self, url):
        self._initialize_database()
        html = requests.get(url)
        soup = BeautifulSoup(html.text, "lxml")

        for table in soup.find_all("tr"):
            if table.th:
                continue
            title = table.find("td", {"class": "side td1"}).text
            lyric_url = self.DOMAIN + table.find("td", {"class": "side td1"}).a["href"]
            artist = table.find("td", {"class": "td2"}).text
            lyricist = table.find("td", {"class": "td3"}).text
            composer = table.find("td", {"class": "td4"}).text
            lyrics = JpopLyrics.get_lyrics(lyric_url)
            if self._is_exist(title):
                print(str(title) + " EXISTED in the database")
                continue
            else:
                self._save_to_database(
                    title, artist, lyricist, composer, lyric_url, lyrics
                )
                print("SAVED " + str(title) + " into the database")
                self.connection.commit()

        self.connection.close()


def main():
    parser = argparse.ArgumentParser(description="download jpop lyrics")
    # 私立恵比寿中学: http://www.uta-net.com/artist/12973/
    parser.add_argument("-u", "--url", type=str)
    args = parser.parse_args()

    db = JpopLyrics("jpop-lyrics.db")
    db.parse_lyrics(args.url)
    return


if __name__ == "__main__":
    main()
