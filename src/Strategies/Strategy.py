# Strategy should have a param/function that says when to apply the strategy
# TODO: be able to apply the strategy in the middle of the simulation with a different function than
#       apply_strategy and a function on whether to do it or not

class GenericStrategy:

    def __init__(self, model, purpose, parameters):
        self.model      = model
        self.purpose    = purpose
        self.parameters = parameters

    def override_initialization(self):
        ''' Whether the model's basic initialization will be called before the strategy. '''
        return False
    
    def apply_strategy(self, network): #TODO: maybe needs more args
        ''' Apply the strategy to the network. '''
        pass