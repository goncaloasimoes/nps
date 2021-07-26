# Save the simulations as images or gifs
import networkx as nx
import matplotlib.pyplot as plt
from . import Generic #pylint: disable=relative-beyond-top-level
from matplotlib.lines import Line2D
from matplotlib.backends.backend_agg import FigureCanvas
import imageio
import os
import cv2
import numpy as np

#TODO: on the side of the network, draw a graph which shows the numbers of each state overtime.
#TODO: stop overwriting previous files, maybe add date to filename
#TODO: class needs to be reworked to receive options/config via __init__

'''Visualize simulation as they happen or save snapshots at each timestep.'''
class Visualize(Generic.Generic):
    #TODO: more colors
    default_colors = ['blue', 'red', 'yellow', 'green', 'purple']
    temp_save_location = './Data/TempMedia/' #TODO: delete directory at the start of each
    default_save_location = './Data/Media/'
    default_filename = 'temp' #TODO:
    show_legend = False
    create_gif = True #TODO: get this from parameters
    step = 0 # Current step of combination
    part = 0 # Current part of the simulation ( for ordering images )
    save_number = 1
    figure = plt.figure(figsize=(10,10))
    show_in_window = True # Whether to save or show, TODO: receive via __init__
    graph_layout = None

    def __init__(self, parameters = {}):
        super().__init__(parameters)
        self.save_location = parameters['save_location'] if 'save_location' in parameters else self.default_save_location
        #TODO: how to make sure this is used only by Visualize and not by Save when doing multiple
        self.filename = parameters['filename'] if 'filename' in parameters else self.default_filename
        self.show_legend = parameters['show_legend'] if 'show_legend' in parameters else self.default_show_legend
        if self.show_in_window:
            cv2.namedWindow('img', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('img', 1000,1000)

    def process(self, data):
        self.draw(data)

    def draw(self, data, draw_before=None, draw_after=None):
        #TODO: Model specific
        #FIXME: fix this return
        color_map, states, color_order = self._get_color_map(data['network'], data['model'])
        graph = data['network'].get_graph()
        if self.graph_layout is None:
            # TODO: Receive which layout to use via __init__
            #self.graph_layout = nx.kamada_kawai_layout(graph, scale=1)
            self.graph_layout = nx.spring_layout(graph, scale=1, seed=100)
        ax = self.figure.add_subplot(111)
        plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
        plt.axis('off')
        ax.axis('off')
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        if draw_before != None:
            draw_before(ax)
        nx.draw(
            graph,
            pos = self.graph_layout,
            ax = ax,
            edgecolors='black',
            node_color = color_map,
            node_size=[ v * 10 for v in dict(graph.degree).values()],
            edge_color='gray'
        )
        if self.show_legend:
            self._add_legends(states, color_order)
        if draw_after != None:
            draw_after(ax)
        if self.show_in_window:
            canvas = FigureCanvas(self.figure)
            canvas.draw()
            cv2.imshow(
                "img",
                mat=cv2.cvtColor(np.uint8(canvas.renderer.buffer_rgba()), cv2.COLOR_BGR2RGB)
            )
            cv2.waitKey(5)  # it's needed, but no problem, it won't pause/wait
        else:
            self.figure.savefig('%s%d.png' % (self.temp_save_location, self.part))
        self.figure.clf()
        self.part += 1

    def end_set_processing(self, data = {}):
        ''' Signal that processing has ended for a set of parameters. '''
        self.part = 0
        #TODO: change filename when starting new one

    def end_step_processing(self, data = {}):
        ''' Signal that processing has ended for a step of a set of parameters. '''
        import time
        time.sleep(5)
        if not self.show_in_window:
            self._create_gif()
        self.part = 0
        self.save_number += 1
        self.step += 1
        self.graph_layout = None # Reset layout

    def _get_color_map(self, network, model):
        color_map = []
        states = {}
        i = 0
        for state in model.get_states():
            states[state] = [0, i] # count and index
            i += 1
        # TODO: make colors possible in parameters
        color_order = self._get_default_colors(len(states))
        for node in network:
            state = network.get_node_state(node)
            color_map.append(color_order[states[state][1]])
            states[state][0] += 1
        return [color_map, states, color_order]

    def _get_default_colors(self, n):
        ''' Get colors from a premade list of colors up to 10 different colors. '''
        if n > len(self.default_colors):
            raise Exception('More states than the default colors. Please provide the colors that you want for each state.')
        return self.default_colors[0:n]
    
    def _add_legends(self, states, color_order):
        #TODO: show simulation step and combination step visually
        legend = []
        for state in states: 
            legend.append(
                Line2D(
                    [0], 
                    [0], 
                    marker='o', 
                    color='w', 
                    label='%s (%s)' %(state, str(states[state][0])),
                    markerfacecolor=color_order[states[state][1]], 
                    markersize=15
                ),
            )
        self.figure.gca().legend(
            handles=legend, 
            loc=2, 
            prop={'size': 15},
            labelspacing=0.90,
            title_fontsize=15,
            title=('Simulation, step %i\n\ntime step: %i' % ( self.step + 1, self.part + 1 ))
        )

    def _create_gif(self):
        f = []
        for (dirpath, dirnames, filenames) in os.walk(self.temp_save_location):
            f.extend(filenames)
            break
        filenames = list(map(lambda x: int(x[:-4]), f))
        filenames.sort()
        images = []
        for filename in filenames:
            images.append(imageio.imread('%s%i.png' % (self.temp_save_location, filename)))
            os.remove('%s%i.png' % (self.temp_save_location, filename))
        filename_to_save = "%s-%i" % (self.filename, self.save_number)
        print( 'Saved to ' + filename_to_save + '.gif in Media folder' )
        imageio.mimsave('%s%s.gif' % (self.save_location, filename_to_save), images, format='GIF', duration=1/5)