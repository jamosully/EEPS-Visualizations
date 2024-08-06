# UI Modules
from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget, QGridLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import numpy as np

class ResultsDisplay(QtWidgets.QWidget):

    def __init__(self, simulator):

        QtWidgets.QWidget.__init__(self)
        self.simulator = simulator
    
        grid = QGridLayout()
        self.setLayout(grid)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        grid.addWidget(self.toolbar, 0, 0)
        grid.addWidget(self.canvas, 1, 0)

    def display_results(self):

        self.figure.clf()

        results_plot = self.figure.add_subplot(211)

        results_plot.bar(self.simulator.results)




        
        



