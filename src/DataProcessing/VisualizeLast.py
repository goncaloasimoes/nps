from . import Visualize #pylint: disable=relative-beyond-top-level

''' Visualize the last state of network at the end of a simulation. '''
class VisualizeLast(Visualize.Visualize):

    def process(self, data = {}):
        ''' Do nothing. Override saving of state for every step.'''
        pass

    def end_step_processing(self, data = {}):
        self.show_legend = False
        self.draw(data)
        self.save_number += 1
        self.step += 1
        self.graph_layout = None # Reset layout