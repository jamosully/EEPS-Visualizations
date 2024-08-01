# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QGroupBox, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import EEPS.initialization
import EEPS.initialization_detail
import numpy as np

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

        self.rdt_volume = []
        self.rdt_density = []
        self.num_classes = EEPS.initialization_detail.environment_parameters_details(EEPS.initialization.environment_parameters()["environment_ID"][0])[0]
        for i in range(self.num_classes):
            self.rdt_volume.append([])
            self.rdt_density.append([])

        self.grid.addWidget(self.canvas, 1, 0)

    def createClassButtons(self, num_classes):

        # self.button_group_box = QGroupBox()
        self.class_layout = QHBoxLayout()

        def addToLayout(button, layout):
            self.class_layout.addWidget(button)
            self.class_layout.setSpacing(10)
            # self.button_group_box.setLayout(layout)

        self.class_dict = {}

        for i in range(num_classes):
            button_name = "Class " + str(i + 1)
            button = QPushButton(button_name)
            button.setObjectName(button_name)
            self.class_dict[button.objectName] = i
            print(i)
            addToLayout(button, self.class_layout)
            button.clicked.connect(self.visualizeClass)
        
        self.grid.addLayout(self.class_layout, 0, 0)

    def visualizeClass(self):

        self.class_id = int(self.sender().objectName()[6]) - 1
        print(self.class_id)
        self.visualize_rdt_data(self.simulator.clip_space)
        # self.simulator.agent.visualize_rdt_data(self.canvas, 
        #                                         self.figure, 
        #                                         self.class_id, 
        #                                         self.simulator.interaction.rdt_volume[self.class_id], 
        #                                         self.simulator.interaction.rdt_density[self.class_id])

    def visualize_rdt_data(self, clip_space):

        # Relational Volume = Number of relations contained within the network
        #                     Total area of network
        #                     OR number of nodes
        # Relational Density = Strength of various relations contained in the network
        #                      Perimiter of network/volume
        #                      OR strength of relations (SUM)

        self.figure.clf()

        volume_plot = self.figure.add_subplot(311)
        density_plot = self.figure.add_subplot(312)
        mass_plot = self.figure.add_subplot(313)

        self.track_rdt_data(clip_space)

        volume_plot.plot(self.rdt_volume[self.class_id])
        density_plot.plot(self.rdt_density[self.class_id])
        mass_plot.plot(np.multiply(self.rdt_volume[self.class_id], self.rdt_density[self.class_id]))

        self.canvas.draw()

    def track_rdt_data(self, clip_space):

        # TODO: Figure out how to calculate densities
        
        rdt_volume_count = []
        rdt_density_value = []

        # print(clip_space.edges(data=True))
        
        for i in range(self.num_classes):
            rdt_volume_count.append(0)
            rdt_density_value.append(0)

        for edge in clip_space.edges(data=True):
            if edge[0][1] == edge[1][1]:
                rdt_volume_count[(int(edge[0][1]) - 1)] += 1
                rdt_density_value[(int(edge[0][1]) - 1)] += edge[2]['weight']

        for i in range(self.num_classes):
            self.rdt_volume[i].append(rdt_volume_count[i])
            self.rdt_density[i].append(rdt_density_value[i])

        