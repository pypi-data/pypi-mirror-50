# Local libraries
from lib.wordSpaces.ContextNetworkWordSpace import ContextNetworkWordSpace
from lib.utils.DataReader import DataReader
from lib.dataStructures.contextNetwork.ContextNetworkResponse import ContextNetworkResponse
from lib.utils.SerialiseClassObjectToJson import SerialiseClassObjectToJson
from lib.enums import ContextNetworkMethod


class ContextNetworkResponseHandler:
    def __init__(self, dataReader: DataReader):
        self.__wordSpace = ContextNetworkWordSpace(dataReader)

    def handle(
        self,
        wordValue: str,
        year: int,
        contextRelevance: float,
        maximumNodes: int,
        contextCohesiveness: float,
        wordRelevance: float,
        minimumEdges: int,
        displayNodes: int,
        method: ContextNetworkMethod
    ):
        primaryWord = self.__wordSpace.getWordObj(wordValue, year)

        contextNetwork = self.__wordSpace.plotContextNetwork(
            wordValue,
            year,
            contextRelevance,
            maximumNodes,
            contextCohesiveness,
            wordRelevance,
            minimumEdges,
            displayNodes,
            method
        )

        result = ContextNetworkResponse(primaryWord, contextNetwork)

        serialisedObj = SerialiseClassObjectToJson(result)
        return serialisedObj.json
