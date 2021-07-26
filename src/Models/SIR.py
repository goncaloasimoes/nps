from .Model import GenericModel
import random

class SIR(GenericModel):
    ''' Classical Epidemic Spreading Model. '''

    def constructor(self, beta, gamma):
        super().__init__(
            ['S', 'I', 'R'],
            {
                'beta': beta,
                'gamma': gamma
            },
            {
                'IS': self.infect,
                'I': self.recover
            }
        )

    def __init__(self, beta = .5, gamma = .5): 
        self.constructor(beta, gamma)
    
    def end_condition(self, time_step, network):
        return network.get_count_of_state('I') == 0

    def basic_init(self):
        return {'S': 1.0, 'I': 0.0, 'R': 0.0}

    def get_name(self):
        return 'SIR'
    
    def get_states_for_strategy(self):
        return { 'inf': 'I', 'vac': 'R' }

    # Transitions
    def infect(self, initiator, initiator_state, receiver, receiver_state, network):
        if random.random() <= self.get_parameter('beta'):
            return [ initiator_state, 'I' ]
        return [ initiator_state, receiver_state ]

    def recover(self, node, state, network):
        if random.random() <= self.get_parameter('gamma'):
            return 'R'
        return 'I'