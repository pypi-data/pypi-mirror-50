from typing import List
from lib.dataStructures.Word import Word
from lib.dataStructures.closest.ClosestWord import ClosestWord


class ClosestResponse:
    def __init__(self, primaryWord: Word, closestWords: List[ClosestWord]):
        self.primaryWord = primaryWord
        self.closestWords = closestWords
