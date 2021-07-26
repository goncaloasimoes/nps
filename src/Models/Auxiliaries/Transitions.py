class Transitions:

    def __init__(self, transitions):
        self.pair_transitions = {}
        self.self_transitions = {}

        for key in transitions.keys():
            # Pair Transition
            if len(key) == 2:
                initiator = key[0]
                receiver = key[1]
                if initiator in self.pair_transitions:
                    if receiver in self.pair_transitions[initiator]:
                        raise Exception("Error when creating transitions: Receiver " + receiver + " for initiator " + initiator + " already defined.")
                else:
                    self.pair_transitions[initiator] = {}
                self.pair_transitions[initiator][receiver] = transitions[key]
                
            elif len(key) == 1:
                if key in self.self_transitions:
                    raise Exception("Error when creating transition: There is already a single transition for " + key + " defined.")
                self.self_transitions[key] = transitions[key]
    
    def get_all_pair_initiators(self):
        return list(self.pair_transitions.keys())

    def get_all_self_transitions(self):
        return list(self.self_transitions.keys())

    def get_receivers_of(self, initiator_state):
        return list(self.pair_transitions[initiator_state].keys())
    
    def check_if_state_has_pair_transitions(self, initiator_state):
        return initiator_state in self.pair_transitions

    def check_if_receiver_available(self, initiator_state, receiver_state):
        return receiver_state in self.pair_transitions[initiator_state]

    def call_pair_transition_function(self, initiator, initiator_state, receiver, receiver_state, network):
        return self.pair_transitions[initiator_state][receiver_state](
            initiator,
            initiator_state,
            receiver,
            receiver_state,
            network
        )
    
    def check_if_self_transition_exists(self, state):
        return state in self.self_transitions
    
    def call_self_transition_function(self, node, state, network):
        return self.self_transitions[state](node, state, network)