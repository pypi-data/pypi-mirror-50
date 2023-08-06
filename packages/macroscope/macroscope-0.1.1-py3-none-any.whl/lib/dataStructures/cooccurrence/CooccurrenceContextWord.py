from typing import List
from lib.dataStructures.Word import Word
from lib.dataStructures.cooccurrence.CooccurrenceDatumPoint import CooccurrenceDatumPoint


class CooccurrenceContextWord:
    def __init__(self, word: Word, data: List[CooccurrenceDatumPoint]):
        self.word = word
        self.data = data
