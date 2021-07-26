# Choose the network to get given its string name
# pylint: disable=relative-beyond-top-level
from . import DMS, BA, LFR
from pydoc import locate

known_networks = {
    'DMS': DMS.DMS,
    'BA': BA.BA,
    'LFR': LFR.LFR
}

def get_network(name):
    if name in known_networks:
        return known_networks[name]
    network_class = locate(".src.Networks." + name + '.' + name)
    if network_class == None:
        raise Exception('Network ' + name + ' does not exist.')
    return network_class