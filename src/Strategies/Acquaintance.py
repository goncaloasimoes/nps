# Random strategy for "vaccination"
from .Strategy import GenericStrategy
import random

class Acquaintance(GenericStrategy):

    default_states = { 'inf': 'I', 'vac': 'R' }

    def apply_strategy(self, network, param_value):
        # Only expects one state.
        # TODO: verify output
        strategy_state = self.model.get_states_for_strategy()[self.purpose]
        if len(strategy_state) == 0:
            if self.purpose not in self.default_states:
                raise Exception( 'Model does not accept purpose %s.' % self.purpose ) #TODO:
            strategy_state = self.default_states[self.purpose]
            if strategy_state not in self.model.get_states():
                raise Exception( 'Default state for random strategy doesnt work for this model.' )
        elif len(strategy_state) >= 1:
            strategy_state = strategy_state[0]

        # Get number to change (fraction or literal)
        #TODO: verify if number
        # number_to_change = 0.1
        # if self.purpose == 'vac' and 'vaccinate' in self.parameters:
        #         number_to_change = self.parameters['vaccinate']
        # elif self.purpose == 'inf' and 'infect' in self.parameters:
        #         number_to_change = self.parameters['infect']
        number_to_change = param_value

        n_states = int(number_to_change)
        # If it is a fraction then get the percentage of the network to change
        if isinstance(number_to_change, float) and number_to_change < 1:
            n_states = int(network.get_size() * number_to_change)

        # Randomly change nodes in the network
        randoms = random.sample( range( 0, network.get_size() ), n_states )

        for node in randoms:
            neighbors = list(network.neighbors(node))
            #TODO: default state should come from model
            accepted_neighbors = [x for x in neighbors if network.graph.nodes[x]['state']=='S']
            if len( accepted_neighbors) == 0:
                continue
            network.set_node_state( random.choice( accepted_neighbors ), strategy_state )