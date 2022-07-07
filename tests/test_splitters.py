import pytest

from jpop_lyrics_analysis.splitters import SentenceSplitter


@pytest.fixture
def splitter():
    criterias = ["名詞", "動詞"]
    return SentenceSplitter(criterias)


def test_get_chunks(splitter):
    obj = splitter
    result = obj.get_chunks("そっと目を閉じれば 回り出すメリーゴーランド")
    expected_result = [
        ["そっと", "ソット", "ソット", "そっと", "副詞", "", "", "0"],
        ["目", "メ", "メ", "目", "名詞-普通名詞-一般", "", "", "1"],
        ["を", "オ", "ヲ", "を", "助詞-格助詞", "", "", ""],
        ["閉じれ", "トジレ", "トジル", "閉じる", "動詞-一般", "上一段-ザ行", "仮定形-一般", "2"],
        ["ば", "バ", "バ", "ば", "助詞-接続助詞", "", "", ""],
        ["回り", "マワリ", "マワル", "回る", "動詞-非自立可能", "五段-ラ行", "連用形-一般", "0"],
        ["出す", "ダス", "ダス", "出す", "動詞-非自立可能", "五段-サ行", "連体形-一般", "1"],
        [
            "メリーゴーランド",
            "メリーゴーランド",
            "メリーゴーランド",
            "メリーゴーランド-merry-go-round",
            "名詞-普通名詞-一般",
            "",
            "",
            "4",
        ],
    ]
    assert result == expected_result


def test_extract(splitter):
    obj = splitter
    result = obj.extract("そっと目を閉じれば 回り出すメリーゴーランド")
    expected_result = ["目", "閉じる", "回る", "出す", "メリーゴーランド-merry-go-round"]
    assert result == expected_result
