# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QVBoxLayout, QGroupBox, QPushButton, QSlider
from PySide6.QtCore import Slot

class ButtonPanel(QtWidgets.QWidget):
    
    def __init__(self, parent, simulator, simulator_thread, mutex):
        QtWidgets.QWidget.__init__(self)
        
        self.verticalGroupBox = QGroupBox()
        self.simulator = simulator
        self.main_window = parent
        self.simulator_thread = simulator_thread

        layout = QVBoxLayout()

        def addToLayout(button, layout):
            layout.addWidget(button)
            layout.setSpacing(10)
            self.verticalGroupBox.setLayout(layout)
        
        self.initSimButton = QPushButton("Initialize Parameters", self)
        self.initSimButton.setObjectName("Initialize Parameters")
        addToLayout(self.initSimButton, layout)

        self.runSimButton = QPushButton("Run Simulation", self)
        self.runSimButton.setObjectName("Run Simulation")
        addToLayout(self.runSimButton, layout)

        self.stepButton = QPushButton("Proceed", self)
        self.stepButton.setObjectName("Proceed")
        addToLayout(self.stepButton, layout)

        self.showResultsButton = QPushButton("Show Results", self)
        self.showResultsButton.setObjectName("Show Results")
        addToLayout(self.showResultsButton, layout)
        #showResultsButton.clicked.connect()

        self.initSimButton.clicked.connect(self.build_model)
        self.runSimButton.clicked.connect(self.start_model)
        self.stepButton.clicked.connect(mutex.unlock)

        self.runSimButton.setDisabled(True)
        self.stepButton.setDisabled(True)
        self.showResultsButton.setDisabled(True)

        print("Button Panel Created")

    Slot()
    def build_model(self):
        
        self.simulator.initialize_model(
            100,
            self.main_window.main_table.network_tab,
            self.main_window.main_table.rdt_tab)
        self.runSimButton.setDisabled(False)
        print("Parameters Loaded")
    
    Slot()
    def start_model(self):

        self.simulator_thread.start()
        self.stepButton.setDisabled(False)
        print("Model Running")

    Slot()
    def prepare_results(self):

        self.showResultsButton.setDisabled(False)
        print("Results Ready")



class StepSlider(QtWidgets.QWidget):

    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self)

        # TODO: Improve this, and link it to self.step
        
        self.stepslider = QSlider()
        self.stepslider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.stepslider.setTickInterval(5)
        self.stepslider.setMinimum(1)
        self.stepslider.setEnabled(True)

        self.stepslider.valueChanged.connect(self.adjust_step_count)

        print("Step Slider Created")

    def adjust_step_count(self, value):

        # TODO: This might need to be linked better

        print(self.step)
        self.step = value * 100


