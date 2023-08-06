# Standard library
from typing import Tuple

# Local libraries
from lib.wordSpaces.ClosestWordSpace import ClosestWordSpace
from lib.dataStructures.closest.ClosestResponse import ClosestResponse
from lib.utils.SerialiseClassObjectToJson import SerialiseClassObjectToJson
from lib.enums import ClosestSearchMethod
from lib.utils.DataReader import DataReader


class ClosestResponseHandler:
    def __init__(self, dataReader: DataReader):
        self.__wordSpace = ClosestWordSpace(dataReader)

    def handle(
        self,
        wordValues: Tuple[str],
        year: int,
        numberOfClosestWords: int = None,
        method: ClosestSearchMethod = None
    ):
        primaryWords = []
        for wordValue in wordValues:
            primaryWord = self.__wordSpace.getWordObj(wordValue, year, method)
            closestWords = self.__wordSpace.getClosestWords(wordValue, year, numberOfClosestWords, method)

            primaryWords.append(ClosestResponse(primaryWord, closestWords))

        serialisedObj = SerialiseClassObjectToJson(primaryWords)
        return serialisedObj.json
