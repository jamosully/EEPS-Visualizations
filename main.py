import sys

# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QGridLayout, QVBoxLayout, QPushButton, QGroupBox, QSlider
from PySide6.QtCore import Slot, Signal, QThread, QMutex, QWaitCondition

from simulator import Simulator
from table_setup import TableDisplay
from control_panel import ButtonPanel, StepSlider

class MainWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Affinity.net")

        grid = QGridLayout()
        
        self.setLayout(grid)

        self.createSimulator()
        self.createTable()
        self.createControlPanel()

        grid.addWidget(self.main_table, 0, 1)
        grid.addLayout(self.control_layout, 0, 0)


    def createSimulator(self):
        self.mutex = QMutex()
        self.cond = QWaitCondition()
        self.simulator = Simulator(self.mutex)
        self.simulator_thread = QThread()

        self.simulator.moveToThread(self.simulator_thread)

        self.simulator_thread.started.connect(self.simulator.run_sim)

    def createTable(self):

        self.main_table = TableDisplay(self, self.simulator)

    def createControlPanel(self):

        self.control_layout = QVBoxLayout()

        self.button_panel = ButtonPanel(self, self.simulator, self.simulator_thread, self.mutex)
        self.slider = StepSlider(self)

        self.control_layout.addWidget(self.button_panel.verticalGroupBox)
        self.control_layout.addWidget(self.slider.stepslider)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())