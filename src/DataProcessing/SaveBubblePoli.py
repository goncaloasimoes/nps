from . import Save #pylint: disable=relative-beyond-top-level
import json
import statistics

'''
Save polarization index of a network at the end of a simulation on said network.

This polarization index characterizes how much polarization there is on a network on a community bases, by measuring the reverse of mean of 
cross edges over total edges, per community. Cross edges represent edges between different states. A network has various communities when its
nodes have a 'community' property which represents which community they belong to. If they don't have these properties, the whole network is 
considered as a whole community.

Index: 1 - mean(cross_edges/total_edges, per community.)
'''
class SaveBubblePoli(Save.Save):

    def process(self, data = {}):
        ''' Do nothing. Override saving of state for every step.'''
        pass

    def end_step_processing(self, data = {}):
        if self.file == None:
            #TODO: name should be something like Model-Network-Size-Strategy
            self.file = self._open_file(data)

        G = data['network'].graph
        if 'community' not in G.nodes[0]:
            communities = {frozenset(G.nodes)}
        else:
            communities = {frozenset(G.nodes[v]["community"]) for v in G}

        per_node = {}
        for nodes in communities:
            for node in nodes:
                diff  = 0
                total = 0

                state_0 = G.nodes[node]['state']
                for neighbor in G.neighbors(node):
                    state_1 = G.nodes[neighbor]['state']
                    if state_0 != state_1:
                        diff +=1
                    total +=1
                per_node[node] = diff/total

        ## Communities
        per_communities = []
        i = 0
        for community in communities:
            per = []
            for node in community:
                per.append(per_node[node])
            per_communities.append( statistics.mean(per) )

            i += 1
        self._write('%s\n' % (json.dumps({'polarization': 1 - statistics.mean(per_communities)})))