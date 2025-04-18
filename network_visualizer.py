# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QGridLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.colors as mcolors
import matplotlib as mpl

import networkx as nx
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

        self.selected_stim = None

        self.name = "Memory Network Visualizer"

        self.figure = Figure(tight_layout=False)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.grid.addWidget(self.toolbar, 0, 0)
        self.grid.addWidget(self.canvas, 1, 0)

    def visualize_memory_network(self, clip_space):

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
        color_map = []
        for stimuli in clip_space.nodes:
            subsets[stimuli] = stimuli[0]
        subsets = {k: subsets[k] for k in list(sorted(subsets.keys()))}

        for item in subsets.items():
            color_map.append(list(mcolors.TABLEAU_COLORS.keys())[int(item[0][1]) + 3])

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

        pos = nx.multipartite_layout(ordered_clip_space, "layers", align="horizontal", scale=-1)

        nx.draw_networkx_nodes(ordered_clip_space, pos, node_color=color_map, ax=memory_plot, node_size=500)
        nx.draw_networkx_labels(ordered_clip_space, pos, ax=memory_plot, font_color='white')
        self.edge_artist = []
        weight_counter = 0
        for key, weight in normalized_weights.items():
            nx.draw_networkx_edges(ordered_clip_space,
                                    pos,
                                    connectionstyle='arc3,rad=0.1',
                                    edgelist=[key],
                                    ax=memory_plot,
                                    arrows=True,
                                    edge_color=edge_color_map(weight),
                                    width=2 + (weight * 6),
                                    alpha=max(0.33, weight)) #+ (weights[weight_counter] / 8),
                                    #alpha=weight)
            weight_counter += 1
            
        network_cursor = mplcursors.cursor(self.figure)

        @network_cursor.connect("add")
        def on_add(sel):
            self.table.populateEditor(list(ordered_clip_space.nodes())[sel.index], clip_space)
            self.selected_stim = list(ordered_clip_space.nodes())[sel.index]

        #self.main_display.setFixedSize(self.main_display.grid.sizeHint())
        self.canvas.draw()