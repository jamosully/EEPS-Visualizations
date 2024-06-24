import sys
import random

# 
# import matplotlib.pyplot as plt

# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QGridLayout, QVBoxLayout, QPushButton, QGroupBox, QSlider
from PySide6.QtCore import Slot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

# EEPS Modules
import initialization
import initialization_detail
import environment as env
import agent as agn
import interaction as intrc
import pdb


class MyWidget(QtWidgets.QWidget):

    NumButtons = [['Initialize Model', 'self.initialize_model'],
                  ['Run Simulation', 'self.run_sim'],
                  ['Continue', 'self.continue_sim']]

    def __init__(self):
        super().__init__()

        # Code sourced from:
        # https://stackoverflow.com/questions/35328916/embedding-a-networkx-graph-into-pyqt-widget
        
        self.setWindowTitle("Affinity.net")

        grid = QGridLayout()
        self.setLayout(grid)
        self.createVerticalGroupBox()
        self.createStepSlider()

        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.verticalGroupBox)
        buttonLayout.addWidget(self.stepslider)

        # control_widget = QWidget(self)
        # control_layout = QGridLayout(control_widget)
        # control_layout.setColumnStretch(1, 1)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas, self)

        grid.addWidget(self.toolbar, 0, 1)
        grid.addWidget(self.canvas, 1, 1, 9, 9)
        grid.addLayout(buttonLayout, 1, 0)

        self.step = 100

        # self.toolbar = NavigationToolbar(canvas, self)

        # main_widget = QWidget(self)
        # main_layout = QHBoxLayout(main_widget)
        # main_layout.setStretch(0, 1)
        # main_layout.addWidget(control_widget)
        # main_layout.addWidget(canvas)

        # self.button = QtGui.QPushButton('Plot')
        # self.button.clicked.connect(self.plot_agent_memory)

        # layout = QtGui.QVBoxLayout()
        # layout.addWidget(self.toolbar)
        # layout.addWidget(self.canvas)
        # layout.addWidget(self.button)
        # self.setLayout(layout)

    def createVerticalGroupBox(self):
        self.verticalGroupBox = QGroupBox()

        layout = QVBoxLayout()
        for i in  self.NumButtons:
            button = QPushButton(i[0])
            button.setObjectName(i[0])
            layout.addWidget(button)
            layout.setSpacing(10)
            self.verticalGroupBox.setLayout(layout)
            button.clicked.connect(eval(i[1]))
    
    def createStepSlider(self):

        # TODO: Improve this, and link it to self.step
        
        self.stepslider = QSlider()
        self.stepslider.tickPosition = QSlider.TickPosition.TicksRight

    Slot()
    def initialize_model(self):

        self.environment_detail = initialization_detail.environment_details()
        self.environment_parameter, self.agent_parameter = initialization.config()

        # TODO: Allow users to upload files
        
        file_name = None

        if file_name == None:
            self.agent = agn.Agent(self.agent_parameter)
            self.environment = env.Environment(self.environment_parameter)
            self.interaction = intrc.Interaction(self.agent, self.environment, self.agent_parameter,
                                                                self.environment_parameter, self.step, self.canvas, self.figure)
            
    Slot()
    def run_sim(self):

        if self.interaction is not None:
            self.interaction.run_save()
            file_name = self.interaction.file_name
            print(file_name)

    Slot()
    def continue_sim(self):

        if self.interaction is not None:
            self.interaction.continue_sim()
        

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())