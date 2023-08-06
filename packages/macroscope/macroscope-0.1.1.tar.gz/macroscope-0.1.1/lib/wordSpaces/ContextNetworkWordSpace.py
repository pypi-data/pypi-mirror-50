# External libraries
from numpy import array, log, isnan, sqrt, seterr
from pandas import DataFrame, options
from scipy import sparse
from networkx import Graph
import community

# Standard library
from heapq import nlargest
from typing import List

# Local libraries
from lib.utils.DataReader import DataReader, ContextNetworkData
from lib.dataStructures.Word import Word
from lib.enums import ContextNetworkMethod
from lib.dataStructures.contextNetwork.ContextNetwork import ContextNetwork
from lib.dataStructures.contextNetwork.ContextNetworkNode import ContextNetworkNode
from lib.dataStructures.contextNetwork.ContextNetworkEdge import ContextNetworkEdge

# TODO: This entire file needs a massive refactor
# Possibly going to need detailed instructions on how calculations should be done
# contact li

# TODO: THESE WARNING SUPPRESSIONS NEEDS TO BE REMOVED AND LINES CAUSING THEM FIXED
# The following line suppresses the warning when executing coo['PMI'][coo['PMI'] <= 0] = 0
options.mode.chained_assignment = None  # default='warn'

# https://docs.scipy.org/doc/numpy/reference/generated/numpy.seterr.html
# https://stackoverflow.com/questions/15933741/how-do-i-catch-a-numpy-warning-like-its-an-exception-not-just-for-testing
seterr(divide='ignore', invalid='ignore')
# ----------------------------------------------------------------------------------------


class TempNode:
    def __init__(self, word: Word, size: int):
        self.word = word
        self.size = size


class TempNodes:
    def __init__(self):
        self.indices = []
        self.values = []
        self.sizes = []

    def add(self, node: TempNode):
        self.indices.append(node.word.index)
        self.values.append(node.word.value)
        self.sizes.append(node.size)


class ContextNetworkWordSpace:
    def __init__(self, dataReader: DataReader):
        self.__dataReader = dataReader

        self.__cor_size_K = None

        # for __loadData
        self.__data: ContextNetworkData = None
        self.__year = None

    def getWordObj(self, wordValue: str, year: int):
        #  TODO: cache already indexed words?
        self.__loadData(year)

        return Word(self.__data.vocab.index(wordValue), wordValue)

    def plotContextNetwork(
        self,
        wordValue: str,
        year: int,
        w_pmi: float,  # contextRelevance
        nodeSize: int,  # maximumNodes
        e_PMI: float,  # contextCohesiveness
        pmi_threshold: float,  # wordRelevance
        D: int,  # minimumEdges
        cap: int,  # displayNodes
        method: ContextNetworkMethod
    ):
        # w_pmi: First step: assign value to each selected words based on its relation with the target word.
        # w_pmi * PMI + (1-w_pmi) * cor       (cor is short for correlation?)
        # nodeSize: get top n (n=nodeSize) most relevant words based on w_pmi

        # pmi_threshold: Second step: remove edges if pmi is less than pmi_threshold

        # e_PMI: Third step: In the network, each nodes is re-evaluated based on its connections wih other nodes:
        # e_PMI* network_df.PMI/max(network_df.PMI) + (1-e_PMI)* network_df.co_occur/max(network_df.co_occur)

        # D: remove nodes if degree is less than D
        # cap: total number of words included in words exceed cap threshold

        # --------------- Step 1.load data --------------------------
        self.__loadData(year)

        primaryWord = self.getWordObj(wordValue, year)

        combined_i = self.__setCombinedI(primaryWord.index)
        year_i_freq = self.__getYearIFrequency(year)
        word_freq = year_i_freq[primaryWord.index]  # number of times word appears
        lexicon_size_year_i = self.__data.sumYear[str(year)]  # lexicon size of the year

        # TODO: what are cor and PMI? - contact li
        # --------------- Step 2: get cor and PMI between each word and target word: cor(x_i, risk) and PMI (x_i, risk)
        PMI = log(
            (combined_i[:50000]/lexicon_size_year_i) /
            ((word_freq/lexicon_size_year_i) *
             (year_i_freq[:50000]/lexicon_size_year_i))
        )

        # Convert unwanted ranges to 0
        PMI[PMI <= 0] = 0
        PMI[PMI > 20] = 0
        PMI[isnan(PMI)] = 0

        cor = log(combined_i)

        PMI = PMI/max(PMI)
        cor = cor/max(cor)  # after taking log of count, normalize between 0-1

        relevance_nodes = w_pmi * PMI + (1 - w_pmi) * cor

        # --------------- Step3: 1st Screen. Reduce number of nodes ----------------------------
        nodeData = nlargest(nodeSize, zip(relevance_nodes, list(range(0, 50000))))
        nodeSizes = nlargest(nodeSize, zip(relevance_nodes, combined_i))

        nodes = TempNodes()
        for i in list(range(0, nodeSize)):
            # TODO: score is not being used - what is it and why is it not being used? 
            score, wordIndex = nodeData[i]
            _wordValue = self.__data.vocab[wordIndex]
            _, size = nodeSizes[i]

            word = Word(wordIndex, _wordValue)
            node = TempNode(word, size)
            nodes.add(node)
        del nodeData, nodeSizes

        # set for key words PMI and cor vale
        # TODO: must be a more efficient data structure for doing this
        if primaryWord.value in nodes.values:
            nodes.sizes[nodes.values.index(primaryWord.value)] = max(nodes.sizes)
        else:
            size = max(nodes.sizes)
            node = TempNode(primaryWord, size)
            nodes.add(node)

        nodes.sizes /= lexicon_size_year_i

        # TODO: what is this? rename?
        self.__cor_size_K = {key: value for key, value in zip(nodes.values, nodes.sizes)}

        # --------------- Step 4. prepare edges ---------------
        # reduce matrix to 500*500

        # TODO: what is this? rename?
        tempData = self.__data.sparseCsrMatrix[nodes.indices, :][:, nodes.indices]
        tempData = tempData.transpose() + tempData

        # Return a Coordinate (coo) representation of the Compresses-Sparse-Column (csc) matrix.
        coo = sparse.triu(tempData.tocoo(copy=False), k=1)

        # Access `row`, `col` and `data` properties of coo matrix.
        coo = DataFrame({
            'word1': coo.row,
            'word2': coo.col,
            'co_occur_count': coo.data
        })[['word1', 'word2', 'co_occur_count']].sort_values(['word1', 'word2'])

        coo = coo[coo.co_occur_count >= 10]
        coo = coo.reset_index(drop=True)

        convert_index = {
            key: value for key, value in zip(range(0, len(nodes.indices)), nodes.indices)
        }

        coo.word1 = [convert_index.get(i) for i in coo.word1]
        coo.word2 = [convert_index.get(i) for i in coo.word2]

        # compute PMI
        p_w1 = year_i_freq[coo.word1.tolist()]/lexicon_size_year_i
        p_w2 = year_i_freq[coo.word2.tolist()]/lexicon_size_year_i
        p_w1_w2 = array(coo.co_occur_count)/lexicon_size_year_i  # (p(a,b))
        tempPMI = log(p_w1_w2/(p_w1*p_w2))

        # network_df = coo.copy()
        coo['PMI'] = tempPMI

        # TODO: This line is the line producing the warning when executing this file
        coo['PMI'][coo['PMI'] <= 0] = 0

        network_df = coo.sort_values('co_occur_count', ascending=False)

        network_df['word1'] = [self.__data.vocab[i] for i in network_df.word1]
        network_df['word2'] = [self.__data.vocab[i] for i in network_df.word2]

        # Trim edges based on PMI
        network_df = network_df[network_df.PMI >= pmi_threshold]

        # Get edge_score
        network_df['co_occur'] = log(network_df.co_occur_count)
        network_df['edge_score'] = e_PMI * network_df.PMI / \
            max(network_df.PMI) + (1 - e_PMI) * \
            network_df.co_occur/max(network_df.co_occur)
        network_df.sort_values(by='edge_score', ascending=False)

        words = network_df.word1.tolist()+network_df.word2.tolist()
        edge_scores = network_df.edge_score.tolist()+network_df.edge_score.tolist()

        temp = DataFrame({'words': words, 'edge_scores': edge_scores})
        temp = temp.groupby('words', as_index=False).agg({'edge_scores': 'sum'})
        temp = temp.sort_values(by='edge_scores', ascending=False)
        keep = temp.words[:cap].tolist()
        # if wordValue not in keep:
        #     keep.append(word)
        del temp

        # Step 5. Prepare plot
        network_df = network_df.reset_index(drop=True)

        if method == ContextNetworkMethod.COR:
            network_df['co_occur'] = sqrt(network_df.co_occur)/60
        if method == ContextNetworkMethod.PMI:
            network_df['PMI'] = (network_df.PMI*network_df.PMI)/40

        G = Graph()

        _edges = []
        for i in range(network_df.shape[0]):
            _word1 = network_df.word1[i]
            _word2 = network_df.word2[i]
            _df = None

            if method == ContextNetworkMethod.COR:
                _df = network_df.co_occur[i]
            elif method == ContextNetworkMethod.PMI:
                _df = network_df.PMI[i]
            else:
                raise NotImplementedError("Method " + method + " not implemented")

            _edges.append(
                (_word1, _word2, _df)
            )

        G.add_weighted_edges_from(_edges)

        # remove nodes if connection is less D
        remove = [node for node, degree in G.degree() if degree < D]
        G.remove_nodes_from(remove)
        remove = [node for node, degree in G.degree() if degree <= 0]
        G.remove_nodes_from(remove)

        if len(G.nodes()) > cap:
            remove = [x for x in G.nodes() if x not in keep]
            G.remove_nodes_from(remove)
            remove = [node for node, degree in G.degree() if degree <= 1]
            G.remove_nodes_from(remove)

        nodes = self.__getNodes(G)
        edges = self.__getEdges(G)

        return ContextNetwork(nodes, edges)

    def __getNodes(self, graph: Graph) -> List[ContextNetworkNode]:
        nodeSizes = self.__calculateNodeSizes(graph)
        partition = self.__calculatePartition(graph)

        nodes = []
        for i, wordValue in enumerate(graph.nodes()):
            index = self.__data.vocab.index(wordValue)
            word = Word(index, wordValue)

            size = nodeSizes[i]
            group = partition.get(wordValue)

            nodes.append(ContextNetworkNode(word, size, group))

        return nodes

    def __calculateNodeSizes(self, graph: Graph) -> List[float]:
        nodesizes = [self.__cor_size_K.get(x) for x in graph.nodes()]
        try:
            nodesizes = 15*log((nodesizes/max(nodesizes)+1))
        except ValueError:
            raise Exception(
                '''
                Given your settings, the Context Network has no nodes.
                Adjust the Context Network settings
                (set Context Relevance, Context Cohesiveness or Individual World Relevance to a smaller value),
                making the node filtering less restrictive.
                '''
            )

        return nodesizes

    def __calculatePartition(self, graph: Graph):
        partition = None
        try:
            partition = community.community_louvain.best_partition(graph)
        except ValueError:
            raise Exception(
                '''
                Given your settings, the Context Network has no links.
                Adjust the Context Network settings to make them more inclusive.
                '''
            )

        return partition

    def __getEdges(self, graph: Graph) -> List[ContextNetworkEdge]:
        edges = []
        for source, target in graph.edges():
            weight = graph[source][target]['weight']
            edges.append(ContextNetworkEdge(source, target, weight))

        return edges

    # TODO: rename this, what is it? - contact li
    def __setCombinedI(self, wordIndex: int):
        front = self.__data.sparseCsrMatrix.getrow(wordIndex).toarray()
        back = self.__data.sparseCsrMatrix.getcol(wordIndex).toarray().transpose()

        combined = front + back

        return combined[0][0:50000]

    def __getYearIFrequency(self, year: int):
        year_i_freq = self.__data.kernelYearFrequency[:, year-1800]
        return year_i_freq[0:50000]

    def __loadData(self, year: int):
        if self.__data is not None and self.__year == year:
            return

        self.__data = self.__dataReader.getContextNetworkData(year)
        self.__year = year
