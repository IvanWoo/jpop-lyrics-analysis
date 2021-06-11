import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString

from jpop_lyrics_analysis.models import Jpop


class UtaNet:
    domain = "http://www.uta-net.com"

    def get_lyrics(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        contents = soup.find("div", {"id": "kashi_area"}).contents
        lyrics = " ".join(filter(lambda x: type(x) == NavigableString, contents))

        # replace full-width space with half-width one
        return lyrics.replace("\u3000", " ").replace("　", " ")

    def parse(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")

        for table in soup.find_all("tr"):
            if table.th:
                continue

            title = table.find("td", {"class": "side td1"}).text
            lyric_url = self.domain + table.find("td", {"class": "side td1"}).a["href"]
            artist = table.find("td", {"class": "td2"}).text
            lyricist = table.find("td", {"class": "td3"}).text
            composer = table.find("td", {"class": "td4"}).text
            lyrics = self.get_lyrics(lyric_url)

            yield Jpop(
                title=title,
                lyric_url=lyric_url,
                artist=artist,
                lyricist=lyricist,
                composer=composer,
                lyrics=lyrics,
            )
