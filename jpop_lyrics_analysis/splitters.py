from typing import List

import MeCab


class SentenceSplitter:
    def __init__(self, criterias: List[str]):
        self.splitter = MeCab.Tagger("-Ochasen")
        self.criterias = criterias

    def get_chunks(self, content: str):
        chunks = self.splitter.parse(content).splitlines()[:-1]
        return [x.split("\t") for x in chunks]

    def extract(self, lyrics: str) -> List[str]:
        """
        https://gist.github.com/ikegami-yukino/68a741ef854de68871cc#file-parse_vs_parsetonode-ipynb
        """
        target_words = []
        chunks = self.get_chunks(lyrics)
        for chunk in chunks:
            (surface, feature) = chunk[2], chunk[3]
            for criteria in self.criterias:
                if feature.startswith(criteria):
                    target_words.append(surface)
                    break
        return target_words
