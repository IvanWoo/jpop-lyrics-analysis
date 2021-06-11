from dataclasses import asdict, dataclass
from typing import Dict


@dataclass
class Jpop:
    title: str
    artist: str
    lyricist: str
    composer: str
    lyric_url: str
    lyrics: str

    def asdict(self) -> Dict:
        return asdict(self)

    def __str__(self) -> str:
        return f"Jpop(title='{self.title}', artist='{self.artist}')"
