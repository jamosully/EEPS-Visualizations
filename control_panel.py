# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QVBoxLayout, QGroupBox, QPushButton, QSlider

class ButtonPanel(QtWidgets.QWidget):

    def __init__(self, parent, simulator, simulator_thread, mutex):
        QtWidgets.QWidget.__init__(self)
        
        self.verticalGroupBox = QGroupBox()
        self.simulator = simulator

        layout = QVBoxLayout()

        def addToLayout(button, layout):
            layout.addWidget(button)
            layout.setSpacing(10)
            self.verticalGroupBox.setLayout(layout)
        
        initSimButton = QPushButton("Initialize Parameters")
        initSimButton.setObjectName("Initialize Parameters")
        addToLayout(initSimButton, layout)
        initSimButton.clicked.connect(self.simulator.initialize_model(parent.main_table.network_tab.canvas, 100, parent.main_table.network_tab.figure))

        runSimButton = QPushButton("Run Simulation")
        runSimButton.setObjectName("Run Simulation")
        addToLayout(runSimButton, layout)
        runSimButton.clicked.connect(simulator_thread.start)

        stepButton = QPushButton("Step")
        stepButton.setObjectName("Step")
        addToLayout(stepButton, layout)
        stepButton.clicked.connect(mutex.unlock)

        print("Button Panel Created")

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


