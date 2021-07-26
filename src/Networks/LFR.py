import random as rnd
from .Network import Network
import networkx as nx
from networkx.generators.community import LFR_benchmark_graph

class LFR(Network):

    def __init__(self, n):
        super().__init__()
        # TODO: receive these parameters as constructor arguments
        tau1 = 3
        tau2 = 2
        mu = 0.07
        self.graph = LFR_benchmark_graph(n, tau1, tau2, mu, average_degree=5, min_community=50)

    def get_name(self):
        return 'LFR'