# Rumour SIR
from .Model import GenericModel
import random

class rSIR(GenericModel):
    ''' Classical Rumor Spreading Model. '''

    def constructor(self, beta, gamma, delta):
        super().__init__(
            ['S', 'I', 'R'],
            {
                'beta': beta,
                'gamma': gamma,
                'delta': delta
            },
            {
                'IS': self.infect,
                'II': self.init_spreader_becomes_stifler,
                'IR': self.init_spreader_becomes_stifler,
                'I' : self.forget,
            }
        )

    def __init__(self, beta = .5, gamma = .5, delta = .5): 
        self.constructor(beta, gamma, delta)

    def end_condition(self, time_step, network):
        return network.get_count_of_state('I') == 0
    
    def basic_init(self):
        return {'S': 1.0, 'I': 0.0, 'R': 0.0}
    
    def get_name(self):
        return 'rSIR'

    def get_states_for_strategy(self):
        return { 'inf': 'I', 'vac': 'R' }

    # Transitions
    def infect(self, initiator, initiator_state, receiver, receiver_state, network):
        if random.random() <= self.get_parameter('beta'):
            return [ initiator_state, 'I']
        return [ initiator_state, 'S' ]

    def init_spreader_becomes_stifler(self, initiator, initiator_state, receiver, receiver_state, network):
        if random.random() <= self.get_parameter('gamma'):
            return [ 'R', receiver_state ]
        return [ initiator_state, receiver_state ]
    
    def forget(self, node, state, network):
        if random.random() <= self.get_parameter('delta'):
            return 'R'
        return state