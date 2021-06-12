import pytest

from jpop_lyrics_analysis.splitters import SentenceSplitter


@pytest.fixture
def splitter():
    criterias = ["名詞-一般", "動詞-自立", "名詞-代名詞-一般"]
    return SentenceSplitter(criterias)


def test_get_chunks(splitter):
    obj = splitter
    result = obj.get_chunks("そっと目を閉じれば 回り出すメリーゴーランド")
    expected_result = [
        ["そっと", "ソット", "そっと", "副詞-一般", "", ""],
        ["目", "メ", "目", "名詞-一般", "", ""],
        ["を", "ヲ", "を", "助詞-格助詞-一般", "", ""],
        ["閉じれ", "トジレ", "閉じる", "動詞-自立", "一段", "仮定形"],
        ["ば", "バ", "ば", "助詞-接続助詞", "", ""],
        ["回り", "マワリ", "回り", "名詞-一般", "", ""],
        ["出す", "ダス", "出す", "動詞-自立", "五段・サ行", "基本形"],
        ["メリーゴーランド", "メリーゴーランド", "メリーゴーランド", "名詞-一般", "", ""],
    ]
    assert result == expected_result


def test_extract(splitter):
    obj = splitter
    result = obj.extract("そっと目を閉じれば 回り出すメリーゴーランド")
    expected_result = ["目", "閉じる", "回り", "出す", "メリーゴーランド"]
    assert result == expected_result
