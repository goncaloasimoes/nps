from . import Visualize #pylint: disable=relative-beyond-top-level
import networkx as nx
from matplotlib import lines
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np

# TODO: Needs to be retested and fixed.
''' Visualize or save images of the network with its various communities represented. '''
class VisualizeCommunities(Visualize.Visualize):

    def process(self, data = {}):
        ''' Do nothing. Override saving of state for every step.'''
        pass

    def end_step_processing(self, data = {}):
        self.show_legend = False
        # color_map, states, color_order = self._get_color_map(data['network'], data['model'])
        graph = data['network'].get_graph()
        if self.graph_layout is None:
            self.graph_layout = nx.spring_layout(graph, scale=1, seed=100)
        communities = {frozenset(graph.nodes[v]['community']) for v in graph}
        centers = []
        for community in communities:
            center_x = 0
            center_y = 0
            for node in community:
                center_x += self.graph_layout[node][0]
                center_y += self.graph_layout[node][1]
            center = [
                center_x/len(community),
                center_y/len(community),
            ]
            centers.append(center)
        print(centers)
        centers = np.array(centers)
        print(centers)
        vor = Voronoi(centers)
        self.points = centers
        self.vor = vor
        # for region in vor.regions:
        #     if not -1 in region:
        #         polygon = [vor.vertices[i] for i in region]
        #         plt.fill(*zip(*polygon))
        self.draw( data, draw_before=self.voronoi )
        self.save_number += 1
        self.step += 1
        self.graph_layout = None # Reset layout
    
    def voronoi(self, ax):
        color = 'crimson'
        alpha = 0.7
        #ax.plot(self.points[:,0], self.points[:,1], 'o')
        #ax.plot(self.vor.vertices[:,0], self.vor.vertices[:,1], '*')
        
        lim_x = [0,0]
        lim_y = [0,0]
        for node in self.graph_layout:
            x = self.graph_layout[node][0]
            y = self.graph_layout[node][1]
            if x < lim_x[0]:
                lim_x[0] = x
            if x > lim_x[1]:
                lim_x[1] = x
            if y < lim_y[0]:
                lim_y[0] = y
            if y > lim_y[1]:
                lim_y[1] = y
        padding = 0.1
        ax.set_xlim(lim_x[0] - padding, lim_x[1] + padding); ax.set_ylim(lim_y[0] - padding, lim_y[1] + padding)

        for simplex in self.vor.ridge_vertices:
            simplex = np.asarray(simplex) 
            if np.all(simplex >= 0):
                line = lines.Line2D(self.vor.vertices[simplex,0], self.vor.vertices[simplex,1], lw=2., color=color, linestyle='--', alpha=alpha)
                ax.add_line(line)
                # ax.plot(self.vor.vertices[simplex,0], self.vor.vertices[simplex,1], 'r-', linewidth=1)

        center = self.points.mean(axis=0)
        for pointidx, simplex in zip(self.vor.ridge_points, self.vor.ridge_vertices):
            simplex = np.asarray(simplex)
            if np.any(simplex < 0):
                i = simplex[simplex >= 0][0] # finite end self.Voronoi vertex
                t = self.points[pointidx[1]] - self.points[pointidx[0]] # tangent
                t /= np.linalg.norm(t)
                n = np.array([-t[1], t[0]]) # normal
                midpoint = self.points[pointidx].mean(axis=0)
                far_point = self.vor.vertices[i] + np.sign(np.dot(midpoint - center, n)) * n * 100
                line = lines.Line2D([self.vor.vertices[i,0], far_point[0]], [self.vor.vertices[i,1], far_point[1]], lw=2., color=color, linestyle='--', alpha=alpha)
                line.set_clip_on(False)
                ax.add_line( line)
                # ax.plot([self.vor.vertices[i,0], far_point[0]], [self.vor.vertices[i,1], far_point[1]], 'r--', linewidth=1)
        # voronoi_plot_2d(self.vor,ax=ax, show_vertices = False, show_points=False, line_colors='red')
