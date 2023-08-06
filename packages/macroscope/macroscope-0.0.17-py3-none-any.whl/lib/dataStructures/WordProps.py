# Standard library
from typing import List

# Local libraries
from lib.dataStructures.ClosestWord import ClosestWord
from lib.dataStructures.ContextChangeWord import ContextChangeWord
from lib.dataStructures.CooccurrenceContextWord import CooccurrenceContextWord
from lib.dataStructures.SemanticDriftPoints import SemanticDriftPoints
from lib.dataStructures.Coord import Coord
from lib.dataStructures.FrequencyCoords import FrequencyCoords
from lib.dataStructures.ContextNetwork import ContextNetwork
from lib.dataStructures.SynonymNetwork import SynonymNetwork


class WordProps:
    def __init__(self):
        self.closestWords = None
        self.contextChangeWords = None
        self.cooccurrenceContextWords = None
        self.semanticDrift = None
        self.sentimentCoords = None
        self.frequencyCoords = None
        self.contextNetwork = None
        self.synonymNetwork = None

    def setClosestWords(self, closestWords: List[ClosestWord]):
        self.closestWords = closestWords

    def setContextChangeWords(self, contextChangeWords: List[ContextChangeWord]):
        self.contextChangeWords = contextChangeWords

    def setCooccurenceContextWords(self, cooccurrenceContextWords: List[CooccurrenceContextWord]):
        self.cooccurrenceContextWords = cooccurrenceContextWords

    def setSemanticDriftPoints(self, semanticDriftPoints: SemanticDriftPoints):
        self.semanticDrift = semanticDriftPoints

    def setSentimentCoords(self, sentimentCoords: List[Coord]):
        self.sentimentCoords = sentimentCoords

    def setFrequencyCoords(self, frequencyCoords: FrequencyCoords):
        self.frequencyCoords = frequencyCoords

    def setContextNetwork(self, contextNetwork: ContextNetwork):
        self.contextNetwork = contextNetwork

    def setSynonymNetwork(self, synonymNetwork: SynonymNetwork):
        self.synonymNetwork = synonymNetwork
