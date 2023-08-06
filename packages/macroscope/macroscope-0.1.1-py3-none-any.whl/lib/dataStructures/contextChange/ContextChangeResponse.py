from typing import List
from lib.dataStructures.Word import Word
from lib.dataStructures.contextChange.ContextChangeWord import ContextChangeWord


class ContextChangeResponse:
    def __init__(self, primaryWord: Word, contextChangeWords: List[ContextChangeWord]):
        self.primaryWord = primaryWord
        self.contextChangeWords = contextChangeWords
