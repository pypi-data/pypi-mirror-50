from typing import List
from lib.dataStructures.Word import Word
from lib.dataStructures.cooccurrence.CooccurrenceContextWord import CooccurrenceContextWord


class CooccurrenceResponse:
    def __init__(self, primaryWord: Word, cooccurrenceContextWords: List[CooccurrenceContextWord]):
        self.primaryWord = primaryWord
        self.cooccurrenceContextWords = cooccurrenceContextWords
