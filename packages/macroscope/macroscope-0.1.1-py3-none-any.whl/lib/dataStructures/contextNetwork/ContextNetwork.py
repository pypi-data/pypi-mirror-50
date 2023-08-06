from typing import List
from lib.dataStructures.contextNetwork.ContextNetworkNode import ContextNetworkNode
from lib.dataStructures.contextNetwork.ContextNetworkEdge import ContextNetworkEdge


class ContextNetwork:
    def __init__(self, nodes: List[ContextNetworkNode], edges: List[ContextNetworkEdge]):
        self.nodes = nodes
        self.edges = edges
