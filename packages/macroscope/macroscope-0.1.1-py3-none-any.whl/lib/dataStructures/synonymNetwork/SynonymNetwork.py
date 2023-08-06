from typing import List
from lib.dataStructures.synonymNetwork.SynonymNetworkNode import SynonymNetworkNode
from lib.dataStructures.synonymNetwork.SynonymNetworkEdge import SynonymNetworkEdge


class SynonymNetwork:
    def __init__(self, nodes: List[SynonymNetworkNode], edges: List[SynonymNetworkEdge]):
        self.nodes = nodes
        self.edges = edges
