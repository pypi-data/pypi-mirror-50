from typing import List
from lib.dataStructures.SynonymNetworkNode import SynonymNetworkNode
from lib.dataStructures.SynonymNetworkEdge import SynonymNetworkEdge


class SynonymNetwork:
    def __init__(self, nodes: List[SynonymNetworkNode], edges: List[SynonymNetworkEdge]):
        self.nodes = nodes
        self.edges = edges
