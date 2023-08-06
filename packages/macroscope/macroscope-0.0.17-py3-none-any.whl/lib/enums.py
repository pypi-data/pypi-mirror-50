from enum import Enum


class ClosestSearchMethod(Enum):
    SVD = 'svd'
    SGNS = 'sgns'


class ContextNetworkMethod(Enum):
    PMI = 'PMI'
    COR = 'COR'


class Reduce(Enum):
    PCA = 'pca'
    TSNE = 't-sne'


class SentimentPlotType(Enum):
    V = 'V'
    A = 'A'
    C = 'C'
