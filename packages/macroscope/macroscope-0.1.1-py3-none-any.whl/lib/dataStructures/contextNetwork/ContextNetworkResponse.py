from lib.dataStructures.Word import Word
from lib.dataStructures.contextNetwork.ContextNetwork import ContextNetwork


class ContextNetworkResponse:
    def __init__(self, primaryWord: Word, contextNetwork: ContextNetwork):
        self.primaryWord = primaryWord
        self.contextNetwork = contextNetwork
