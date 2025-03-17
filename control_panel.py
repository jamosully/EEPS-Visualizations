# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QVBoxLayout, QGroupBox, QPushButton, QSlider, QSpinBox, QLabel
from PySide6.QtCore import Slot, Signal

"""
control_panel.py

Simulation progression and step control
"""

class ControlPanel(QtWidgets.QWidget):

    """
    Four buttons and a slider

    Update parameters: pass parameters in the toolbox to 
                       the simulator
    
    Initialise model: runs initialize_model in simulator.py

    Run Model: starts the model

    Proceed: step forward through the simulation

    Step Slider: controls the rate of progression
    """

    update_params = Signal()
    
    def __init__(self,  mainDisplay, simulator, simulatorThread, mutex):
        QtWidgets.QWidget.__init__(self)

        # TODO: This initialization is a mess
        #       Could be potentially refactored?
        
        self.verticalGroupBox = QGroupBox()
        self.simulator = simulator
        self.mainDisplay = mainDisplay
        self.simulatorThread = simulatorThread

        self.step_count = 1

        self.panelLayout = QVBoxLayout()

        def addToLayout(widget):
            self.panelLayout.addWidget(widget)
            self.panelLayout.setSpacing(10)
            self.verticalGroupBox.setLayout(self.panelLayout)

        self.modifyParametersButton = QPushButton("Update Parameters", self)
        self.modifyParametersButton.setObjectName("Update Parameters")
        addToLayout(self.modifyParametersButton)
        
        self.initSimButton = QPushButton("Initialize Parameters", self)
        self.initSimButton.setObjectName("Initialize Parameters")
        addToLayout(self.initSimButton)

        self.runSimButton = QPushButton("Run Simulation", self)
        self.runSimButton.setObjectName("Run Simulation")
        addToLayout(self.runSimButton)

        self.stepButton = QPushButton("Proceed", self)
        self.stepButton.setObjectName("Proceed")
        addToLayout(self.stepButton)

        self.modifyParametersButton.clicked.connect(lambda: self.simulator.update_parameters(self.mainDisplay.main.parameterMenu.model_agent_params,
                                                                                             self.mainDisplay.main.parameterMenu.model_env_params))
        self.initSimButton.clicked.connect(lambda: self.build_model())
        self.runSimButton.clicked.connect(self.start_model)
        self.stepButton.clicked.connect(mutex.unlock)

        self.runSimButton.setDisabled(True)
        self.stepButton.setDisabled(True)

        print("Button Panel Created")

        self.stepSlider = StepControl(self, self.step_count)
        self.panelLayout.addWidget(self.stepSlider.stepslider, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.panelLayout.setSpacing(10)
        self.verticalGroupBox.setLayout(self.panelLayout)

        self.panelLayout.addWidget(self.stepSlider.stepCounter)#, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.panelLayout.setSpacing(10)
        self.verticalGroupBox.setLayout(self.panelLayout)
        self.setLayout(self.panelLayout)

    Slot()
    def build_model(self):
        
        self.simulator.initialize_model(
            self.step_count,
            self.mainDisplay)
        self.runSimButton.setDisabled(False)
        print("Parameters Loaded")
    
    Slot()
    def start_model(self):

        self.simulatorThread.start()
        self.stepButton.setDisabled(False)
        print("Model Running")

class StepControl(QtWidgets.QWidget):

    """
    Vertical slider and spin box for controlling
    rate of progession
    """

    def __init__(self, parent, step):
        QtWidgets.QWidget.__init__(self)

        # TODO: Improve this, and link it to self.step
        self.control_panel = parent
        
        self.stepslider = QSlider()
        # self.stepslider.setTickPosition(QSlider.TickPosition.TicksAbove)
        # self.stepslider.setTickInterval(5)
        self.stepslider.setMinimum(1)
        self.stepslider.setMaximum(1000)
        self.stepslider.setEnabled(True)

        print("Step Slider Created")

        self.stepCounter = QSpinBox()
        self.stepCounter.setMaximum(10000)
        self.stepCounter.setMinimum(1)
        self.stepCounter.setValue(self.control_panel.step_count)
        self.stepCounter.setSingleStep(1)
        #self.stepCounter.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.stepCounter.valueChanged.connect(self.stepslider.setValue)
        self.stepCounter.valueChanged.connect(self.adjust_step)
        self.stepslider.valueChanged.connect(self.stepCounter.setValue)
        self.stepslider.valueChanged.connect(self.adjust_step)

    def adjust_step(self, value):

        # TODO: This might need to be linked better

        self.control_panel.step_count = value
        self.control_panel.mainDisplay.step_changed = True