from typing import Set
import MeCab

from jpop_lyrics_analysis.databases import Sqlite


class SentenceSplitter:
    def __init__(self, criterias):
        self.splitter = MeCab.Tagger("-Ochasen")
        self.criterias = criterias

    def _extract_word_by(self, lyrics) -> Set:
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
            for criteria in self.criterias:
                if feature.startswith(criteria):
                    target_words.append(surface)
                    break
        return target_words

    def get_word_feed(self, artist):
        # TODO: use contextmanager for db
        db = Sqlite()
        feed = []
        for lyrics in db.lyrics_by_artist(artist):
            target_words = self._extract_word_by(lyrics)
            feed.extend(target_words)
        db.close()
        return feed
