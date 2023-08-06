# Standard library
from typing import Tuple

# Local libraries
from lib.wordSpaces.SentimentWordSpace import SentimentWordSpace
from lib.enums import SentimentPlotType
from lib.utils.DataReader import DataReader
from lib.utils.SerialiseClassObjectToJson import SerialiseClassObjectToJson
from lib.dataStructures.sentiment.SentimentResponse import SentimentResponse


class SentimentHandler:
    def __init__(self, dataReader: DataReader):
        self.__wordSpace = SentimentWordSpace(dataReader)

    def handle(self, wordValues: Tuple[str], plotType: SentimentPlotType):
        primaryWords = []

        for wordValue in wordValues:
            primaryWord = self.__wordSpace.getWordObj(wordValue, plotType)
            sentimentCoords = self.__wordSpace.getSentimentCoords(wordValue, plotType)

            primaryWords.append(SentimentResponse(primaryWord, sentimentCoords))

        serialisedObj = SerialiseClassObjectToJson(primaryWords)
        return serialisedObj.json
