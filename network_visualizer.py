# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QWidget, QGridLayout
from PySide6.QtCore import Slot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import networkx as nx
import numpy as np

class NetworkVisualizer(QtWidgets.QWidget):

    def __init__(self, parent, simulator):

        # TODO: Get clicking working again

        QtWidgets.QWidget.__init__(self)

        grid = QGridLayout()
        self.setLayout(grid)

        self.name = "Memory Network Visualizer"

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        grid.addWidget(self.toolbar, 0, 0)
        grid.addWidget(self.canvas, 1, 0)

        # simulator.setCanvasAndFigure(self.canvas, self.figure)

    def visualize_memory_network(self, clip_space):

        # Produce a visualisation of the agent's memory
        # TODO: Make things clickable

        subsets = dict()
        for stimuli in clip_space.nodes:
            subsets[stimuli] = stimuli[0]
        subsets = {k: subsets[k] for k in list(sorted(subsets.keys()))}

        self.figure.clf()
        
        nx.set_node_attributes(clip_space, subsets, name="layers")
        weight_labels = nx.get_edge_attributes(clip_space, 'weight')

        weights = np.array([weight for weight in weight_labels.values()])
        normalized_weights = {key: ((weight_labels[key] - np.min(weights)) / (np.max(weights) - np.min(weights))) for key in weight_labels.keys()}

        memory_plot = self.figure.add_subplot(111, picker=1)
        
        ordered_clip_space = nx.DiGraph()
        ordered_clip_space.to_directed()
        ordered_clip_space.add_nodes_from(sorted(clip_space.nodes(data=True)), size=10000)
        ordered_clip_space.add_weighted_edges_from(clip_space.edges(data=True))

        pos = nx.multipartite_layout(ordered_clip_space, "layers", align="horizontal", scale=-1)
        print(pos)
        
        nx.draw_networkx_nodes(ordered_clip_space, pos, ax=memory_plot, node_size=500)
        nx.draw_networkx_labels(ordered_clip_space, pos, ax=memory_plot)
        for key, weight in normalized_weights.items():
            nx.draw_networkx_edges(ordered_clip_space,
                                    pos,
                                    connectionstyle='arc3,rad=0.1',
                                    edgelist=[key],
                                    ax=memory_plot,
                                    arrows=True,
                                    alpha=weight,
                                    width=5)

        self.canvas.draw()

    Slot()
    def on_pick(self, event):
        artist = event.artist
        x_mouse, y_mouse = event.mouseevent.xdata, event.mouseevent.ydata
        ax = event.canvas.figure.gca()
        print(ax)
        # x, y = artist.get_xdata(), artist.get_ydata()
        print(str(x_mouse) + '\n' + str(y_mouse))