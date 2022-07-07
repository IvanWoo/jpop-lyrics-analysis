import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString

from jpop_lyrics_analysis.models import Jpop


class UtaNet:
    domain = "https://www.uta-net.com"

    def validate(self, url: str) -> bool:
        artist_url = f"{self.domain}/artist/"
        return url.startswith(artist_url)

    def get_lyrics(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        contents = soup.find("div", {"id": "kashi_area"}).contents
        lyrics = " ".join(filter(lambda x: type(x) == NavigableString, contents))

        # replace full-width space with half-width one
        return lyrics.replace("\u3000", " ").replace("　", " ")

    def get_all_pages(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        pages = set([url])
        for anchor in soup.find("div", {"id": "page_list"}).find_all("a", href=True):
            pages.add(anchor["href"])
        return pages

    def parse_one(self, url):
        print(f"start scraping from {url}")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")

        for table in soup.find_all("tr"):
            if table.th:
                continue
            tds = table.find_all("td")
            if len(tds) <= 4:
                continue

            title = (
                tds[0]
                .find("span", {"class": lambda x: "songlist-title" in x.split()})
                .text
            )
            lyric_url = self.domain + tds[0].find("a")["href"]
            artist = tds[1].text
            lyricist = tds[2].text
            composer = tds[3].text
            lyrics = None

            yield Jpop(
                title=title,
                lyric_url=lyric_url,
                artist=artist,
                lyricist=lyricist,
                composer=composer,
                lyrics=lyrics,
            )

    def parse_many(self, url):
        pages = self.get_all_pages(url)
        print(f"will scrape from: {pages}")
        for page in pages:
            yield from self.parse_one(page)

    def parse(self, url):
        if not self.validate(url):
            raise ValueError(f"unsupported {url=}")
        # FIXME: use parse_many after fixing the bug in get_all_pages
        yield from self.parse_one(url)
