# Standard library
from typing import Tuple

# Local libraries
from lib.wordSpaces.ContextChangeWordSpace import ContextChangeWordSpace
from lib.utils.SerialiseClassObjectToJson import SerialiseClassObjectToJson
from lib.dataStructures.contextChange.ContextChangeResponse import ContextChangeResponse


class ContextChangeResponseHandler:
    def __init__(self, dataReader):
        self.__wordSpace = ContextChangeWordSpace(dataReader)

    def handle(
        self,
        wordValues: Tuple[str],
        startYear: int,
        endYear: int,
        k: int,
        increase: bool
    ):
        primaryWords = []
        for wordValue in wordValues:
            primaryWord = self.__wordSpace.getWordObj(wordValue)
            contextWords = self.__wordSpace.getContextChange(wordValue, startYear, endYear, k, increase)

            primaryWords.append(ContextChangeResponse(primaryWord, contextWords))

        serialisedObj = SerialiseClassObjectToJson(primaryWords)
        return serialisedObj.json
