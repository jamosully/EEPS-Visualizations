# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QVBoxLayout, QGroupBox, QPushButton, QSlider, QSpinBox, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Slot, Signal

class ControlPanel(QtWidgets.QWidget):
    
    def __init__(self,  main_table, simulator, simulator_thread, mutex):
        QtWidgets.QWidget.__init__(self)

        # TODO: This initialization is a mess
        #       Could be potentially refactored?
        
        self.verticalGroupBox = QGroupBox()
        self.simulator = simulator
        self.main_table = main_table
        self.simulator_thread = simulator_thread

        self.step_count = 100

        layout = QVBoxLayout()

        def addToLayout(widget, layout):
            layout.addWidget(widget)
            layout.setSpacing(10)
            self.verticalGroupBox.setLayout(layout)

        self.modifyParametersButton = QPushButton("Update Parameters", self)
        self.modifyParametersButton.setObjectName("Update Parameters")
        addToLayout(self.modifyParametersButton, layout)
        
        self.initSimButton = QPushButton("Initialize Parameters", self)
        self.initSimButton.setObjectName("Initialize Parameters")
        addToLayout(self.initSimButton, layout)

        self.runSimButton = QPushButton("Run Simulation", self)
        self.runSimButton.setObjectName("Run Simulation")
        addToLayout(self.runSimButton, layout)

        self.stepButton = QPushButton("Proceed", self)
        self.stepButton.setObjectName("Proceed")
        addToLayout(self.stepButton, layout)

        self.initSimButton.clicked.connect(lambda: self.build_model())
        self.runSimButton.clicked.connect(self.start_model)
        self.stepButton.clicked.connect(mutex.unlock)

        self.runSimButton.setDisabled(True)
        self.stepButton.setDisabled(True)

        print("Button Panel Created")

        self.stepSlider = StepControl(self, self.step_count)
        layout.addWidget(self.stepSlider.stepslider, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        layout.setSpacing(10)
        self.verticalGroupBox.setLayout(layout)

        layout.addWidget(self.stepSlider.stepCounter)#, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        layout.setSpacing(10)
        self.verticalGroupBox.setLayout(layout)

    Slot()
    def build_model(self):
        
        self.simulator.initialize_model(
            self.step_count,
            self.main_table.network_tab,
            self.main_table.rdt_tab,
            self.main_table.heatmap_tab)
        self.runSimButton.setDisabled(False)
        print("Parameters Loaded")
    
    Slot()
    def start_model(self):

        self.simulator_thread.start()
        self.stepButton.setDisabled(False)
        print("Model Running")

class StepControl(QtWidgets.QWidget):

    def __init__(self, parent, step):
        QtWidgets.QWidget.__init__(self)

        # TODO: Improve this, and link it to self.step
        self.control_panel = parent
        
        self.stepslider = QSlider()
        # self.stepslider.setTickPosition(QSlider.TickPosition.TicksAbove)
        # self.stepslider.setTickInterval(5)
        self.stepslider.setMinimum(10)
        self.stepslider.setMaximum(1000)
        self.stepslider.setEnabled(True)

        print("Step Slider Created")

        self.stepCounter = QSpinBox()
        self.stepCounter.setMaximum(10000)
        self.stepCounter.setMinimum(10)
        self.stepCounter.setValue(self.stepslider.value())
        self.stepCounter.setSingleStep(10)
        #self.stepCounter.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.stepCounter.valueChanged.connect(self.stepslider.setValue)
        self.stepCounter.valueChanged.connect(self.adjust_step)
        self.stepslider.valueChanged.connect(self.stepCounter.setValue)
        self.stepslider.valueChanged.connect(self.adjust_step)

    def adjust_step(self, value):

        # TODO: This might need to be linked better

        self.control_panel.step_count = value
        print(self.control_panel.step_count)



