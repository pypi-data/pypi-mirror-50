from lib.dataStructures.Word import Word
from lib.dataStructures.frequency.FrequencyCoords import FrequencyCoords


class FrequencyResponse:
    def __init__(self, primaryWord: Word, frequencyCoords: FrequencyCoords):
        self.primaryWord = primaryWord
        self.frequencyCoords = frequencyCoords
