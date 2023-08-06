# Local libraries
from lib.wordSpaces.SynonymNetworkWordSpace import SynonymNetworkWordSpace
from lib.utils.DataReader import DataReader
from lib.dataStructures.WordProps import WordProps
from lib.dataStructures.WordWithProps import WordWithProps
from lib.utils.SerialiseClassObjectToJson import SerialiseClassObjectToJson


class SynonymNetworkResponseHandler:
    def __init__(self, dataReader: DataReader):
        self.__wordSpace = SynonymNetworkWordSpace(dataReader)

    def handle(self, wordValue: str, year: int, synonymsPerTarget: int, similarityThreshold: float):
        primaryWord = self.__wordSpace.getWordObj(wordValue, year)

        synonymNetwork = self.__wordSpace.plotSynonymNetwork(wordValue, year, synonymsPerTarget, similarityThreshold)

        wordProps = WordProps()
        wordProps.setSynonymNetwork(synonymNetwork)

        result = WordWithProps(primaryWord, wordProps)

        serialisedObj = SerialiseClassObjectToJson(result)
        return serialisedObj.json
