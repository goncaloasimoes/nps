from ..Helpers.Singleton import Singleton
from .Network import Network
import random

class ReuseNetworks(Network,metaclass=Singleton):

    number_networks = 100 # TODO: this sould be configurable
    networks        = []
    last            = -1

    def __init__(self, n, incremental = False):
        self.per_state = dict()
        self.info = {}

        if len( self.networks ) == 0:
            print( 'Generating ' + str(self.number_networks) + ' networks...' )
            for i in range(0, self.number_networks):
                self.networks.append( self.get_network_generator(n) )

        if incremental:
            self.last += 1
            if self.last == len(self.networks):
                self.last = 0
            choice = self.last
        else:
            choice = random.randint(0, self.number_networks - 1)
        self.graph = self.networks[choice]

    def get_network_generator(self,n):
        raise Exception('This class shouldn\'t be used by itself.')