# Standard library
from typing import Tuple

# Local libraries
from lib.wordSpaces.ContextChangeWordSpace import ContextChangeWordSpace
from lib.utils.SerialiseClassObjectToJson import SerialiseClassObjectToJson
from lib.dataStructures.WordProps import WordProps
from lib.dataStructures.WordWithProps import WordWithProps


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

            wordProps = WordProps()
            wordProps.setContextChangeWords(contextWords)

            primaryWords.append(WordWithProps(primaryWord, wordProps))

        serialisedObj = SerialiseClassObjectToJson(primaryWords)
        return serialisedObj.json
