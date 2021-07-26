# String multiple data processors together
# if Save, Visualize
# start: Save -> Visualize
# end: Visualize -> Save
#pylint: disable=relative-beyond-top-level
from . import Generic 
from . import DataProcessorGetter

class MultipleProcessing(Generic.Generic):
    processors = []

    def __init__(self, processors, parameters = {}):
        super().__init__(parameters)
        self._create_processors(processors, parameters)

    def start_process(self, data = {}):
        ''' Unused right now. '''
        self._call_processors_function('start_process', data, reverse = False)

    def process(self, data = {}):
        ''' Called after every time step of a simulation. '''
        self._call_processors_function('process', data, reverse = False)

    def start_set_processing(self, data = {}):
        ''' Called before the simulation for a set of parameters is started. '''
        self._call_processors_function('start_set_processing', data, reverse = False)

    def end_set_processing(self, data = {}):
        ''' Called after the simulation for a set of parameters is finished. '''
        self._call_processors_function('end_set_processing', data, reverse = True)

    def start_combination_processing(self, data = {}):
        ''' Called before the simulation for the combinations of parameters is finished. '''
        self._call_processors_function('start_combination_processing', data, reverse = False)

    def end_combination_processing(self, data = {}):
        ''' Called after the simulation for the combinations of parameters is finished. '''
        self._call_processors_function('end_combination_processing', data, reverse = True)

    def _call_processors_function(self, func_name, data, reverse = False):
        iterator = self.processors if not reverse else reversed(self.processors)
        for processor in iterator:
            func = getattr(processor, func_name)
            func(data)

    def _create_processors(self, processors, parameters):
        for processor in processors:
            if processor == 'Multiple':
                raise Exception('Do not use Multiple processor like this. It is something to be created by the program by itself.')
            self.processors.append(
                DataProcessorGetter.get_data_processor(processor)(parameters)
            )