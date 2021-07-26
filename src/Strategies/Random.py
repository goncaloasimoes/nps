# Random strategy for "vaccination"
from .Strategy import GenericStrategy
import random

class Random(GenericStrategy):

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
        number_to_change = param_value

        n_states = int(number_to_change)
        # If it is a fraction then get the percentage of the network to change
        if isinstance(number_to_change, float) and number_to_change < 1:
            n_states = int(network.get_size() * number_to_change)

        # Randomly change nodes in the network
        network.set_state_for_n_randoms(strategy_state, n_states, True) 