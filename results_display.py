# UI Modules
from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import numpy as np
import EEPS.interaction

class ResultsDisplay(QtWidgets.QWidget):

    def __init__(self, simulator):

        QtWidgets.QWidget.__init__(self)
        self.simulator = simulator
        self.results_layout = QHBoxLayout()
    
        grid = QGridLayout()
        self.setLayout(grid)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        grid.addWidget(self.toolbar, 0, 0)
        grid.addWidget(self.canvas, 1, 0)

        self.display_results()

    def createButtons(self):

        self.backButton = QPushButton(self)
        self.forwardButton = QPushButton(self)

        # SP_ArrowForward, SP_ArrowBack

    def display_results(self):

        self.figure.clf()

        self.filename = self.simulator.file_name
        self.results_runner = EEPS.interaction.Plot_results(self.filename)

        self.bar_plot = self.figure.add_subplot(111)

        self.results_runner.showResults(self.bar_plot, None)

        self.canvas.draw()




        
        



