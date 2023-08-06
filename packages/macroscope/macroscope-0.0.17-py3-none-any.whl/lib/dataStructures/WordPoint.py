from lib.dataStructures.Word import Word
from lib.dataStructures.Coord import Coord


class WordPoint:
    def __init__(self, word: Word, coord: Coord):
        self.word = word
        self.coord = coord
