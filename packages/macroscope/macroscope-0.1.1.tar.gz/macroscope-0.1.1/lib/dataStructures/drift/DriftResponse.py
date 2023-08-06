from lib.dataStructures.Word import Word
from lib.dataStructures.drift.SemanticDriftPoints import SemanticDriftPoints


class DriftResponse:
    def __init__(self, primaryWord: Word, semanticDrift: SemanticDriftPoints):
        self.primaryWord = primaryWord
        self.semanticDrift = semanticDrift
