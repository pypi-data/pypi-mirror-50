from lib.dataStructures.Word import Word


class ContextChangeWord:
    def __init__(self, word: Word, dif: float):
        self.word = word
        self.dif = dif
