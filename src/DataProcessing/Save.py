from . import Generic #pylint: disable=relative-beyond-top-level
from datetime import datetime
import json

class Save(Generic.Generic):
    default_save_location = './Data/'
    step = None
    file = None
    filename = 'temp' #TODO: this is overwritten by the filename created below while saving

    def __init__(self, parameters = {}):
        super().__init__(parameters)
        #TODO: verify if save_location given has '/' at the end
        self.save_location = parameters['save_location'] if 'save_location' in parameters else self.default_save_location

    def process(self, data = {}):
        ''' Save the data in the save location with a given name. '''
        if self.file == None:
            #TODO: name should be something like Model-Network-Size-Strategy
            self.file = self._open_file(data)

        self._write('%s\n' % (json.dumps(data['network'].get_per_state())))
        pass

    def start_step_processing(self, data = {}):
        print( ' Step: %s' % data['step'], end=' ' )
        if self.step == None:
            self._write('Step: %s\n' % str(data['step']))
            self.step = data['step']
        elif self.step != data['step']:
            self._write('Step: %s\n' % str(data['step']))
            self._finish_step()
            self.step = data['step']

    def start_set_processing(self, data = {}):
        if self.file == None:
            #TODO: name should be something like Model-Network-Size-Strategy
            self.file = self._open_file(data)
        #TODO: save as json.dumps
        self._write("VALUES: %s\n" % ( json.dumps(data['param_values'].get_values())))
        pass

    def end_set_processing(self, data = {}):
        ''' Signal that processing has ended for a set of parameters. '''
        print( 'Done!' +  ' ' * 20 )
        pass

    def end_combination_processing(self, data = {}):
        ''' Signal that processing has ended in order to finish the saving. '''
        self._write('END_OF_DATA')
        self.file.close()
        self.file = None
        pass

    def _finish_step(self):
        ''' Finish a step in the save. '''
        pass

    def _open_file(self, data = {}):
        ''' Return a file opened with a filename generated from the data. '''
        #TODO: refactor into smaller functions
        if 'network_class' in data:
            network_name = data['network_class'].__name__
        elif 'network' in data:
            network_name = data['network'].get_name()
        else:
            raise Exception('No way to get network name when creating data file.')

        if 'size' in data:
            size = data['size']
        elif 'network' in data:
            size = data['network'].get_size()
        else:
            raise Exception('No way to get network size when creating data file.')

        return open(
            self.save_location + "%s-%s-%s-%s.txt" % (
                data['model'].get_name(), network_name, size, datetime.now().strftime("%Y%m%d%H%M%S")
            ),
            "w+"
        )

    def _write(self, output):
        self.file.write(output)

    def start_process(self, data = {}):
        pass