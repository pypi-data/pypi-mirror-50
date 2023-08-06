# External libraries
from numpy import einsum
from scipy import sparse
from pandas import DataFrame
from networkx import Graph
import community

# Standard library
from typing import List

# Local libraries
from lib.utils.DataReader import DataReader, SynonymNetworkData
from lib.wordSpaces.ClosestWordSpace import ClosestWordSpace
from lib.dataStructures.closest.ClosestWord import ClosestWord
from lib.enums import ClosestSearchMethod
from lib.dataStructures.Word import Word
from lib.dataStructures.synonymNetwork.SynonymNetwork import SynonymNetwork
from lib.dataStructures.synonymNetwork.SynonymNetworkNode import SynonymNetworkNode
from lib.dataStructures.synonymNetwork.SynonymNetworkEdge import SynonymNetworkEdge


# TODO: check /embeddings-10-years folder has the same contents as /embeddings/10-years
# I don't think it does as i recieve an error when using /embeddings/10-years
# Rename /embeddings-10-years ??

# TODO: contact li about the difference between /embeddings-10-years and /embeddings/10-years
class SynonymNetworkWordSpace:
    def __init__(self, dataReader: DataReader):
        self.__dataReader = dataReader
        self.__closestWordSpace = ClosestWordSpace(dataReader)

        # TODO: add as cli option?
        self.__closestMethod = ClosestSearchMethod.SVD

        # for __loadData
        self.__data: SynonymNetworkData = None
        self.__year = None

    def getWordObj(self, wordValue: str, year: int):
        #  TODO: cache already indexed words?
        self.__loadData(year)

        return Word(self.__data.vocab.index(wordValue), wordValue)

    def plotSynonymNetwork(
        self,
        wordValue: str,
        year: int,
        synonymsPerTarget: int,  # k
        similarityThreshold: float  # minSim
    ):
        '''
        synonymsPerTarget: number of synonyms of each target word is included in the structure
        similarityThreshold: link if semantic similarity is larger than similarityThreshold
        '''

        self.__loadData(year)

        primaryWord = self.getWordObj(wordValue, year)

        # assign score as inf because it is the primary word
        primaryWordAsSynonym = ClosestWord(primaryWord, float('inf'))

        synonyms = []
        synonyms.append(primaryWordAsSynonym)
        synonyms += self.__closestWordSpace.getClosestWords(wordValue, year, synonymsPerTarget, self.__closestMethod)

        synonymIndices = []
        for synonym in synonyms:
            synonymIndices.append(synonym.word.index)

        word_embeddings = self.__data.m[synonymIndices, :]

        # construct similarity table, prepare for network plot
        sim_matrix = einsum('xj,yj->xy', word_embeddings, word_embeddings)

        # TODO: the following line has a typo - maRTix instead of maTRix.
        # The typo was in the original code written by li.
        # I have left it commented out to match the legacy response.
        # When uncommenting and fixing the typo it doesnt change the response, so it doesn't seem necessary.
        # contact li about this
        # ----------------------------------
        # sim_martix = triu(sim_matrix, k=1)
        # ----------------------------------

        coo = sparse.coo_matrix(sim_matrix)
        coo = sparse.triu(coo, k=1)

        coo = DataFrame({
            'word1': coo.row,
            'word2': coo.col,
            'value': coo.data
        })[['word1', 'word2', 'value']].sort_values(['word1', 'word2'])

        coo.word1 = [synonyms[i].word.value for i in coo.word1]
        coo.word2 = [synonyms[i].word.value for i in coo.word2]

        # select threshold of similarity value
        network_df = coo[coo.value >= similarityThreshold]

        # Plot
        G = Graph()

        # weight by similarity
        _edges = []
        for i in range(network_df.shape[0]):
            _edges.append(
                (network_df.word1.iloc[i], network_df.word2.iloc[i], network_df.value.iloc[i])
            )

        G.add_weighted_edges_from(_edges)

        # don't remove any nodes
        remove = [node for node, degree in G.degree() if degree <= 0]
        G.remove_nodes_from(remove)

        edges = self.__getEdges(G)
        nodes = self.__getNodes(G)

        return SynonymNetwork(nodes, edges)

    def __getNodes(self, graph: Graph) -> List[SynonymNetworkNode]:
        partition = self.__calculatePartition(graph)

        nodes = []
        for wordValue in graph.nodes():
            index = self.__data.vocab.index(wordValue)
            word = Word(index, wordValue)

            group = partition.get(wordValue)

            nodes.append(SynonymNetworkNode(word, group))

        return nodes

    def __calculatePartition(self, graph: Graph):
        partition = None
        try:
            partition = community.community_louvain.best_partition(graph)
            community.community_louvain.modularity(partition, graph)
        except ValueError:
            raise Exception(
                '''
                    Given your settings, the Synonym Network has no links.
                    Adjust the Synonym Network settings to make them more inclusive.
                '''
            )

        return partition

    def __getEdges(self, graph: Graph) -> List[SynonymNetworkEdge]:
        edges = []
        for source, target in graph.edges():
            weight = graph[source][target]['weight']
            edges.append(SynonymNetworkEdge(source, target, weight))

        return edges

    def __loadData(self, year: int):
        if self.__data is not None and self.__year == year:
            return

        self.__data = self.__dataReader.getSynonymNetworkData(year)
        self.__year = year
