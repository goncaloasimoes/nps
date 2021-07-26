# How to initialise the network regarding states
import networkx as nx
from operator import itemgetter
import math
import random

class Network:

    def __init__(self):
        self.graph = nx.Graph()
        self.per_state = dict()
        self.info = {}

    def __iter__(self):
        return self.graph.__iter__()

    def get_graph(self):
        return self.graph

    def get_node_state(self, node):
        return self.graph.nodes[node]['state']

    def set_node_state(self, node, state):
        old_state = self.graph.nodes[node]['state']
        self._remove_from_state_count(old_state, 1)
        self.graph.nodes[node]['state'] = state
        self._add_to_state_count(state, 1)

    def get_per_state(self):
        return self.per_state

    def get_count_of_state(self, state):
        return self.per_state[state]

    def get_size(self):
        return len(self.graph)

    def set_count_of_state(self, state, value):
        self.per_state[state] = value

    def set_state_for_n_randoms(self, state, n, force_state=False):
        if force_state:
            # TODO: make this not the default, get it from model
            susceptible_nodes = [x for x,y in self.graph.nodes(data=True) if y['state']=='S']
            nodes_to_change = random.sample( susceptible_nodes, k=n )
        else:
            #TODO: check if n is int
            nodes_to_change = random.sample(
                range(0, len(self.graph)), # all nodes
                n
            )
        for node in nodes_to_change:
            self.set_node_state(node, state)

    def neighbors(self, node_number):
        return self.graph.neighbors(node_number)

    def get_node_with_attr(self, node_number):
        return self.graph.nodes[node_number]

    #TODO: test code
    def initialize_states(self, parameters = {'S': 1.0}):
        '''Initialize the states of the nodes with the given parameters and their percentages.'''
        #TODO: deal with more complex initialization
        sorted_params = self._sort_parameters(parameters)
        # Base state
        base_state, percentage_base_state = self._set_base_state(sorted_params)
        # Per state count
        self.per_state = {param: 0 for param in parameters}
        # Other states
        count_of_other_states = self._set_other_states(sorted_params, percentage_base_state)
        # Update base state count
        self.per_state[base_state] = len(self.graph) - count_of_other_states

    def _set_base_state(self, sorted_params):
        base_state = sorted_params[0][0]
        percentage_base_state = sorted_params[0][1]
        nx.classes.function.set_node_attributes(self.graph, base_state, 'state')
        del sorted_params[0]
        return [base_state, percentage_base_state]

    def _set_other_states(self, sorted_params, percentage_base_state):
        # Randomly select a set of (1.0 - percentage_base_state) * size of network, and rounded down
        nodes_to_change = random.sample(
            range(0, len(self.graph)), # all nodes
            int((1.0 - percentage_base_state) * len(self.graph)) # Rounded down the number of nodes available for the other states
        )
        # For every state and its percentage, get a random subset of the above random subset and change their state
        idx = 0
        for param in sorted_params:
            idx = self._set_single_other_state(nodes_to_change, param, idx)
        return idx

    def _set_single_other_state(self, nodes_to_change, state_def, idx):
        how_many = int(len(self.graph) * state_def[1])
        subset = nodes_to_change[idx : idx + how_many]
        nx.set_node_attributes(
            self.graph,
            dict.fromkeys(subset, {'state': state_def[0]})
        )
        self.per_state[state_def[0]] = how_many
        return idx + how_many

    def _sort_parameters(self, parameters):
        params = parameters.items()
        sum_percentage = [0.0]

        def sort_auxiliary(item, sum_percentage):
            sum_percentage[0] += item[1]
            return item[1]

        params = sorted(
            params,
            key = lambda x: sort_auxiliary(x, sum_percentage),
            reverse=True
        )
        sum_percentage = sum_percentage[0]
        if not math.isclose(1.0, sum_percentage):
            raise Exception('Percentages for network initiation do not sum  \
                to 100%, but to ' + str(sum_percentage * 100) + '%.')
        return params

    def _add_to_state_count(self, state, number):
        self.per_state[state] += number

    def _remove_from_state_count(self, state, number):
        self.per_state[state] -= number