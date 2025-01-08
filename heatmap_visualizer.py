# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QGroupBox, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import seaborn as sns
import networkx as nx
import pandas as pd
from sklearn import preprocessing
import mplcursors

"""
heatmap_visualizer.py

Controls the heatmap visualisation, (currently) via
the seaborn package
"""


class HeatmapVisualizer(QtWidgets.QWidget):

    """
    Heatmap of normalised edge weights
    """

    # TODO: Potentially add toggle for normalised edge weights/probability values
    
    def __init__(self, parent, simulator):
        QtWidgets.QWidget.__init__(self)

        self.simulator = simulator
        self.class_id = 0

        self.grid =  QGridLayout()

        self.setLayout(self.grid)

        self.name = "Heatmap Visualizer"

        self.figure = Figure(tight_layout=False)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.grid.addWidget(self.toolbar, 0, 0)
        self.grid.addWidget(self.canvas, 1, 0)

    # TODO: This already exists in the RDT visualizer file,
    #       Maybe create a file for visualizer tools?
    
    def createClassButtons(self, num_classes):

        self.classLayout = QHBoxLayout()

        def addToLayout(button, layout):
            self.classLayout.addWidget(button)
            self.classLayout.setSpacing(10)

        self.class_dict = {}

        for i in range(num_classes):
            button_name = "Class " + str(i + 1)
            button = QPushButton(button_name)
            button.setObjectName(button_name)
            self.class_dict[button.objectName] = i
            addToLayout(button, self.classLayout)
            button.clicked.connect(self.visualizeClass)
        
        self.grid.addLayout(self.classLayout, 0, 0)

    def visualizeClass(self):
        
        self.class_id = int(self.sender().objectName()[6]) - 1

    def visualize_heatmaps(self, clip_space):

        """
        Visualises normalised edge weights via seaborns
        """

        # TODO: mplcursor doesn't work with seaborn, might change to matplotlib heatmaps

        self.figure.clf()

        scaler = preprocessing.MinMaxScaler()
        heat_df = nx.to_pandas_adjacency(clip_space)
        norm_heat_df = pd.DataFrame(scaler.fit_transform(heat_df), index=heat_df.index, columns=heat_df.columns)
        norm_heat_df = norm_heat_df.reindex(sorted(norm_heat_df.columns), axis=1).sort_index()

        heatmap_plot = self.figure.add_subplot(111, picker=1)
        map = sns.heatmap(norm_heat_df, ax=heatmap_plot)
        heatmap_plot.set(xlabel="Percept Stimuli", ylabel="Action Stimuli")

        heatmap_cursor = mplcursors.cursor(map)

        @heatmap_cursor.connect("add")
        def on_add(sel):
            print(sel)

        self.canvas.draw()