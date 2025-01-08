# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QGroupBox, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import EEPS.initialization
import EEPS.initialization_detail
import numpy as np
import networkx as nx
import itertools

class RDTVisualizer(QtWidgets.QWidget):

    """
    Records relational density theory data in real-time
    (density, volume, mass)
    """

    def __init__(self, parent, simulator, env_params):
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
        print(self.plot_blocks)

        if not self.plot_blocks:
            self.relation_types_available = False # Have to rely on training order instead
            self.obtain_direct_relations()
        else:
            self.relation_types_available = True
            self.relation_types = self.plot_blocks['relation_type']

        print(self.relation_types)

        self.rdt_volume = []
        self.rdt_density = []

        self.num_classes = EEPS.initialization_detail.environment_parameters_details(self.env_params["environment_ID"][0])[0]      
        for i in range(self.num_classes):
            self.rdt_volume.append([])
            self.rdt_density.append([])

        self.grid.addWidget(self.toolbar, 0, 0)
        self.grid.addWidget(self.canvas, 2, 0)

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
        
        self.grid.addLayout(self.classLayout, 1, 0)

    def visualizeClass(self):

        self.class_id = int(self.sender().objectName()[6]) - 1
        print(self.class_id)
        self.visualize_rdt_data(self.simulator.agent.clip_space)

    def visualize_rdt_data(self, clip_space):

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

        volume_plot.plot(self.rdt_volume[self.class_id])
        density_plot.plot(self.rdt_density[self.class_id])
        mass_plot.plot(np.multiply(self.rdt_volume[self.class_id], self.rdt_density[self.class_id]))

        volume_plot.set(ylabel="Relational Volume")
        density_plot.set(ylabel="Relational Density")
        mass_plot.set(ylabel="Relational Mass")

        self.canvas.draw()

    def track_rdt_data(self, clip_space: nx.DiGraph):
        
        rdt_volume_count = []
        rdt_density_value = []
        rdt_edge_count = []
        rdt_h_vectors = []

        # Nodal distance = number of nodes that link two stimuli
        #                  that are not related by direct training
        
        for i in range(self.num_classes):
            rdt_volume_count.append(0)
            rdt_density_value.append(0)
            rdt_edge_count.append(0)
            rdt_h_vectors.append([])

        for edge in clip_space.edges(data=True):
            if edge[0][1] == edge[1][1]:
                rdt_h_vectors[(int(edge[0][1]) - 1)].append(edge[2]['weight'])
                rdt_edge_count[(int(edge[0][1]) - 1)] += 1

        distances = dict(nx.all_pairs_shortest_path_length(clip_space))

        for stimulus in distances:
            for action in distances[stimulus]:
                relation_pair = stimulus[0] + action[0]
                if relation_pair in self.relation_types['Baseline']:
                    continue
                elif stimulus[1] == action[1]:
                    rdt_volume_count[int(stimulus[1]) - 1] += distances[stimulus][action]

        for i in range(len(rdt_h_vectors)):
            if not rdt_h_vectors[i]:
                rdt_density_value[i] = 0
            else:
                rdt_density_value[i] = np.mean(self.simulator.agent.softmax(rdt_h_vectors[i],
                                                                        self.simulator.agent.beta_h)) / rdt_edge_count[i]

        for i in range(self.num_classes):
            self.rdt_volume[i].append(rdt_volume_count[i])
            self.rdt_density[i].append(rdt_density_value[i])

        