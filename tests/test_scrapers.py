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
            title="Akimahen打ち落とされ傘を伝って",
            artist="BAND-MAIKO",
            lyricist="鳩子",
            composer="BAND-MAID",
            lyric_url="https://www.uta-net.com/song/265467/",
            lyrics=None,
        ),
        Jpop(
            title="ansanCheck me out ねぇそっと",
            artist="BAND-MAIKO",
            lyricist="鳩子",
            composer="BAND-MAID",
            lyric_url="https://www.uta-net.com/song/265468/",
            lyrics=None,
        ),
        Jpop(
            title="祇園町おこしやすおおきに",
            artist="BAND-MAIKO",
            lyricist="鳩子",
            composer="BAND-MAID",
            lyric_url="https://www.uta-net.com/song/265465/",
            lyrics=None,
        ),
        Jpop(
            title="secret MAIKO lips全身全霊嫌な世界やわぁ",
            artist="BAND-MAIKO",
            lyricist="鳩子",
            composer="BAND-MAID",
            lyric_url="https://www.uta-net.com/song/265471/",
            lyrics=None,
        ),
        Jpop(
            title="すくりーみんぐ間違っていたって無視できひん",
            artist="BAND-MAIKO",
            lyricist="鳩子",
            composer="BAND-MAID",
            lyric_url="https://www.uta-net.com/song/265466/",
            lyrics=None,
        ),
        Jpop(
            title="虎 and 虎もうあきまへんえ呟く",
            artist="BAND-MAIKO",
            lyricist="鳩子",
            composer="BAND-MAID",
            lyric_url="https://www.uta-net.com/song/265470/",
            lyrics=None,
        ),
        Jpop(
            title="YOLOSIOSU叶わへん言葉すべてあんさんの",
            artist="BAND-MAIKO",
            lyricist="鳩子",
            composer="BAND-MAID",
            lyric_url="https://www.uta-net.com/song/265469/",
            lyrics=None,
        ),
    ]
