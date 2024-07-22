# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QGroupBox, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import EEPS.initialization_detail

class RDTVisualizer(QtWidgets.QWidget):

    # TODO: Implement RDT view

    def __init__(self, parent, simulator):
        super().__init__()

        self.simulator = simulator
        self.class_id = 0

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.name = "RDT Visualizer"

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.grid.addWidget(self.canvas, 1, 0)

    def createClassButtons(self, num_classes):

        self.button_group_box = QGroupBox()
        layout = QHBoxLayout()

        def addToLayout(button, layout):
            layout.addWidget(button)
            layout.setSpacing(10)
            self.button_group_box.setLayout(layout)

        for i in range(num_classes):
            button_name = "Class " + str(i + 1)
            button = QPushButton(button_name)
            button.setObjectName(button_name)
            addToLayout(button, layout)
            button.clicked.connect(lambda: self.visualizeClass(i))
        
        self.grid.addWidget(self.button_group_box, 0, 0)

    def visualizeClass(self, id):

        self.class_id = id
        self.simulator.agent.visualize_rdt_data(self.canvas, 
                                                self.figure, 
                                                self.class_id, 
                                                self.simulator.interaction.rdt_volume[id], 
                                                self.simulator.interaction.rdt_density[id])

        