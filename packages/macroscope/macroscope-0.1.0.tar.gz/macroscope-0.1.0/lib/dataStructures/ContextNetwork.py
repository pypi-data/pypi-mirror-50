from typing import List
from lib.dataStructures.ContextNetworkNode import ContextNetworkNode
from lib.dataStructures.ContextNetworkEdge import ContextNetworkEdge


class ContextNetwork:
    def __init__(self, nodes: List[ContextNetworkNode], edges: List[ContextNetworkEdge]):
        self.nodes = nodes
        self.edges = edges
