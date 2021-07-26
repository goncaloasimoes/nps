from .ReuseNetworks import ReuseNetworks
import networkx as nx
import random as rnd

class SameDMS(ReuseNetworks):

    def get_name(self):
        return 'DMS'

    def get_network_generator(self,n):
        return self._create_dms_graph(n)

    # TODO: Repeated code from DMS.py
    def _create_dms_graph(self, n):
        graph = nx.Graph()
        self._create_initial_nodes_and_edges(graph)

        edges = [(0,1),(2,0),(2,1)]
        for k in range(3,n):
            a = rnd.randint(0, len(edges)-1)
            edge = edges[a]
            graph.add_node(k)
            graph.add_edge(k, edge[0])
            graph.add_edge(k, edge[1])
            edges.append((k,edge[0]))
            edges.append((k,edge[1]))
        return graph

    def _create_initial_nodes_and_edges(self, graph):
        graph.add_node(0)
        graph.add_node(1)
        graph.add_node(2)

        graph.add_edge(0,1)
        graph.add_edge(2,0)
        graph.add_edge(2,1)