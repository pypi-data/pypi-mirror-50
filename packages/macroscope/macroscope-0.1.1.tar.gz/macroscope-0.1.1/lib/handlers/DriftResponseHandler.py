# Local libraries
from lib.wordSpaces.DriftWordSpace import DriftWordSpace
from lib.utils.DataReader import DataReader
from lib.utils.SerialiseClassObjectToJson import SerialiseClassObjectToJson
from lib.dataStructures.drift.DriftResponse import DriftResponse


class DriftResponseHandler:
    def __init__(self, dataReader: DataReader):
        self.__wordSpace = DriftWordSpace(dataReader)

    def handle(
        self,
        wordValue: str,
        startYear: int,
        endYear: int,
        numberOfYearsInInterval: int,
        numberOfClosestWords: int
    ):
        primaryWord = self.__wordSpace.getWordObj(wordValue, startYear, endYear)
        semanticDriftPoints = self.__wordSpace.getSemanticDriftPoints(
            wordValue,
            startYear,
            endYear,
            numberOfYearsInInterval,
            numberOfClosestWords
        )

        result = DriftResponse(primaryWord, semanticDriftPoints)

        serialisedObj = SerialiseClassObjectToJson(result)
        return serialisedObj.json
