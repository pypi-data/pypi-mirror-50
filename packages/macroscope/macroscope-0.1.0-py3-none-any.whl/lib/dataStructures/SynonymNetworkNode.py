from lib.dataStructures.Word import Word


class SynonymNetworkNode:
    def __init__(self, word: Word, group: int):
        self.word = word
        self.group = group
