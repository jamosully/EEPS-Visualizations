# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QGroupBox, QPushButton, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import EEPS.initialization
import EEPS.initialization_detail
import numpy as np
import networkx as nx
import itertools
import json

class RDTVisualizer(QtWidgets.QWidget):

    """
        Records relational density theory data in real-time
        (density, volume, mass)
    """

    def __init__(self, parent, simulator, env_params, rdt_volume_types, rdt_density_types):
        QtWidgets.QWidget.__init__(self)

        self.simulator = simulator
        self.class_id = 0

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.name = "RDT Visualizer"

        self.figure = Figure(tight_layout=False)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.env_params = env_params
        
        self.plot_blocks = EEPS.initialization_detail.environment_parameters_details(self.env_params["environment_ID"][0])[2]

        if not self.plot_blocks:
            self.relation_types_available = False # Have to rely on training order instead
            self.obtain_direct_relations()
        else:
            self.relation_types_available = True
            self.relation_types = self.plot_blocks['relation_type']

        self.rdt_volume = dict()
        self.rdt_density = dict()

        self.num_classes = EEPS.initialization_detail.environment_parameters_details(self.env_params["environment_ID"][0])[0]

        with open("initialization.json", 'r', encoding='utf8') as init_params:
            self.json_params = json.load(init_params)
        
        self.rdt_vol_types = self.json_params['rdt_volume_types']
        self.rdt_den_types = self.json_params['rdt_density_types']
        self.rdt_vol_type = self.rdt_vol_types[0]
        self.rdt_den_type = self.rdt_den_types[0]
        self.volComboBox = QComboBox()
        self.denComboBox = QComboBox()

        for i, type in enumerate(self.rdt_vol_types):
            self.rdt_volume[type] = []
            self.volComboBox.insertItem(i, type)
            for j in range(self.num_classes):
                self.rdt_volume[type].append([])

        for i, type in enumerate(self.rdt_den_types):
            self.rdt_density[type] = []
            self.denComboBox.insertItem(i, type)
            for j in range(self.num_classes):
                self.rdt_density[type].append([])

        print(self.rdt_volume)

        self.volComboBox.currentIndexChanged.connect(lambda: self.change_volume_type(self.volComboBox.currentText()))
        self.denComboBox.currentIndexChanged.connect(lambda: self.change_density_type(self.denComboBox.currentText()))

        self.grid.addWidget(self.toolbar, 0, 0)
        self.grid.addWidget(self.volComboBox, 0, 1)
        self.grid.addWidget(self.denComboBox, 0, 2)
        self.grid.addWidget(self.canvas, 2, 0, 1, 2)

    def change_volume_type(self, volume_type):

        self.rdt_vol_type = volume_type
        self.visualize_rdt_data()

    def change_density_type(self, density_type):
        
        self.rdt_den_type = density_type
        self.visualize_rdt_data()

    def obtain_direct_relations(self):

        training_order = EEPS.initialization_detail.environment_parameters_details(self.env_params['environment_ID'][0])[1]
        self.relation_types = {"Baseline": []}

        for key in training_order:
            for step in training_order[key]:
                relation = step[0] + step[1]
                self.relation_types["Baseline"].append(relation)

        print(self.relation_types)


    def createClassButtons(self, num_classes):

        # self.button_group_box = QGroupBox()
        self.classLayout = QHBoxLayout()
        self.num_classes = num_classes

        def addToLayout(button, layout):
            self.classLayout.addWidget(button)
            self.classLayout.setSpacing(10)
            # self.button_group_box.setLayout(layout)

        self.class_dict = {}

        for i in range(num_classes):
            button_name = "Class " + str(i + 1)
            button = QPushButton(button_name)
            button.setObjectName(button_name)
            self.class_dict[button.objectName] = i
            addToLayout(button, self.classLayout)
            button.clicked.connect(self.visualizeClass)
        
        self.grid.addLayout(self.classLayout, 1, 0, 1, 2)

    def visualizeClass(self):

        self.class_id = int(self.sender().objectName()[6]) - 1
        print(self.class_id)
        self.visualize_rdt_data(self.simulator.agent.clip_space)

    def visualize_rdt_data(self, clip_space=None):

        # Relational Volume = Number of relations contained within the network
        #                     Total area of network
        #                     OR number of nodes OR nodal distance
        # Relational Density = Strength of various relations contained in the network
        #                      Perimiter of network/volume
        #                      OR strength of relations (SUM)
        #                      OR probability/response accuracy

        self.figure.clf()

        volume_plot = self.figure.add_subplot(311)
        density_plot = self.figure.add_subplot(312)
        mass_plot = self.figure.add_subplot(313)

        #self.track_rdt_data(clip_space)

        volume_plot.plot(self.rdt_volume[self.rdt_vol_type][self.class_id])
        density_plot.plot(self.rdt_density[self.rdt_den_type][self.class_id])
        mass_plot.plot(np.multiply(self.rdt_volume[self.rdt_vol_type][self.class_id], self.rdt_density[self.rdt_den_type][self.class_id]))

        volume_plot.set(ylabel="Relational Volume")
        density_plot.set(ylabel="Relational Density")
        mass_plot.set(ylabel="Relational Mass")

        self.canvas.draw()

    def track_rdt_data(self, clip_space: nx.DiGraph, accuracy_rates):
        
        rdt_edge_count = []
        rdt_h_vectors = []

        # Nodal distance = number of nodes that link two stimuli
        #                  that are not related by direct training
        
        for i in range(self.num_classes):
            rdt_edge_count.append(0)
            rdt_h_vectors.append([])

        for edge in clip_space.edges(data=True):
            if edge[0][1] == edge[1][1]:
                rdt_h_vectors[(int(edge[0][1]) - 1)].append(edge[2]['weight'])
                rdt_edge_count[(int(edge[0][1]) - 1)] += 1

        for key in self.rdt_volume.keys():
            vol_measures = [0] * self.num_classes
            match key:
                case "Nodal distance":
                    distances = dict(nx.all_pairs_shortest_path_length(clip_space))

                    for stimulus in distances:
                        for action in distances[stimulus]:
                            relation_pair = stimulus[0] + action[0]
                            if relation_pair in self.relation_types['Baseline']:
                                continue
                            elif stimulus[1] == action[1]:
                                vol_measures[int(stimulus[1]) - 1] += distances[stimulus][action]

                case "Class size":
                    for node in clip_space.nodes:
                        vol_measures[int(node[1]) - 1] += 1
                case "Number of relations":
                    for edge in clip_space.edges:
                        vol_measures[int(edge[0][1]) - 1] += 1

            for i in range(len(vol_measures)):
                self.rdt_volume[key][i].append(vol_measures[i])

        for key in self.rdt_density.keys():
            den_measures = [0] * self.num_classes
            match key:
                case "Mean softmax":
                    for i in range(len(rdt_h_vectors)):
                        if not rdt_h_vectors[i]:
                            den_measures[i] = 0
                        else:
                            den_measures[i] = np.mean(self.simulator.agent.softmax(rdt_h_vectors[i],
                                                                                    self.simulator.agent.beta_h)) / rdt_edge_count[i]
                case "Class success rate":
                    for i in range(self.num_classes):
                        den_measures[i] = accuracy_rates[i + 1]
                case "Mean h-value":
                    for i in range(self.num_classes):
                        den_measures[i] = np.mean(rdt_h_vectors[i])
            
            for i in range(len(den_measures)):
                self.rdt_density[key][i] = den_measures[i]

        