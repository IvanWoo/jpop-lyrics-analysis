from jpop_lyrics_analysis.models import Jpop
from jpop_lyrics_analysis.scrapers import UtaNet


def test_utanet__parse_one(requests_mock):
    target_url = "https://www.uta-net.com/artist/26425/"
    with open("tests/data/utanet_parse_one.html", "r") as f:
        html = f.read()
        requests_mock.get(target_url, text=html)

    utanet = UtaNet()
    assert list(utanet.parse_one(target_url)) == [
        Jpop(
            title="Akimahen",
            artist="BAND-MAIKO",
            lyricist="鳩子",
            composer="BAND-MAID",
            lyric_url="https://www.uta-net.com/song/265467/",
            lyrics=None,
        ),
        Jpop(
            title="ansan",
            artist="BAND-MAIKO",
            lyricist="鳩子",
            composer="BAND-MAID",
            lyric_url="https://www.uta-net.com/song/265468/",
            lyrics=None,
        ),
        Jpop(
            title="祇園町",
            artist="BAND-MAIKO",
            lyricist="鳩子",
            composer="BAND-MAID",
            lyric_url="https://www.uta-net.com/song/265465/",
            lyrics=None,
        ),
        Jpop(
            title="secret MAIKO lips",
            artist="BAND-MAIKO",
            lyricist="鳩子",
            composer="BAND-MAID",
            lyric_url="https://www.uta-net.com/song/265471/",
            lyrics=None,
        ),
        Jpop(
            title="すくりーみんぐ",
            artist="BAND-MAIKO",
            lyricist="鳩子",
            composer="BAND-MAID",
            lyric_url="https://www.uta-net.com/song/265466/",
            lyrics=None,
        ),
        Jpop(
            title="虎 and 虎",
            artist="BAND-MAIKO",
            lyricist="鳩子",
            composer="BAND-MAID",
            lyric_url="https://www.uta-net.com/song/265470/",
            lyrics=None,
        ),
        Jpop(
            title="YOLOSIOSU",
            artist="BAND-MAIKO",
            lyricist="鳩子",
            composer="BAND-MAID",
            lyric_url="https://www.uta-net.com/song/265469/",
            lyrics=None,
        ),
    ]


def test_utanet__next_page(requests_mock):
    mock_data = [
        ("https://www.uta-net.com/artist/39/0/1/", "tests/data/utanet_curr_page.html"),
        ("https://www.uta-net.com/artist/39/0/2/", "tests/data/utanet_next_page.html"),
    ]
    for url, html_file in mock_data:
        with open(html_file, "r") as f:
            html = f.read()
            requests_mock.get(url, text=html)

    curr_page, next_page = mock_data[0][0], mock_data[1][0]
    utanet = UtaNet()
    assert utanet.next_page(curr_page) == next_page
    assert utanet.next_page(next_page) is None
