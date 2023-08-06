# Standard library
from typing import List

# Local libraries
from lib.dataStructures.Coord import Coord


class FrequencyCoords:
    def __init__(self, fullWordCoords: List[Coord], startCoords: List[Coord], middleCoords: List[Coord], endCoords: List[Coord]):
        self.matchFullWord = fullWordCoords
        self.matchStart = startCoords
        self.matchMiddle = middleCoords
        self.matchEnd = endCoords
