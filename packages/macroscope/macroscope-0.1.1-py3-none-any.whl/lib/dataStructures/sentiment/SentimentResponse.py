from typing import List
from lib.dataStructures.Word import Word
from lib.dataStructures.Coord import Coord


class SentimentResponse:
    def __init__(self, primaryWord: Word, sentimentCoords: List[Coord]):
        self.primaryWord = primaryWord
        self.sentimentCoords = sentimentCoords
