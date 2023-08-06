from lib.dataStructures.Word import Word


class ContextNetworkNode:
    def __init__(self, word: Word, size: float, group: int):
        self.word = word
        self.size = size
        self.group = group
