# Choose the processor to get given its string name
# pylint: disable=relative-beyond-top-level
from . import Generic 
from . import Save
from . import Visualize
from pydoc import locate

known_processors = {
    'None': Generic.Generic,
    'Save': Save.Save,
    'Visualize': Visualize.Visualize
}

def get_data_processor(name):
    if name in known_processors:
        return known_processors[name]
    processor_class = locate(".src.DataProcessing." + name + '.' + name)
    if processor_class == None:
        raise Exception('Data Processor ' + name + ' does not exist.')
    return processor_class