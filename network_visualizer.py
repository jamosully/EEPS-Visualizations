# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QGridLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.colors as mcolors
import matplotlib as mpl
import matplotlib.animation

import networkx as nx
import netgraph
import numpy as np
import mplcursors

"""
network_visualizer.py

Creates graph network visualisations of an agent's
clip-space via networkx and matplotlib. Also leverages
mplcursors, letting users select stimuli in the view
and modify their connected edge weights via the
stimuli editor
"""

class NetworkVisualizer(QtWidgets.QWidget):

    """
    Visualiser for graph networks
    """

    def __init__(self, parent, table, simulator):

        QtWidgets.QWidget.__init__(self)

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.main_display = parent
        self.table = table

        self.vis_types = {
            "Sequential Layout": True,
            "Community Layout": False,
            "Multigraph Layout": False
        }

        self.selected_stim = None

        self.name = "Memory Network Visualizer"

        self.figure = Figure(tight_layout=False)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.grid.addWidget(self.toolbar, 0, 0)
        self.grid.addWidget(self.canvas, 1, 0)

    def visualize_network(self, clip_space):
        
        """
        Routes the clip_space to the currently-selected visualizer
        """

        

    def visualize_network_networkx(self, clip_space, as_community):

        """
        Called by the simulator, creates a new visualization via three steps:

        1. Separate stimuli into respective classes, and apply colour mappings

        2. Create array of normalised weights used in edge opacity 

        3. Visualise each feature of the network on the provided plot
        """

        if self.selected_stim is not None:
            self.table.stimEditor.update_clip_space(clip_space)
            self.table.update_editor.emit()

        # colours = [(1,1,1), (0,0,0), (0.85,0,0)]
        # edge_color_map = LinearSegmentedColormap.from_list("edge_colours", colours, 1000)
        edge_color_map = mpl.colormaps['gist_heat_r']

        subsets = dict()
        community_dict = {}
        color_map = {}
        color_map_array = []
        for stimuli in clip_space.nodes:
            community_dict[stimuli] = int(stimuli[1]) - 1
            color_map[stimuli] = (list(mcolors.TABLEAU_COLORS.keys())[int(stimuli[1]) + 3])
            subsets[stimuli] = stimuli[0]
        subsets = {k: subsets[k] for k in list(sorted(subsets.keys()))}
                
        for item in subsets.items():
            color_map_array.append(list(mcolors.TABLEAU_COLORS.keys())[int(item[0][1]) + 3])


        self.figure.clf()
        
        nx.set_node_attributes(clip_space, subsets, name="layers")

        weight_labels = nx.get_edge_attributes(clip_space, 'weight')

        weights = np.array([weight for weight in weight_labels.values()])
        normalized_weights = {key: ((weight_labels[key] - np.min(weights)) / (np.max(weights) - np.min(weights))) for key in weight_labels.keys()}

        memory_plot = self.figure.add_subplot(111) #, picker=self.on_pick)
        #memory_plot.set_facecolor('1') 
        
        ordered_clip_space = nx.DiGraph()
        ordered_clip_space.to_directed()
        ordered_clip_space.add_nodes_from(sorted(clip_space.nodes(data=True)))
        ordered_clip_space.add_weighted_edges_from(clip_space.edges(data=True))

        # pos = nx.multipartite_layout(ordered_clip_space, "layers", align="horizontal", scale=-1)
        # pos = nx.spring_layout(clip_space)#
        # pos = self.community_layout(clip_space, community_dict)

        # nx.draw_networkx_nodes(clip_space, pos, ax=memory_plot, node_size=500)
        # nx.draw_networkx_labels(clip_space, pos, ax=memory_plot, font_color='white')
        # self.edge_artist = []
        # weight_counter = 0
        # for key, weight in normalized_weights.items():
        #     nx.draw_networkx_edges(clip_space,
        #                             pos,
        #                             connectionstyle='arc3,rad=0.1',
        #                             edgelist=[key],
        #                             ax=memory_plot,
        #                             arrows=True,
        #                             edge_color=edge_color_map(weight),
        #                             width=2 + (weight * 6),
        #                             alpha=max(0.33, weight)) #+ (weights[weight_counter] / 8),
        #                             #alpha=weight)
        #     weight_counter += 1
            
        # network_cursor = mplcursors.cursor(self.figure)

        # @network_cursor.connect("add")
        # def on_add(sel):
        #     self.table.populateEditor(list(ordered_clip_space.nodes())[sel.index], clip_space)
        #     self.selected_stim = list(ordered_clip_space.nodes())[sel.index]

        netgraph.Graph(clip_space,
                       node_color=color_map, node_edge_width=0, edge_alpha=normalized_weights,
                       node_layout="community", node_layout_kwargs=dict(node_to_community=community_dict),
                       edge_layout="bundled", edge_layout_kwargs=dict(k=2000),
                       ax=memory_plot, arrows=True, node_labels=True)

        #self.main_display.setFixedSize(self.main_display.grid.sizeHint())
        self.canvas.draw()

    def visualize_community_network(self, clip_space):

        """
        Visualizes the agent's memory network via clusters
        of nodes that 
        """

    def community_layout(self, g, partition):
        """
        Compute the layout for a modular graph.


        Arguments:
        ----------
        g -- networkx.Graph or networkx.DiGraph instance
            graph to plot

        partition -- dict mapping int node -> int community
            graph partitions

        weights -- array containing edge weights

        Returns:
        --------
        pos -- dict mapping int node -> (float x, float y)
            node positions

        """

        pos_communities = self._position_communities(g, partition, scale=3., seed=1)

        pos_nodes = self._position_nodes(g, partition, scale=1., seed=1)

        # combine positions
        pos = dict()
        for node in g.nodes():
            pos[node] = pos_communities[node] + pos_nodes[node]

        return pos

    def _position_communities(self, g, partition, **kwargs):

        # create a weighted graph, in which each node corresponds to a community,
        # and each edge weight to the number of edges between communities
        between_community_edges = self._find_between_community_edges(g, partition)

        communities = set(partition.values())
        hypergraph = nx.DiGraph()
        hypergraph.add_nodes_from(communities)
        for (ci, cj), edges in between_community_edges.items():
            hypergraph.add_edge(ci, cj, weight=len(edges))

        # find layout for communities
        pos_communities = nx.spring_layout(hypergraph, **kwargs)

        # set node positions to position of community
        pos = dict()
        for node, community in partition.items():
            pos[node] = pos_communities[community]

        return pos

    def _find_between_community_edges(self, g, partition):

        edges = dict()

        for (ni, nj) in g.edges():
            ci = partition[ni]
            cj = partition[nj]

            if ci != cj:
                try:
                    edges[(ci, cj)] += [(ni, nj)]
                except KeyError:
                    edges[(ci, cj)] = [(ni, nj)]

        return edges

    def _position_nodes(self, g, partition, **kwargs):
        """
        Positions nodes within communities.
        """

        communities = dict()
        for node, community in partition.items():
            try:
                communities[community] += [node]
            except KeyError:
                communities[community] = [node]

        pos = dict()
        for ci, nodes in communities.items():
            subgraph = g.subgraph(nodes)
            pos_subgraph = nx.spring_layout(subgraph, **kwargs)
            pos.update(pos_subgraph)

        return pos