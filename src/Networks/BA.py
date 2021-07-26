# Barabasi Albert
from .Network import Network
import networkx as nx

class BA(Network):

    def __init__(self, n):
        super().__init__()
        self.graph = nx.barabasi_albert_graph(n,2)

    def get_name(self):
        return 'BA'