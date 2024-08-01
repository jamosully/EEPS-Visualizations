# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QGroupBox, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class HeatmapVisualizer(QtWidgets.QWidget):

    def __init__(self, simulator):
        super.__init__()

        self.simulator = simulator
        self.class_id = 0

        self.grid =  QGridLayout()

        self.setLayout(self.grid)

        self.name = "Heatmap Visualizer"

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.grid.addWidget(self.canvas, 1, 0)

    # TODO: This already exists in the RDT visualizer file,
    #       Maybe create a file for visualizer tools?
    
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
        self.simulator.agent.visualize_rdt_data(self.canvas, 
                                                self.figure, 
                                                self.class_id, 
                                                self.simulator.interaction.rdt_volume[self.class_id], 
                                                self.simulator.interaction.rdt_density[self.class_id])