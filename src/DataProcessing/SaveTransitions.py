from . import Save #pylint: disable=relative-beyond-top-level
import json

class SaveTransitions(Save.Save):

    def process(self, data = {}):
        ''' Do nothing. Override saving of state for every step.'''
        pass

    def end_step_processing(self, data = {}):
        if self.file == None:
            #TODO: name should be something like Model-Network-Size-Strategy
            self.file = self._open_file(data)
        self._write('%s\n' % (json.dumps(data['network'].info)))