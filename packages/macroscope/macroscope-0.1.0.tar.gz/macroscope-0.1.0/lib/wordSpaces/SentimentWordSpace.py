# External libraries
from numpy import transpose, isnan

# Standard library
from typing import List

# Local libraries
from lib.utils.DataReader import DataReader, SentimentData
from lib.enums import SentimentPlotType
from lib.dataStructures.Coord import Coord
from lib.dataStructures.Word import Word


class SentimentWordSpace:
    def __init__(self, dataReader: DataReader):
        self.__dataReader = dataReader

        # for __loadData
        self.__data: SentimentData = None
        self.__plotType = None

    def getWordObj(self, wordValue: str, plotType: SentimentPlotType):
        #  TODO: cache already indexed words?
        self.__loadData(plotType)

        return Word(self.__data.vocab.index(wordValue), wordValue)

    def getSentimentCoords(self, wordValue: str, plotType: SentimentPlotType) -> List[Coord]:
        self.__loadData(plotType)

        wordIndex = self.__data.vocab.index(wordValue)
        sentimentValues = transpose(self.__data.dataArray[wordIndex])

        # Convert nan value to 0
        sentimentValues[isnan(sentimentValues)] = 0

        year = 1800
        coords = []
        for value in sentimentValues:
            coord = Coord(year, value)
            coords.append(coord)
            year += 1

        return coords

    def __loadData(self, plotType: SentimentPlotType):
        # TODO: cache loaded data - store in hash table (dict) with key str(year_method)
        if self.__data is not None and self.__plotType == plotType:
            return

        self.__data = self.__dataReader.getSentimentData(plotType)
        self.__plotType = plotType
