# Standard library
from typing import Tuple

# Local libraries
from lib.utils.DataReader import DataReader
from lib.wordSpaces.FrequencyWordSpace import FrequencyWordSpace
from lib.utils.SerialiseClassObjectToJson import SerialiseClassObjectToJson
from lib.dataStructures.frequency.FrequencyResponse import FrequencyResponse


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

            primaryWords.append(FrequencyResponse(primaryWord, frequencyCoords))

        serialisedObj = SerialiseClassObjectToJson(primaryWords)
        return serialisedObj.json
