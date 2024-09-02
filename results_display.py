# UI Modules
from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QHBoxLayout
from PySide6.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import EEPS.interaction

class ResultsDisplay(QtWidgets.QWidget):

    def __init__(self, main, simulator, rdt_volume, rdt_density):

        QtWidgets.QWidget.__init__(self)
        self.simulator = simulator
        self.results_layout = QHBoxLayout()
        self.main_display = main
    
        self.visual_grid = QGridLayout()

        self.figure = Figure(tight_layout=False)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.figure_id = 0

        self.createButtons()

        self.visual_grid.addWidget(self.toolbar, 0, 0)
        self.visual_grid.addWidget(self.canvas, 1, 0)

        self.results_layout.addWidget(self.backButton)
        self.results_layout.addLayout(self.visual_grid)
        self.results_layout.addWidget(self.forwardButton)

        self.setLayout(self.results_layout)

        self.display_results(rdt_volume, rdt_density)

    def createButtons(self):

        self.forwardButton = QPushButton(self)
        self.forwardButton.setText(">")
        self.forwardButton.clicked.connect(lambda: self.switch_figure(self.figure_id + 1))
        #self.forwardButton.setIcon()
        #self.forwardButton.clicked.connect()

        self.backButton = QPushButton(self)
        self.backButton.setText("<")
        self.backButton.clicked.connect(lambda: self.switch_figure(self.figure_id - 1))

        # SP_ArrowForward, SP_ArrowBack

    def switch_figure(self, value):

        self.figure.clf()
        self.r_ax = self.figure.add_subplot(111)

        if value >= 0 and value < len(self.results):
            if self.results[value]['type'] == 'bar':
                self.results[value]['result'].plot(kind='bar',
                                                color = ['royalblue','lightgreen', 'red','cyan'], 
                                                ax=self.r_ax)
                self.r_ax.legend(fontsize = 20)
                self.r_ax.tick_params(labelsize = 20)
                self.r_ax.set_title(self.results[value]['name'], fontsize = 20)
                self.r_ax.set_ylabel('Correct match ratio', fontsize = 20)
                self.figure.tight_layout()

                # This one below doesn't seem to have a corresponding function with the canvas

                #self.r_ax( rotation=45, fontsize = 18, horizontalalignment = 'right')
            elif self.results[value]['type'] == 'heatmap':
                sns.heatmap(self.results[value]['result'].round(3),xticklabels=True, yticklabels=True, annot = True,
                        annot_kws = {"size": 14}, linewidths =.15, fmt="g", cmap="Blues", ax=self.r_ax) # cmap="Greens"
                self.r_ax.set_title(self.results[value]['name'], fontsize = 16)
                self.r_ax.tick_params(labelsize = 16)
                self.figure.tight_layout()
            elif self.results[value]['type'] == 'line':
                for i in range(len(self.results[value]['result'])):
                    self.r_ax.plot(self.results[value]['result'][i], label=("Class " + str(i + 1)))
                self.r_ax.legend(fontsize = 20)
                self.r_ax.tick_params(labelsize = 20)
                self.r_ax.set_title(self.results[value]['name'], fontsize = 20)
            self.canvas.draw()
            #self.main_display.setFixedSize(self.main_display.grid.sizeHint())
            self.figure_id = value
        

    def display_results(self, rdt_volume, rdt_density):

        self.filename = self.simulator.file_name

        self.obtain_and_organise_data(rdt_volume, rdt_density)

        self.switch_figure(self.figure_id)

        self.canvas.draw()

    def obtain_and_organise_data(self, rdt_volume, rdt_density):

        resultFile = open(self.filename, 'rb')
        self.data = pickle.load(resultFile)
        resultFile.close()

        self.results = []

        for i in range(len(self.data['show'])):

            result = {}
            result['result'] = self.data['result'][self.data['show'][i][0]]
            result['type'] = self.data['show'][i][1]
            result['name'] = self.data['show'][i][0] + '_' + result['type']
            self.results.append(result)

        self.add_rdt_data(rdt_volume, rdt_density)

    def add_rdt_data(self, rdt_volume, rdt_density):

        result = {}
        result['result'] = rdt_volume
        result['type'] = 'line'
        result['name'] = "Relational volume over sim"
        self.results.append(result)
        
        result = {}
        result['result'] = rdt_density
        result['type'] = 'line'
        result['name'] = "Relational density over sim"
        self.results.append(result)

        result = {}
        r_mass = []
        for i in range(len(rdt_density)):
            r_mass.append(np.multiply(rdt_density[i], rdt_volume[i]))
        result['result'] = r_mass
        result['type'] = 'line'
        result['name'] = "Relational mass over sim"
        self.results.append(result)





        
        



