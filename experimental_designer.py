from PySide6 import QtCore, QtWidgets 

import EEPS.initialization
import EEPS.initialization_detail

import networkx as nx
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

"""
experiment_designer.py (WOP)

Provides an interface for creating new experimental designs.
Users should have the ability to use pre-exisiting designs
as templates for new designs
"""

class ExperimentDesigner(QtWidgets.QWidget):

    def __init__(self):
        super.__init__()

        plot_blocks = EEPS.initialization_detail.environment_parameters_details(EEPS.initialization.environment_parameters['environment_ID'][0])
        #self.generate_training_structure(plot_blocks)
    

def generate_training_structure(plot_blocks):

    for i, plot_block in enumerate(plot_blocks):
        print(plot_block)


plot_blocks = EEPS.initialization_detail.environment_parameters_details(EEPS.initialization.environment_parameters()['environment_ID'][0])
print(plot_blocks)
#generate_training_structure(plot_blocks)