from . import Save #pylint: disable=relative-beyond-top-level
import json
import statistics

class SavePolarization(Save.Save):

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
        #print(len(communities))
        fractions = []
        for nodes in communities:
            
            edges = set()
            for node in nodes:
                neighbors = G.neighbors(node)
                for neighbor in neighbors:
                    if neighbor in nodes:
                        edges.add( (node, neighbor) )
            # print('community edges')
            # print(len(edges))
            diff  = 0
            total = 0
            diffs = { 'V': 0, 'R': 0, 'S': 0 }
            for edge in edges:
                state_0 = G.nodes[edge[0]]['state']
                state_1 = G.nodes[edge[1]]['state']
                if state_0 != state_1:
                    diff +=1
                if state_0 == 'V' and state_1 == 'V':
                    diffs['V'] += 1
                if state_0 == 'R' and state_1 == 'R':
                    diffs['R'] += 1
                if state_0 == 'S' and state_1 == 'S':
                    diffs['S'] += 1
                total +=1
            # print(total)
            # print(diff)
            # print(diffs)
            fractions.append( diff/total )
        # print(fractions)
        a = statistics.mean(fractions)
        index = (1-a)
        #print('INDEX')
        #print(index)
        # print( (1-a) * 100)
        # print(list(network.neighbors(0)))
        self._write('%s\n' % (json.dumps({'polarization': index})))