# Local libraries
from lib.wordSpaces.DriftWordSpace import DriftWordSpace
from lib.utils.DataReader import DataReader
from lib.utils.SerialiseClassObjectToJson import SerialiseClassObjectToJson
from lib.dataStructures.WordProps import WordProps
from lib.dataStructures.WordWithProps import WordWithProps


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

        wordProps = WordProps()
        wordProps.setSemanticDriftPoints(semanticDriftPoints)

        wordWithProps = WordWithProps(primaryWord, wordProps)

        serialisedObj = SerialiseClassObjectToJson(wordWithProps)
        return serialisedObj.json
