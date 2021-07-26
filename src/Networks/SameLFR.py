from .ReuseNetworks import ReuseNetworks
import networkx as nx
import random as rnd
import glob

class SameLFR(ReuseNetworks):

    files = []
    idx = 0

    def get_name(self):
        return 'LFR'

    def get_network_generator(self,n):
        if len(self.files) == 0:
            self.files = glob.glob("./Data/SavedNetworks/LFR-" + str(n) + "/*.gpickle")
            self.idx = 0
        network = nx.read_gpickle( self.files[self.idx] )
        self.idx += 1
        return network