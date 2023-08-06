# External libraries
from scipy import sparse

# Standard library
from typing import List

# Local libraries
from lib.utils.DataReader import DataReader, CooccurrenceData
from lib.dataStructures.Word import Word
from lib.dataStructures.cooccurrence.CooccurrenceDatumPoint import CooccurrenceDatumPoint


class CooccurrenceWordSpace:
    def __init__(self, dataReader: DataReader):
        self.__dataReader = dataReader

        # for __loadData
        self.__data: CooccurrenceData = None
        self.__wordValue = None

    def getWordObj(self, wordValue: str):
        #  TODO: cache already indexed words?
        self.__loadData(wordValue)

        return Word(self.__data.vocab.index(wordValue), wordValue)

    def getCooccurenceData(self, wordValue: str, contextWord: str, normalize: bool) -> List[CooccurrenceDatumPoint]:
        self.__loadData(wordValue)

        cor_occur = []

        wordIndex = self.__data.vocab.index(contextWord)
        columnData = self.__data.sparseCsrMatrix.getcol(wordIndex)

        # TODO: Not sure what these lines actually do - contact li
        denseMatrix = sparse.hstack([columnData]).todense()
        cor_occur = denseMatrix[(1800-1700):]
        # --------------------------------------------------

        if normalize:
            primaryWordIndex = self.__data.vocab.index(wordValue)
            kernel_year_freq_values = self.__data.kernelYearFrequency[primaryWordIndex, ][:, None]
            cor_occur = cor_occur/kernel_year_freq_values
        else:
            cor_occur = cor_occur/self.__data.sumYear[:, None]

        # .A1 flattens numpy arrays - https://stackoverflow.com/questions/3337301/numpy-matrix-to-array 
        frequencyValues = cor_occur.A1

        # Years upto, but not including, 2009
        years = list(range(1800, 2009))

        frequencyData = []
        for i, frequencyValue in enumerate(frequencyValues):
            year = years[i]
            datum = CooccurrenceDatumPoint(year, frequencyValue)
            frequencyData.append(datum)

        return frequencyData

    def __loadData(self, wordValue):
        # TODO: cache loaded data
        if self.__data is not None and self.__wordValue == wordValue:
            return

        self.__data = self.__dataReader.getCooccurrenceData(wordValue)
        self.__wordValue = wordValue
