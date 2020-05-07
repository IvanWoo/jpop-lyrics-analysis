import argparse
import sqlite3

import MeCab


class SentenceSplit:
    def __init__(self, data_base):
        self.connection = sqlite3.connect(data_base)
        self.cursor = self.connection.cursor()
        self.splitter = MeCab.Tagger("-Ochasen")

    def _extract_word_by(self, criterias, lyrics):
        """
        # https://gist.github.com/ikegami-yukino/68a741ef854de68871cc#file-parse_vs_parsetonode-ipynb
        :param criterias: list
        :param lyrics: string
        :return: words separated by space
        """
        target_words = []
        for chunk in self.splitter.parse(lyrics).splitlines()[:-1]:
            chunks = chunk.split("\t")
            (surface, feature) = chunks[2], chunks[3]
            # print(feature)
            for criteria in criterias:
                if feature.startswith(criteria):
                    target_words.append(surface)
                    break
        return " ".join(target_words)

    def get_words_feed(self, artist, words_cloud_txt, criterias):
        with open(words_cloud_txt, "w") as text_file:
            for lyrics in self.cursor.execute(
                f"SELECT lyrics FROM jpop WHERE artist = '{artist}' ORDER BY title"
            ):
                target_words = self._extract_word_by(criterias, lyrics[0])
                text_file.write(str(target_words))
        print(words_cloud_txt + " is generated")


def main():
    parser = argparse.ArgumentParser(description="analyze jpop lyrics")
    # eg: 私立恵比寿中学
    parser.add_argument("-a", "--artist", type=str)
    args = parser.parse_args()

    # TODO: Try different extraction criteria.
    criterias = ["名詞-一般", "動詞-自立", "名詞-代名詞-一般"]
    db = SentenceSplit("jpop-lyrics.db")
    db.get_words_feed(args.artist, "word-cloud-feed.txt", criterias)
    return


if __name__ == "__main__":
    main()
