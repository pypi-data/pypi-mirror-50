from lib.dataStructures.Word import Word
from lib.dataStructures.WordProps import WordProps


class WordWithProps:
    def __init__(self, word: Word, props: WordProps):
        self.word = word
        self.props = props
