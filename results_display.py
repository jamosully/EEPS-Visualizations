# UI Modules
from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QHBoxLayout
from PySide6.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import numpy as np
import pickle
import EEPS.interaction

class ResultsDisplay(QtWidgets.QWidget):

    def __init__(self, simulator):

        QtWidgets.QWidget.__init__(self)
        self.simulator = simulator
        self.results_layout = QHBoxLayout()
    
        self.visual_grid = QGridLayout()

        self.canvas = FigureCanvas()
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.figure_id = 0

        self.createButtons()

        self.visual_grid.addWidget(self.toolbar, 0, 0)
        self.visual_grid.addWidget(self.canvas, 1, 0)

        self.results_layout.addWidget(self.backButton)
        self.results_layout.addLayout(self.visual_grid)
        self.results_layout.addWidget(self.forwardButton)

        self.setLayout(self.results_layout)

        self.display_results()

    def createButtons(self):

        self.forwardButton = QPushButton(self)
        self.forwardButton.setText(">")
        self.forwardButton.clicked.connect(lambda: self.switch_figure(1))
        #self.forwardButton.setIcon()
        #self.forwardButton.clicked.connect()

        self.backButton = QPushButton(self)
        self.backButton.setText("<")
        self.backButton.clicked.connect(lambda: self.switch_figure(-1))

        # SP_ArrowForward, SP_ArrowBack

    def switch_figure(self, value):

        print("changing figure")
        if self.figure_id >= 0 and self.figure_id <= (self.num_plots - 1):
            print("correct")
            self.figure_id += value
            #self.canvas.= self.figures[self.figure_id]

    def display_results(self):

        self.filename = self.simulator.file_name
        self.results_runner = EEPS.interaction.Plot_results(self.filename)

        self.num_plots = self.obtain_plot_num()
        self.figures = []
        self.plots = []

        for i in range(self.num_plots):
            fig = Figure()
            plot = fig.add_subplot(111)
            self.figures.append(fig)
            self.plots.append(plot)

        self.results_runner.showResults(self.plots)

        self.canvas.figure = self.figures[0]

        self.canvas.draw()

    def obtain_plot_num(self):

        resultFile = open(self.filename, 'rb')
        data = pickle.load(resultFile)
        resultFile.close()
        return len(data['show'])




        
        



