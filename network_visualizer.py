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

        # self.vis_types = {
        #     "Sequential Layout": True,
        #     "Community Layout": False,
        #     "Multigraph Layout": False
        # }

        self.vis_functions = {
            "Multipartite": self.visualize_sequential_network,
            "Community": self.visualize_community_network
        }

        self.heatmap_edge_colormap = mpl.colormaps['gist_heat_r']

        self.vis_settings = {
            "graph_style": "Community",
            "community_mode": "Greedy Modularity",
            "normalize_weights": True,
            "color_edges": True,
            "softmax_weights": True,
            "min_edge_visibility": 0.25
        }

        self.selected_stim = None

        self.name = "Memory Network Visualizer"

        self.figure = Figure(tight_layout=False)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.grid.addWidget(self.toolbar, 0, 0)
        self.grid.addWidget(self.canvas, 1, 0)

    def update_visualization_type(self, vis_type):

        self.vis_types = dict.fromkeys(self.vis_types, False)
        
        if vis_type in self.vis_types.keys:
            self.vis_types[vis_type] = True

    def update_settings(self, new_settings):

        self.vis_settings = new_settings

    def visualize_network(self, clip_space):
        
        """
        Routes the clip_space to the currently-selected visualizer
        """

        if self.selected_stim is not None:
            self.table.stimEditor.update_clip_space(clip_space)
            self.table.update_editor.emit()

        self.clip_space_backup = clip_space

        self.figure.clf()

        print(self.vis_settings)

        vis_type = self.vis_settings["graph_style"][0]
        print(vis_type)
        self.vis_functions[vis_type](self.clip_space_backup)

        # for vis_type in self.vis_types.keys():
        #     if self.vis_types[vis_type] == self.vis_settings[""]:
        #         self.vis_functions[vis_type](clip_space)

    def generate_groupings(self, clip_space, as_community, as_subsets, use_modularity=True):

        """
        Creates either:

        - Subsets for the multipartite layout
        - Communities for the community layout (with greedy modularity if use_modularity = True,
                                                if false, just group based on class number)
        """

        if as_community:
            if use_modularity:
                return self.community_detection(clip_space)
            else:
                community_dict = {}
                for stimuli in clip_space.nodes:
                    community_dict[stimuli] = int(stimuli[1]) - 1
                return community_dict
        elif as_subsets:
            subsets = {}
            for stimuli in clip_space.nodes:
                subsets[stimuli] = stimuli[0]
            return {k: subsets[k] for k in list(sorted(subsets.keys()))}
            
    def generate_node_color_maps(self, clip_space, subsets=None):

        """
        Creates a dictionary/array which defines the colours of each node
        in the visualization
        """

        if subsets is None:
            color_map  = {}
            for stimuli in clip_space.nodes:
                color_map[stimuli] = (list(mcolors.TABLEAU_COLORS.keys())[int(stimuli[1]) + 3])
        else:
            color_map = []
            for item in subsets.items():
                color_map.append(list(mcolors.TABLEAU_COLORS.keys())[int(item[0][1]) + 3])

        return color_map

    def community_detection(self, clip_space: nx.DiGraph):

        """
        Converts graph into an undirected graph, and uses
        networkx's greedy modularity function to obtain communities
        """

        undirected_clip_space = clip_space.to_undirected()

        for stimuli in clip_space:
            for linked_stim in nx.neighbors(clip_space, stimuli):
                if stimuli in nx.neighbors(clip_space, linked_stim):
                    undirected_clip_space.edges[stimuli, linked_stim]["weight"] = (
                        clip_space.edges[stimuli, linked_stim]['weight'] + clip_space.edges[linked_stim, stimuli]['weight']
                    )

        undirected_communities = nx.community.greedy_modularity_communities(
            undirected_clip_space, "weight", 1, 1, self.environment.num_classes
        )

        community_dict = {}
        for i, community in enumerate(undirected_communities):
            for stimuli in list(community):
                community_dict[stimuli] = i

        return community_dict

    def obtain_normalised_weights(self, clip_space):

        """
        Returns a dictionary of normalised weights from the agent's clip_space
        """
        
        weight_labels = nx.get_edge_attributes(clip_space, 'weight')
        weights = np.array([weight for weight in weight_labels.values()])
        return {key: ((weight_labels[key] - np.min(weights)) / (np.max(weights) - np.min(weights))) for key in weight_labels.keys()}
    
    def create_ordered_clip_space(self, clip_space):

        ordered_clip_space = nx.DiGraph()
        ordered_clip_space.to_directed()
        ordered_clip_space.add_nodes_from(sorted(clip_space.nodes(data=True)))
        ordered_clip_space.add_weighted_edges_from(clip_space.edges(data=True))
        return ordered_clip_space


    def visualize_sequential_network(self, clip_space: nx.DiGraph):

        """
        Called by the simulator, creates a new visualization via three steps:

        1. Separate stimuli into respective classes, and apply colour mappings

        2. Create array of normalised weights used in edge opacity 

        3. Visualise each feature of the network on the provided plot
        """
        # TODO: Re-write above description 

        subsets = self.generate_groupings(clip_space, False, True)
        node_color_map = self.generate_node_color_maps(clip_space, subsets)
        
        nx.set_node_attributes(clip_space, subsets, name="layers")

        if self.vis_settings["normalize_weights"]:
            normalized_weights = self.obtain_normalised_weights(clip_space)

        memory_plot = self.figure.add_subplot(111) #, picker=self.on_pick)
        
        ordered_clip_space = self.create_ordered_clip_space(clip_space)

        pos = nx.multipartite_layout(ordered_clip_space, "layers", align="horizontal", scale=-1)

        nx.draw_networkx_nodes(clip_space, pos, ax=memory_plot, node_size=500, node_color=node_color_map)
        nx.draw_networkx_labels(clip_space, pos, ax=memory_plot, font_color='white')
        # self.edge_artist = []
        weight_counter = 0
        if  self.vis_settings["normalize_weights"]:
            for key, weight in normalized_weights.items():
                nx.draw_networkx_edges(clip_space,
                                        pos,
                                        connectionstyle='arc3,rad=0.1',
                                        edgelist=[key],
                                        ax=memory_plot,
                                        arrows=True,
                                        edge_color=self.heatmap_edge_colormap(weight) if self.vis_settings["color_edges"] else None,
                                        width=2 + (weight * 6),
                                        alpha=max(self.vis_settings["min_edge_visibility"], weight)) #+ (weights[weight_counter] / 8),
                                        #alpha=weight)
            weight_counter += 1
        else:
            nx.draw_networkx_edges(clip_space,
                                   pos,
                                   connectionstyle='arc3,rad=0.1',
                                   ax=memory_plot,
                                   arrows=True,
                                   edge_color=self.heatmap_edge_colormap(weight) if self.vis_settings["color_edges"] else None,
                                   width=2 + (weight * 6),
                                   alpha=max(self.vis_settings["min_edge_visibility"], weight))
            
        # network_cursor = mplcursors.cursor(self.figure)

        # @network_cursor.connect("add")
        # def on_add(sel):
        #     self.table.populateEditor(list(ordered_clip_space.nodes())[sel.index], clip_space)
        #     self.selected_stim = list(ordered_clip_space.nodes())[sel.index]

        #self.main_display.setFixedSize(self.main_display.grid.sizeHint())
        self.canvas.draw()

    def visualize_community_network(self, clip_space):

        """
        Visualizes the agent's memory network via clusters
        of nodes that grow/recede based on relational density
        """

        community_dict = self.generate_groupings(clip_space, True, False,
                                                 True if self.vis_settings["community_mode"] == "Greedy Modularity" else False)
        subsets = self.generate_groupings(clip_space, False, True)
        color_map = self.generate_node_color_maps(clip_space, subsets)
        normalized_weights = self.obtain_normalised_weights(clip_space)

        memory_plot = self.figure.add_subplot(111) #, picker=self.on_pick)

        ordered_clip_space = self.create_ordered_clip_space(clip_space)

        pos = self.community_layout(clip_space, community_dict)

        nx.draw_networkx_nodes(clip_space, pos, node_size=500, node_color=color_map)
        nx.draw_networkx_labels(clip_space, pos, font_color='white')

        if  self.vis_settings["normalize_weights"]:
            weight_counter  = 0
            for key, weight in normalized_weights.items():
                nx.draw_networkx_edges(clip_space,
                                        pos,
                                        connectionstyle='arc3,rad=0.1',
                                        edgelist=[key],
                                        ax=memory_plot,
                                        arrows=True,
                                        edge_color=self.heatmap_edge_colormap(weight) if self.vis_settings["color_edges"] else None,
                                        width=2 + (weight * 6),
                                        alpha=max(self.vis_settings["min_edge_visibility"], weight)) #+ (weights[weight_counter] / 8),
                                        #alpha=weight)
                weight_counter += 1
        else:
            nx.draw_networkx_edges(clip_space,
                                   pos,
                                   connectionstyle='arc3,rad=0.1',
                                   ax=memory_plot,
                                   arrows=True,
                                   edge_color=self.heatmap_edge_colormap(weight) if self.vis_settings["color_edges"] else None,
                                   width=2 + (weight * 6),
                                   alpha=max(self.vis_settings["min_edge_visibility"], weight))
            
        self.canvas.draw()
        

# COMMUNITY-MAKING FUNCTIONS BELOW
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------        

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