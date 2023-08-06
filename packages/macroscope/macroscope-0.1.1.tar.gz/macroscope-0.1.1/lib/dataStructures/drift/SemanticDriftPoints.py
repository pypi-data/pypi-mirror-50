from lib.dataStructures.drift.YearPoint import YearPoint
from lib.dataStructures.drift.WordPoint import WordPoint
from typing import List


class SemanticDriftPoints:
    def __init__(self, yearPoints: List[YearPoint], contextWordPoints: List[WordPoint]):
        self.yearPoints = yearPoints
        self.contextWordPoints = contextWordPoints
