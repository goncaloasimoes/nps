# Rumour SIR (Nekovee) with 
from .Model import GenericModel
import random

class rSIR_V_T(GenericModel):
    ''' Classical Rumor Spreading Model with Vaccinated States and Timescale batching. '''

    def constructor(self, beta, gamma, delta, theta, timescale):
        super().__init__(
            ['S', 'I', 'R', 'V'],
            {
                'beta'     : beta,
                'gamma'    : gamma,
                'delta'    : delta,
                'theta'    : theta,
                'timescale': timescale
            },
            {
                'IS': self.infect,
                'II': self.init_spreader_becomes_stifler,
                'IR': self.init_spreader_becomes_stifler,
                'VS': self.vaccinate,
                'I' : self.forget,
            }
        )

    def __init__(self, beta = .5, gamma = .5, delta = .5, theta = .5, timescale = .5): 
        self.constructor(beta, gamma, delta, theta, timescale)

    def end_condition(self, time_step, network):
        return network.get_count_of_state('I') == 0

    def basic_init(self):
        return {'S': 1.0, 'I': 0.0, 'R': 0.0, 'V': 0.0}
    
    def get_name(self):
        return 'rSIR_V_T'

    def get_states_to_update(self, network):
        ''' Timescale. '''
        if random.uniform(0, 1 + self.get_parameter('timescale')) <= 1:
            return ['I']
        else:
            return ['V']
    
    def get_states_for_strategy(self):
        return { 'inf': 'I', 'vac': 'V' }

    # Transitions
    def infect(self, initiator, initiator_state, receiver, receiver_state, network):
        if random.random() <= self.get_parameter('beta'):
            return [ initiator_state, 'I']
        return [ initiator_state, 'S' ]

    def init_spreader_becomes_stifler(self, initiator, initiator_state, receiver, receiver_state, network):
        if random.random() <= self.get_parameter('gamma'):
            return [ 'R', receiver_state ]
        return [ initiator_state, receiver_state ]

    def vaccinate(self, initiator, initiator_state, receiver, receiver_state, network):
        if random.random() <= self.get_parameter('theta'):
            return [ initiator_state, 'V' ]
        return [ initiator_state, receiver_state ]
    
    def forget(self, node, state, network):
        if random.random() <= self.get_parameter('delta'):
            return 'R'
        return state
