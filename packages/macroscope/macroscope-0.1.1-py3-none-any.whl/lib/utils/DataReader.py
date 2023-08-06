# External libraries
from numpy import load
from sklearn import preprocessing
from pandas import read_pickle
from scipy import sparse

# Standard library
from typing import List

# Local libraries
from lib.enums import ClosestSearchMethod, SentimentPlotType
from lib.utils.roundToDecade import roundToDecade
from lib.dataStructures.Word import Word


# TODO: add types to data members
class ClosestData:
    def __init__(self, vocab, m):
        self.vocab = vocab
        self.m = m


class ContextChangeData:
    def __init__(self, vocab, sumYear, sparseCsrMatrix):
        self.vocab = vocab
        self.sumYear = sumYear
        self.sparseCsrMatrix = sparseCsrMatrix


class CooccurrenceData:
    def __init__(self, vocab, sumYear, kernelYearFrequency, sparseCsrMatrix):
        self.vocab = vocab
        self.sumYear = sumYear
        self.kernelYearFrequency = kernelYearFrequency
        self.sparseCsrMatrix = sparseCsrMatrix


class DriftData:
    def __init__(self, m_startYear, m_endYear, vocab):
        self.m_startYear = m_startYear
        self.m_endYear = m_endYear
        self.vocab = vocab


class SentimentData:
    def __init__(self, vocab, dataArray):
        self.vocab = vocab
        self.dataArray = dataArray


class FrequencyData:
    def __init__(self, vocab, sumYear, kernelYearFrequency):
        self.vocab = vocab
        self.sumYear = sumYear
        self.kernelYearFrequency = kernelYearFrequency


class ContextNetworkData:
    def __init__(self, vocab, sumYear, kernelYearFrequency, sparseCsrMatrix):
        self.vocab = vocab
        self.sumYear = sumYear
        self.kernelYearFrequency = kernelYearFrequency
        self.sparseCsrMatrix = sparseCsrMatrix


class SynonymNetworkData:
    def __init__(self, vocab, m):
        self.vocab = vocab
        self.m = m


# TODO: add return types for private member functions
class DataReader:
    # TODO: make generic data reader for all command services - Extract command specific functions into wordspace class?
    # TODO: Cache results? does caching work with click? How can this be done - store things in memory???
    # TODO: have option to print time taken to load data - figure out if this is truly the bottle neck
    def __init__(self, path: str):
        self.__path = path

    def getClosestData(self,  year: int, method: ClosestSearchMethod) -> ClosestData:
        vocab = self.__getClosestVocab(year, method)
        m = self.__getClosestMData(year, method)

        return ClosestData(vocab, m)

    def getContextChangeData(self, wordValue: str) -> ContextChangeData:
        vocab = self.__getVocab50k()
        sumYear = self.__getSumYear()
        sparseCsrMatrix = self.__get50kMatrixFrontSparseCsr(Word(vocab.index(wordValue), wordValue))
        return ContextChangeData(vocab, sumYear, sparseCsrMatrix)

    def getCooccurrenceData(self, wordValue: str) -> CooccurrenceData:
        vocab = self.__getVocab50k()
        sumYear = self.__getSumYear()
        kernelYearFrequency = self.__getKernelYearFrequency()
        sparseCsrMatrix = self.__get50kMatrixFrontSparseCsr(Word(vocab.index(wordValue), wordValue))
        return CooccurrenceData(vocab, sumYear, kernelYearFrequency, sparseCsrMatrix)

    def getDriftData(self, startYear: int, endYear: int, method: ClosestSearchMethod):
        m_startYear = self.__getClosestMData(startYear, method)
        m_endYear = self.__getClosestMData(endYear, method)

        vocab = self.__getClosestVocab(endYear, method)

        return DriftData(m_startYear, m_endYear, vocab)

    def getClosestMForYears(self, years: List[int], method: ClosestSearchMethod, use10YearsDir=False):
        m = {}
        for year in years:
            m[year] = self.__getClosestMData(year, method, use10YearsDir)

        return m

    def getSentimentData(self, plotType: SentimentPlotType):
        vocab = self.__getVocab50k()
        cacheSum = self.__getCacheSum()

        dataArray = None
        if plotType == SentimentPlotType.V:
            dataArray = cacheSum[:, :, 0]/load(self.__path + '/norm/cache_sumCount_denominator_v.npy')
        elif plotType == SentimentPlotType.A:
            dataArray = cacheSum[:, :, 1]/load(self.__path + '/norm/cache_sumCount_denominator_v.npy')
        elif plotType == SentimentPlotType.C:
            dataArray = cacheSum[:, :, 2]/load(self.__path + '/norm/cache_sumCount_denominator_c.npy')

        return SentimentData(vocab, dataArray)

    def getFrequencyData(self):
        vocab = self.__getVocab50k()
        sumYear = self.__getSumYear()
        kernelYearFrequency = self.__getKernelYearFrequency()

        return FrequencyData(vocab, sumYear, kernelYearFrequency)

    def getContextNetworkData(self, year: int):
        vocab = self.__getVocab50k()
        sumYear = self.__getSumYear()
        kernelYearFrequency = self.__getKernelYearFrequency()
        sparseCsrMatrix = self.__getCompiledCoMatrixSparseCsr(year)

        return ContextNetworkData(vocab, sumYear, kernelYearFrequency, sparseCsrMatrix)

    def getSynonymNetworkData(self, year: int):
        vocab = self.__getVocab50k()
        m = load(self.__path + '/embeddings-10-years/' + str(year) + '_svd_PPMI.npy')
        m = preprocessing.normalize(m)

        return SynonymNetworkData(vocab, m)

    # TODO: find out what M is and rename this function - contact li
    def __getClosestMData(self, year: int, method: ClosestSearchMethod, use10YearsDir=False):
        year = roundToDecade(year)

        if method == ClosestSearchMethod.SGNS:
            return load(self.__path + '/sgns-hamilton/' + str(year) + '-w.npy')
        elif method == ClosestSearchMethod.SVD:
            return self.__getEmbeddingsData(year, use10YearsDir)
        else:
            raise NotImplementedError("No M data handler implemented for method: " + str(method))

    def __getEmbeddingsData(self, year: int, use10YearsDir=False):
        __embeddingsDir = '/embeddings/'
        if use10YearsDir:
            __embeddingsDir += '10-years/'

        m = load(self.__path + __embeddingsDir + str(year) + '_svd_PPMI.npy')
        return preprocessing.normalize(m)

    def __getClosestVocab(self, year: int, method: ClosestSearchMethod):
        year = roundToDecade(year)

        if method == ClosestSearchMethod.SGNS:
            return load(self.__path + '/sgns-hamilton/' + str(year) + '-vocab.pkl', allow_pickle=True)
        elif method == ClosestSearchMethod.SVD:
            return self.__getVocab50k()
        else:
            raise NotImplementedError("No vocab handler implemented for method: " + str(method))

    def __getCompiledCoMatrixSparseCsr(self, year: int):
        relativeFilePath = '/compiled-co-matrix/' + str(year) + '.npz'
        return self.__loadSparseCsr(relativeFilePath)

    def __get50kMatrixFrontSparseCsr(self, word: Word):
        relativeFilePath = '/50k-matrix-front/' + word.value[:2] + '/' + str(word.index) + '.npz'
        return self.__loadSparseCsr(relativeFilePath)

    def __loadSparseCsr(self, relativeFilePath: str):
        loader = load(self.__path + relativeFilePath)
        return sparse.csr_matrix((loader['data'], loader['indices'], loader['indptr']), shape=loader['shape'])

    # TODO: cache these
    # maybe create class data structures around each of these - eg a Vocab class
    def __getVocab50k(self):
        return read_pickle(self.__path + '/vocabulary.pkl')

    def __getKernelYearFrequency(self):
        return read_pickle(self.__path + '/year_count.pkl')

    def __getSumYear(self):
        return read_pickle(self.__path + '/sum_year.pkl')

    def __getCacheSum(self):
        return load(self.__path + '/norm/cache_sum.npy')
