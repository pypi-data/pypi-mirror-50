# External libraries
from heapq import nlargest

# Standard library
from typing import List

# Local libraries
from lib.dataStructures.closest.ClosestWord import ClosestWord
from lib.utils.DataReader import DataReader, ClosestData
from lib.dataStructures.Word import Word
from lib.enums import ClosestSearchMethod


class ClosestWordSpace:
    def __init__(self, dataReader: DataReader):
        self.__dataReader = dataReader

        # for __loadData
        self.__data: ClosestData = None
        self.__method = None
        self.__year = None

    def getWordObj(self, wordValue: str, year: int, method: ClosestSearchMethod):
        #  TODO: cache already indexed words?
        self.__loadData(year, method)

        return Word(self.__data.vocab.index(wordValue), wordValue)

    def getClosestWords(
        self,
        wordValue: str,
        year: int,
        numberOfClosestWords: int,
        method: ClosestSearchMethod
    ) -> List[ClosestWord]:
        self.__loadData(year, method)

        primaryWord = self.getWordObj(wordValue, year, method)

        raw_scores_with_word_indices = self.__data.m.dot(self.__data.m[primaryWord.index, :])
        highest_scoring_words = nlargest(
            numberOfClosestWords + 1,
            zip(raw_scores_with_word_indices, range(0, self.__data.m.shape[0]))
        )

        highest_scoring_words.pop(0)  # Remove highest scoring word - as it is the primary word

        closestWords: List[ClosestWord] = []
        for _word in highest_scoring_words:
            score = _word[0]
            index = _word[1]
            value = self.__data.vocab[index]

            closestWords.append(ClosestWord(Word(index, value), score))

        return closestWords

    def __loadData(self, year: int, method: ClosestSearchMethod):
        # TODO: cache loaded data - store in hash table (dict) with key str(year_method)
        if self.__data is not None and self.__year == year and self.__method == method:
            return

        self.__data = self.__dataReader.getClosestData(year, method)
        self.__year = year
        self.__method = method
