# Dorogovtsev-Mendes-Samukin
import random as rnd
from .Network import Network

class DMS(Network):

    def __init__(self, n):
        super().__init__()
        self._create_dms_graph(n)

    def _create_dms_graph(self, n):
        self._create_initial_nodes_and_edges()

        edges = [(0,1),(2,0),(2,1)]
        for k in range(3,n):
            a = rnd.randint(0, len(edges)-1)
            edge = edges[a]
            self.graph.add_node(k)
            self.graph.add_edge(k, edge[0])
            self.graph.add_edge(k, edge[1])
            edges.append((k,edge[0]))
            edges.append((k,edge[1]))

    def _create_initial_nodes_and_edges(self):
        self.graph.add_node(0)
        self.graph.add_node(1)
        self.graph.add_node(2)

        self.graph.add_edge(0,1)
        self.graph.add_edge(2,0)
        self.graph.add_edge(2,1)

    def get_name(self):
        return 'DMS'