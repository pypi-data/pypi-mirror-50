# Standard library
from typing import Tuple

# Local libraries
from lib.utils.DataReader import DataReader
from lib.wordSpaces.FrequencyWordSpace import FrequencyWordSpace
from lib.utils.SerialiseClassObjectToJson import SerialiseClassObjectToJson
from lib.dataStructures.WordProps import WordProps
from lib.dataStructures.WordWithProps import WordWithProps


class FrequencyResponseHandler:
    def __init__(self, dataReader: DataReader):
        self.__wordSpace = FrequencyWordSpace(dataReader)

    def handle(self, wordValues: Tuple[str], matchFullWord: bool, matchStart: bool, matchMiddle: bool, matchEnd: bool):
        primaryWords = []

        for wordValue in wordValues:
            primaryWord = self.__wordSpace.getWordObj(wordValue)
            frequencyCoords = self.__wordSpace.getFrequencyCoords(
                wordValue,
                matchFullWord,
                matchStart,
                matchMiddle,
                matchEnd
            )

            wordProps = WordProps()
            wordProps.setFrequencyCoords(frequencyCoords)

            primaryWords.append(WordWithProps(primaryWord, wordProps))

        serialisedObj = SerialiseClassObjectToJson(primaryWords)
        return serialisedObj.json
