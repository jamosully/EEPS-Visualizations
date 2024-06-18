import sys
import random

# 
# import matplotlib.pyplot as plt

# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QGridLayout, QVBoxLayout, QPushButton, QGroupBox
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

    NumButtons = [['Run Model', 'self.run_sim()']]

    def __init__(self):
        super().__init__()

        # Code sourced from:
        # https://stackoverflow.com/questions/35328916/embedding-a-networkx-graph-into-pyqt-widget

        self.setWindowTitle("Affinity.net")

        grid = QGridLayout()
        self.setLayout(grid)
        self.createVerticalGroupBox()

        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.verticalGroupBox)

        # control_widget = QWidget(self)
        # control_layout = QGridLayout(control_widget)
        # control_layout.setColumnStretch(1, 1)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        grid.addWidget(self.canvas, 0, 1, 9, 9)
        grid.addLayout(buttonLayout, 0, 0)

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
                button.clicked.connect(i[1])

    @QtCore.Slot()
    def run_sim(self):

        environment_detail = initialization_detail.environment_details()
        environment_parameter, agent_parameter = initialization.config()

        file_name = None

        if file_name == None:
            agent = agn.Agent(agent_parameter, self.canvas)
            environment = env.Environment(environment_parameter)
            interaction = intrc.Interaction(agent, environment, agent_parameter,
                                                                environment_parameter, 100)
            interaction.run_save()
            file_name = interaction.file_name
            print(file_name)
        

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())