import sys

# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QGridLayout, QVBoxLayout, QPushButton, QGroupBox, QSlider
from PySide6.QtCore import Slot, Signal, QThread, QMutex, QWaitCondition

from simulator import Simulator
from table_setup import TableDisplay
from side_panel import SidePanel

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Affinity.net")

        grid = QGridLayout()
        self.setLayout(grid)




    def createSimulator(self):
        self.mutex = QMutex()
        self.cond = QWaitCondition()
        self.simulator = Simulator(self.mutex)
        self.simulator_thread = QThread()

        self.simulator.moveToThread(self.simulator_thread)

        self.simulator_thread.started.connect(self.simulator.run_sim)

    def createTable(self):

        self.main_table = TableDisplay(self.simulator)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())