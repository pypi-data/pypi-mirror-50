# External libraries
from numpy import vstack, linalg
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# Standard library
from typing import List

# Local libraries
from lib.utils.DataReader import DataReader, DriftData
from lib.utils.partitionInterval import partitionInterval
from lib.wordSpaces.ClosestWordSpace import ClosestWordSpace
from lib.enums import ClosestSearchMethod, Reduce
from lib.dataStructures.Word import Word
from lib.dataStructures.YearPoint import YearPoint
from lib.dataStructures.WordPoint import WordPoint
from lib.dataStructures.Coord import Coord
from lib.dataStructures.SemanticDriftPoints import SemanticDriftPoints
from lib.utils.roundToDecade import roundToDecade


class DriftWordSpace:
    def __init__(self, dataReader: DataReader):
        self.__dataReader = dataReader
        self.__closestWordSpace = ClosestWordSpace(dataReader)

        # TODO: add as cli options?
        self.__closestMethod = ClosestSearchMethod.SVD
        self.__historicallyAlign = True
        self.__reduce = Reduce.PCA
        self.__numberOfReduceComponents = 2
        self.__mirror = False

        # for __loadData
        self.__data: DriftData = None
        self.__startYear = None
        self.__endYear = None

    def getWordObj(self, wordValue: str, startYear: int, endYear: int):
        #  TODO: cache already indexed words?
        self.__loadData(startYear, endYear)

        return Word(self.__data.vocab.index(wordValue), wordValue)

    def getSemanticDriftPoints(
        self,
        wordValue: str,
        startYear: int,
        endYear: int,
        numberOfYearsInInterval: int,
        numberOfClosestWords: int
    ):
        years = self.__getYearsArray(startYear, endYear, numberOfYearsInInterval)

        # __getYearsArray rounds start and end year to nearest decade so we reassign them here
        __startYear = years[0]
        __endYear = years[-1]
        self.__loadData(__startYear, __endYear)

        if self.__historicallyAlign:
            self.__data.m_startYear = self.__procrustesAlign(self.__data.m_endYear, self.__data.m_startYear)

        # TODO: get context words for all years not just start and end years? - contact li
        contextWordValues = self.__getContextWordValues(wordValue, [__startYear, __endYear], numberOfClosestWords)
        contextWordIndices = [self.__data.vocab.index(word) for word in contextWordValues]

        targetWord = self.getWordObj(wordValue, __startYear, __endYear)

        compiledM = self.__getCompiledM(contextWordIndices, targetWord, years, self.__data)
        chosen = self.__getChosen(compiledM)

        x_coords = chosen[:, 0]
        y_coords = chosen[:, 1]

        wordPoints = []
        yearPoints = []
        yearIndex = 0
        for i, point in enumerate(chosen):
            x = x_coords[i]
            y = y_coords[i]

            coord = Coord(x, y)

            if i < len(contextWordIndices):
                value = contextWordValues[i]
                index = contextWordIndices[i]
                word = Word(index, value)

                wordPoint = WordPoint(word, coord)
                wordPoints.append(wordPoint)
            else:
                year = years[yearIndex]

                yearPoint = YearPoint(year, coord)
                yearPoints.append(yearPoint)

                yearIndex += 1

        return SemanticDriftPoints(yearPoints, wordPoints)

    def __getYearsArray(self, startYear: int, endYear: int, numberOfYearsInInterval: int):
        self.__parseYearValues(startYear, endYear)

        __startYear = roundToDecade(startYear)
        __endYear = roundToDecade(endYear)

        maxNumberOfYears = int((endYear - startYear)/10) + 1
        if numberOfYearsInInterval > maxNumberOfYears:
            numberOfYearsInInterval = maxNumberOfYears

        years = partitionInterval(__startYear, __endYear, numberOfYearsInInterval)
        years = [roundToDecade(year) for year in years]

        return years

    def __parseYearValues(self, startYear: int, endYear: int):
        if endYear < startYear:
            raise ValueError("StartYear: " + str(startYear) + " must be before EndYear: " + str(endYear))

        if endYear - startYear < 10:
            raise ValueError(
                "StartYear: " + str(startYear) + " and EndYear: " + str(endYear) + " must have a 10 year gap"
            )

    def __getCompiledM(self, indeces, targetWord: Word, years: List[int], data: DriftData):
        compiledM = data.m_endYear[indeces, :]   # get modern embeddings

        compiledM_startYear = data.m_startYear[targetWord.index]
        compiledM_endYear = data.m_endYear[targetWord.index]

        year_continues = years[1:-1]
        if len(year_continues) > 0:
            # TODO: why do we use 10 years directory for between years but not for other years? - contact li
            m = self.__dataReader.getClosestMForYears(year_continues, self.__closestMethod, use10YearsDir=True)

            betweenWordT = []
            for year in year_continues:
                if self.__historicallyAlign:
                    m[year] = self.__procrustesAlign(data.m_endYear, m[year])

                betweenWordT.append(m[year][targetWord.index, :])

            return vstack([compiledM, compiledM_startYear, betweenWordT, compiledM_endYear])
        else:
            return vstack([compiledM, compiledM_startYear, compiledM_endYear])

    def __getChosen(self, compiledM):
        chosen = None
        if self.__reduce == Reduce.PCA:
            chosen = PCA(n_components=self.__numberOfReduceComponents).fit_transform(compiledM)
        elif self.__reduce == Reduce.TSNE:
            pca_30 = PCA(n_components=30).fit_transform(compiledM)
            chosen = TSNE(
                n_components=self.__numberOfReduceComponents,
                init='pca',
                verbose=1,
                perplexity=40,
                n_iter=500,
                learning_rate=30
            ).fit_transform(pca_30)
        else:
            raise NotImplementedError("Reduce method: " + str(self.__reduce) + " not implemented")

        # TODO: what is this for? - contact li
        if self.__mirror:
            chosen[:, 0] = -1*chosen[:, 0]

        return chosen

    def __getContextWordValues(self, wordValue: str, years: List[int], numberOfClosestWords: int) -> List[str]:
        synonyms = set()  # set doesn't allow duplicate values
        for year in years:
            __closestWords = self.__closestWordSpace.getClosestWords(
                wordValue,
                year,
                numberOfClosestWords,
                self.__closestMethod
            )
            for i in range(numberOfClosestWords):
                synonyms.add(__closestWords[i].word.value)

        return list(synonyms)  # return to list so values can be accessed by index

    def __procrustesAlign(self, base_embed, other_embed):
        # """
        #    Align other embedding to base embeddings via Procrustes.
        #    Returns best distance-preserving aligned version of other_embed
        #    NOTE: Assumes indices are aligned
        # """

        basevecs = base_embed - base_embed.mean(0)
        othervecs = other_embed - other_embed.mean(0)
        m = othervecs.T.dot(basevecs)
        u, _, v = linalg.svd(m)
        ortho = u.dot(v)
        fixedvecs = othervecs.dot(ortho)

        return fixedvecs

    def __loadData(self, startYear: int, endYear: int):
        # TODO: cache loaded data - store in hash table (dict) with key str(year_method)
        if self.__data is not None and self.__startYear == startYear and self.__endYear == endYear:
            return

        self.__data = self.__dataReader.getDriftData(startYear, endYear, self.__closestMethod)
        self.__startYear = startYear
        self.__endYear = endYear
