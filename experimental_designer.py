from PySide6 import QtCore, QtWidgets 

import EEPS.initialization
import EEPS.initialization_detail

import networkx as nx
import numpy as np

"""
experiment_designer.py (WOP)

Provides an interface for creating new experimental designs.
Users should have the ability to use pre-exisiting designs
as templates for new designs
"""

class ExperimentDesigner(QtWidgets.QWdget):

    def __init__(self):
        super.__init__()

    

    def generate_training_structure(plot_blocks):

        for i, plot_block in enumerate(plot_blocks):
            for i, step in enumerate(plot_block):
                print(step)