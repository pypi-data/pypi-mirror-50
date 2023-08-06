# External libraries
from numpy import argsort, array, sort

# Local libraries
from lib.utils.DataReader import DataReader, ContextChangeData
from lib.wordSpaces.ClosestWordSpace import ClosestWordSpace
from lib.enums import ClosestSearchMethod
from lib.dataStructures.Word import Word
from lib.dataStructures.contextChange.ContextChangeWord import ContextChangeWord


class ContextChangeWordSpace:
    def __init__(self, dataReader: DataReader):
        self.__dataReader = dataReader
        self.__closestWordSpace = ClosestWordSpace(dataReader)

        # TODO: add as cli option?
        self.__numberOfClosestWords = 100
        self.__closestMethod = ClosestSearchMethod.SVD

        # for __loadData
        self.__data: ContextChangeData = None
        self.__wordValue = None

    def getWordObj(self, wordValue: str):
        #  TODO: cache already indexed words?
        self.__loadData(wordValue)

        return Word(self.__data.vocab.index(wordValue), wordValue)

    def getContextChange(self, wordValue: str, startYear: int, endYear: int, k: int, increase: bool):
        if startYear >= endYear:
            raise ValueError("Start year: " + startYear + " must be before End year: " + endYear)

        self.__loadData(wordValue)

        oldIndices = self.__getIndices(wordValue, startYear)
        newIndices = self.__getIndices(wordValue, endYear)

        # TODO: find out why this is list(set(..... - what difference does it make to simply oldIndices + newIndices
        index_o = list(set(oldIndices + newIndices))
        # index_o = oldIndices + newIndices
        # ----------------------------------------------------------------------------------------------------------

        old = self.__getArrayData(wordValue, startYear)
        new = self.__getArrayData(wordValue, endYear)

        oldArray = old.toarray()[:, index_o]
        newArray = new.toarray()[:, index_o]

        dif = []
        if increase:
            dif = newArray - oldArray
        else:
            dif = oldArray - newArray

        order = argsort(-dif[0])
        wordIndeces = array(index_o)[order][:k]

        dif = sort(-dif)
        dif = dif[0, :k]

        contextChangeWords = []
        for i, wordIndex in enumerate(wordIndeces):
            wordValue = self.__data.vocab[wordIndex]

            word = Word(int(wordIndex), wordValue)
            wordDif = float(dif[i])

            contextChangeWord = ContextChangeWord(word, wordDif)
            contextChangeWords.append(contextChangeWord)

        return contextChangeWords

    def __loadData(self, wordValue):
        # TODO: cache loaded data
        if self.__data is not None and self.__wordValue == wordValue:
            return

        self.__data = self.__dataReader.getContextChangeData(wordValue)
        self.__wordValue = wordValue

    def __getIndices(self, wordValue: str, year: int):
        closestWords = self.__closestWordSpace.getClosestWords(
            wordValue,
            year,
            self.__numberOfClosestWords,
            self.__closestMethod
        )

        indices = [self.__data.vocab.index(w.word.value) for w in closestWords]

        return indices

    def __getArrayData(self, wordValue: str, year: int):
        # Not sure what this function does - but functionality was repeated so I extracted it into a function

        self.__loadData(wordValue)
        sumYear = self.__data.sumYear[str(year)]
        return self.__data.sparseCsrMatrix.getrow(year - 1700)/sumYear
