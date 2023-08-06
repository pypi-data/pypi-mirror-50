# Standard library
from typing import List

# Local libraries
from lib.utils.DataReader import DataReader, FrequencyData
from lib.dataStructures.Coord import Coord
from lib.dataStructures.FrequencyCoords import FrequencyCoords
from lib.dataStructures.Word import Word


class FrequencyWordSpace:
    def __init__(self, dataReader: DataReader):
        self.__dataReader = dataReader

        self.__data: FrequencyData = None

    def getWordObj(self, wordValue: str):
        #  TODO: cache already indexed words?
        self.__loadData()

        return Word(self.__data.vocab.index(wordValue), wordValue)

    def getFrequencyCoords(
        self,
        wordValue: str,
        matchFullWord: bool,
        matchStart: bool,
        matchMiddle: bool,
        matchEnd: bool
    ):
        self.__loadData()

        fullWordCoords = []
        if matchFullWord:
            indices = self.__data.vocab.index(wordValue)
            fullWordCoords = self.__getCoords(indices)

        startCoords = []
        if matchStart:
            indices = []
            for x in self.__data.vocab:
                if x.startswith(wordValue):
                    index = self.__data.vocab.index(x)
                    indices.append(index)

            startCoords = self.__getCoords(indices)

        middleCoords = []
        if matchMiddle:
            indices = []
            for x in self.__data.vocab:
                if wordValue in x:
                    index = self.__data.vocab.index(x)
                    indices.append(index)

            middleCoords = self.__getCoords(indices)

        endCoords = []
        if matchEnd:
            indices = []
            for x in self.__data.vocab:
                if x.endswith(wordValue):
                    index = self.__data.vocab.index(x)
                    indices.append(index)

            endCoords = self.__getCoords(indices)

        return FrequencyCoords(fullWordCoords, startCoords, middleCoords, endCoords)

    def __getCoords(self, indices) -> List[Coord]:
        frequencyArray = self.__data.kernelYearFrequency[indices, ]/self.__data.sumYear[None, :]
        frequencyValues = frequencyArray.sum(axis=0)

        year = 1800
        coords = []
        for value in frequencyValues:
            coord = Coord(year, value)
            coords.append(coord)
            year += 1

        return coords

    def __loadData(self):
        if self.__data is not None:
            return

        self.__data = self.__dataReader.getFrequencyData()
