# Standard library
from typing import Tuple

# Local libraries
from lib.wordSpaces.CooccurrenceWordSpace import CooccurrenceWordSpace
from lib.utils.DataReader import DataReader
from lib.dataStructures.CooccurrenceContextWord import CooccurrenceContextWord
from lib.dataStructures.WordProps import WordProps
from lib.dataStructures.WordWithProps import WordWithProps
from lib.utils.SerialiseClassObjectToJson import SerialiseClassObjectToJson


class CooccurrenceResponseHandler:
    def __init__(self, dataReader: DataReader):
        self.__wordSpace = CooccurrenceWordSpace(dataReader)

    def handle(self, wordValue: str, contextWords: Tuple[str], normalize: bool):
        primaryWord = self.__wordSpace.getWordObj(wordValue)

        cooccurrenceContextWords = []
        for contextWordValue in contextWords:
            contextWord = self.__wordSpace.getWordObj(contextWordValue)
            data = self.__wordSpace.getCooccurenceData(wordValue, contextWordValue, normalize)

            cooccurrenceContextWords.append(CooccurrenceContextWord(contextWord, data))

        wordProps = WordProps()
        wordProps.setCooccurenceContextWords(cooccurrenceContextWords)

        result = WordWithProps(primaryWord, wordProps)

        serialisedObj = SerialiseClassObjectToJson(result)
        return serialisedObj.json
