# Generic Model
from .Auxiliaries.Transitions import Transitions

class GenericModel:

    def __init__(self, states = [], parameters = {}, transitions = {}):
        self.states = states
        self.parameters = parameters
        self.transitions = Transitions(transitions)

    def end_condition(self, time_step, network):
        pass

    def get_states_to_update(self, network):
        ''' 
            Which states should be updated.
            The normal behavior is for all states to be updated every step. But in some cases we
            might want to change these dynamically, like when simulating timescales of transitions.
        '''
        return self.states

    def get_states_for_strategy(self):
        '''
            TODO: example { inf: I, vac: R }
        '''
        return {}

    def get_states(self):
        return self.states

    def get_transitions(self):
        return self.transitions

    def get_parameters(self):
        return self.parameters

    def get_parameter(self, name):
        return self.parameters[name]

    def set_parameter(self, parameter, value):
        self.parameters[parameter] = value

    def set_parameters(self, parameters):
        self.parameters = {**self.parameters, **parameters}