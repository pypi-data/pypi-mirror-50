from lib.dataStructures.Word import Word
from lib.dataStructures.synonymNetwork.SynonymNetwork import SynonymNetwork


class SynonymNetworkResponse:
    def __init__(self, primaryWord: Word, synonymNetwork: SynonymNetwork):
        self.primaryWord = primaryWord
        self.synonymNetwork = synonymNetwork
