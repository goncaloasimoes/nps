from .ReuseNetworks import ReuseNetworks
import networkx as nx

class SameBA(ReuseNetworks):

    def get_name(self):
        return 'BA'

    def get_network_generator(self,n):
        return nx.barabasi_albert_graph(n,2)