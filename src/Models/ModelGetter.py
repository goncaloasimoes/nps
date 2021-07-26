# Choose the model to get given its string name
# pylint: disable=relative-beyond-top-level
from . import SIR
from pydoc import locate

known_models = {
    'SIR': SIR.SIR
}
    
def get_model(name):
    if name in known_models:
        return known_models[name]
    model_class = locate(".src.Models." + name + '.' + name)
    if model_class == None:
        raise Exception('Model ' + name + ' does not exist.')
    return model_class