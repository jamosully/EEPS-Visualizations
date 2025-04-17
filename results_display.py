# UI Modules
from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QHBoxLayout
from PySide6.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as mtrans
import pandas as pd
import seaborn as sns
import pickle
import EEPS.interaction

"""
results_display.py

At the end of an experiment, this script is leveraged
to provide an additional tab in the display of Affinity
which displays result visualisations provided in the original 
version of EEPS and new RDT visualisations
"""

class ResultsDisplay(QtWidgets.QWidget):

    """
    Tab for displaying results at the end of an experiment
    """

    def __init__(self, main, simulator, rdt_volume, rdt_density):

        QtWidgets.QWidget.__init__(self)
        self.simulator = simulator
        self.resultsLayout = QHBoxLayout()
        self.mainDisplay = main
    
        self.visualGrid = QGridLayout()

        self.figure = Figure(tight_layout=False)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.figure_id = 0

        self.createButtons()

        self.visualGrid.addWidget(self.toolbar, 0, 0)
        self.visualGrid.addWidget(self.canvas, 1, 0)

        self.resultsLayout.addWidget(self.backButton)
        self.resultsLayout.addLayout(self.visualGrid)
        self.resultsLayout.addWidget(self.forwardButton)

        self.setLayout(self.resultsLayout)

        self.displayResults(rdt_volume, rdt_density)

    def createButtons(self):

        """
        Buttons which allow a user to switch which visualisation
        is displayed
        """

        self.forwardButton = QPushButton(self)
        self.forwardButton.setText(">")
        self.forwardButton.clicked.connect(lambda: self.switchFigure(self.figure_id + 1))

        self.backButton = QPushButton(self)
        self.backButton.setText("<")
        self.backButton.clicked.connect(lambda: self.switchFigure(self.figure_id - 1))


    def switchFigure(self, value):

        """
        Generates each graph visualisation

        The majority of this code is lifted from the original
        version of EEPS
        """

        self.figure.clf()
        self.r_ax = self.figure.add_subplot(111)
        self.r_ax = self.figure.axes[0]
        self.r_ax.axis("auto")
        self.r_ax.set_autoscale_on(True)

        if value >= 0 and value < len(self.results):
            if self.results[value]['type'] == 'bar':
                self.results[value]['result'].plot(kind='bar',
                                                color = ['royalblue','lightgreen', 'red','cyan'], 
                                                ax=self.r_ax)
                self.r_ax.legend(fontsize = 20)
                self.r_ax.tick_params(labelsize = 20)
                self.r_ax.set_title(self.results[value]['name'], fontsize = 20)
                self.r_ax.set_ylabel('Correct match ratio', fontsize = 20)

                # This one below doesn't seem to have a corresponding function with the canvas

                #self.r_ax( rotation=45, fontsize = 18, horizontalalignment = 'right')
            elif self.results[value]['type'] == 'heatmap':
                sns.heatmap(self.results[value]['result'].round(3),xticklabels=True, yticklabels=True, annot = True,
                        annot_kws = {"size": 7}, linewidths =.15, fmt="g", cmap="Blues", ax=self.r_ax) # cmap="Greens"
                self.r_ax.set_title(self.results[value]['name'])
                self.r_ax.tick_params(labelsize = 16)
            elif self.results[value]['type'] == 'line':
                if isinstance(self.results[value]['result'], dict):
                   line_df = pd.DataFrame.from_dict(self.results[value]['result'])
                   self.r_ax.plot(line_df, label=line_df.columns, linewidth=3)
                   self.r_ax.legend(fontsize = 5)
                   self.r_ax.set_yscale('log')
                else:
                    line_df = pd.DataFrame(self.results[value]['result']).T
                    line_df.columns = line_df.columns.get_level_values(0)
                    for i in range(len(self.results[value]['result'])):
                        offset = mtrans.offset_copy(self.r_ax.transData, fig=self.figure, y=(4 * i), units="points")
                        self.r_ax.plot(self.results[value]['result'][i], label=("Class " + str(i + 1)), 
                                    alpha=0.8, linewidth=4, transform=offset)
                    self.r_ax.set_ylim(line_df.min().min() - (np.mean(line_df) / 2), line_df.max().max() + (np.mean(line_df) / 2))  
                    self.r_ax.set_xlim(-25, len(self.results[value]['result'][i]) + 50) 
                    self.r_ax.legend(fontsize = 20)
                self.r_ax.tick_params(labelsize = 20)
                self.r_ax.autoscale_view()
                self.r_ax.set_title(self.results[value]['name'])
            elif self.results[value]['type'] == 'boxplot':
                self.r_ax.boxplot(list(self.results[value]['result'].values()), labels=list(self.results[value]['result'].keys()))
                self.r_ax.set_title(self.results[value]['name'])
                self.r_ax.set_ylabel("Pearson Correlation Coefficient Value")
                self.figure.autofmt_xdate(rotation=45)
            self.canvas.draw()
            self.figure_id = value
        

    def displayResults(self, rdt_volume, rdt_density):

        self.filename = self.simulator.file_name

        self.obtain_and_organise_data(rdt_volume, rdt_density)

        self.switchFigure(self.figure_id)

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

        # Each array will need padding with an array

        for volume in rdt_volume.keys():
            volume_result = {}
            volume_result['result'] = np.mean(self.pad_rdt_data(rdt_volume[volume]), axis=0)
            print(len(volume_result['result']))
            volume_result['type'] = 'line'
            volume_result['name'] = "Relational volume (" + volume + ") during simulation"
            self.results.append(volume_result)
            
        for density in rdt_density.keys():
            density_result = {}
            density_result['result'] = np.mean(self.pad_rdt_data(rdt_density[density]), axis=0)
            density_result['type'] = 'line'
            density_result['name'] = "Relational density (" + density + ") during simulation"
            self.results.append(density_result)
        
        p_coef = {}
        all_masses = {}
        for volume_mes in rdt_volume.keys():
            for density_mes in rdt_density.keys():

                # Calculate relational mass using the two measures of volumen and density

                cum_mass = []
                r_mass = []
                result = {}
                mean_vol = np.mean(self.pad_rdt_data(rdt_volume[volume_mes]), axis=0)
                mean_dens = np.mean(self.pad_rdt_data(rdt_density[density_mes]), axis=0)
                for i in range(len(mean_vol)):
                    r_mass.append(np.multiply(mean_vol[i], mean_dens[i]))
                result['result'] = r_mass
                result['type'] = 'line'
                result['name'] = "Relational mass (volume = " + volume_mes + ", density = " + density_mes + ") during simulation"
                self.results.append(result)
                all_masses[("Rv = " + volume_mes + ", Rp = " + density_mes)] = (np.mean(r_mass, axis=0))
                

                # Calculate Pearson's correlation coefficient

                coefs = []
                for j in range(len(mean_vol)):
                    coef = (np.corrcoef(mean_vol[j], mean_dens[j])[0,1])
                    coefs.append(coef)
                coef_name = "Rv = " + volume_mes + ", Rp = " + density_mes
                p_coef[coef_name] = coefs

        for mass in p_coef.keys():
            print(mass + ":" + str(np.mean(p_coef[mass])))

        result = {}
        result['result'] = all_masses
        result['type'] = 'line'
        result['name'] = "Relational mass during simulation"
        self.results.append(result)
        
        result = {}
        result['result'] = p_coef
        result['type'] = 'boxplot'
        result['y_label'] = 'Correlation Coefficient'
        result['name'] = "Pearsons correlation coefficients for relational volume and density combinations"
        self.results.append(result)

    def pad_rdt_data(self, rdt_data):

        padding_length = 0
        for x in range(len(rdt_data)):
            if len(max(rdt_data[x], key=len)) > padding_length:
                padding_length = len(max(rdt_data[x], key=len))

        for i in range(len(rdt_data)):
            for j in range(len(rdt_data[i])):
                if len(rdt_data[i][j]) < padding_length:
                    rdt_data[i][j] = np.pad(rdt_data[i][j], (0, padding_length - len(rdt_data[i][j])), 'edge')

        return rdt_data


        
        



