class Generic():
    def __init__(self, parameters = {}):
        pass

    def start_process(self, data = {}):
        ''' Unused right now. '''
        pass

    def process(self, data = {}):
        ''' Called after every time step of a simulation. '''
        pass

    def start_step_processing(self, data = {}):
        ''' Called before the simulation for a step for a set of parameters is started but after
            the network has already been initiated. '''
        pass

    def end_step_processing(self, data = {}):
        ''' Called after the simulation for a step for a set of parameters is finished. '''
        pass
    
    def start_set_processing(self, data = {}):
        ''' Called before the simulation for a set of parameters is started. '''
        pass

    def end_set_processing(self, data = {}):
        ''' Called after the simulation for a set of parameters is finished. '''
        pass

    def start_combination_processing(self, data = {}):
        ''' Called before the simulation for the combinations of parameters is finished. '''
        pass

    def end_combination_processing(self, data = {}):
        ''' Called after the simulation for the combinations of parameters is finished. '''
        pass