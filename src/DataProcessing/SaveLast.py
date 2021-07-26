from . import Save #pylint: disable=relative-beyond-top-level
import json

''' Save the information about the last state of the network at the end of a simulation. '''
class SaveLast(Save.Save):

    def process(self, data = {}):
        ''' Do nothing. Override saving of state for every step.'''
        pass

    def end_step_processing(self, data = {}):
        if self.file == None:
            #TODO: name should be something like Model-Network-Size-Strategy
            self.file = self._open_file(data)
        self._write('%s\n' % (json.dumps(data['network'].get_per_state())))