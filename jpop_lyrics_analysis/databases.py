import sqlite3

from jpop_lyrics_analysis.config import SQLITE_ADDRESS
from jpop_lyrics_analysis.models import Jpop

TABLE_NAME = "jpop"


class Sqlite:
    def __init__(self):
        self.connection = sqlite3.connect(SQLITE_ADDRESS, isolation_level=None)
        self.cursor = self.connection.cursor()
        self._init_db()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def _init_db(self):
        self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME}
            (title text, artist text, lyricist text, composer text, lyric_url text, lyrics text)
            """
        )

    def _insert(self, title, artist, lyricist, composer, lyric_url, lyrics):
        if not lyrics:
            raise ValueError("lyrics can not be empty")
        self.cursor.execute(
            f"INSERT INTO {TABLE_NAME} VALUES "
            + str((title, artist, lyricist, composer, lyric_url, lyrics))
        )

    def is_exist(self, title, artist):
        self.cursor.execute(
            f"SELECT title FROM {TABLE_NAME} WHERE title=? AND artist=?",
            (title, artist),
        )
        return self.cursor.fetchone() is not None

    def insert(self, jpop: Jpop):
        self._insert(**jpop.asdict())
        print(f"INSERTED {jpop} into the database")

    def artists(self):
        self.cursor.execute(f"SELECT DISTINCT artist FROM {TABLE_NAME}")
        return [x[0] for x in self.cursor.fetchall()]

    def lyrics_by_artist(self, artist):
        stream = self.cursor.execute(
            f"SELECT lyrics FROM {TABLE_NAME} WHERE artist = '{artist}' ORDER BY title"
        )
        for lyrics in stream:
            yield lyrics[0]
