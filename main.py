import sys

# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QGridLayout, QVBoxLayout, QStyleFactory, QTabWidget, QGroupBox
from PySide6.QtCore import Slot, Signal, QThread, QMutex, QWaitCondition


from simulator import Simulator
from table_setup import TableDisplay
from control_panel import ButtonPanel, StepSlider
from parameter_details import ParameterToolbox

class MainWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Affinity.net")

        grid = QGridLayout()
        
        self.setLayout(grid)

        self.tabs = QTabWidget()
        # self.createSystem()
        # self.createTable()
        # self.createControlPanel()

        #self.createSim()
        self.createParameterMenu()

        grid.addWidget(self.parameter_menu.toolbox, 0, 0)
        grid.addWidget(self.tabs, 0 , 1)
        # grid.addLayout(self.control_layout, 0, 1)
        # grid.addWidget(self.main_table, 0, 2)

    def createSystem(self):
        self.mutex = QMutex()
        self.cond = QWaitCondition()
        self.simulator = Simulator(self.mutex)
        self.simulator_thread = QThread()

        self.simulator.moveToThread(self.simulator_thread)

        self.simulator_thread.started.connect(self.simulator.run_sim)

    def createParameterMenu(self):

        self.parameter_menu = ParameterToolbox(self)

    def createTable(self):

        self.main_table = TableDisplay(self, self.simulator)

    def createControlPanel(self):

        self.control_layout = QVBoxLayout()

        self.button_panel = ButtonPanel(self, self.simulator, self.simulator_thread, self.mutex)
        self.slider = StepSlider(self)

        self.control_layout.addWidget(self.button_panel.verticalGroupBox)
        self.control_layout.addWidget(self.slider.stepslider)

    Slot()
    def createSim(self, num, params):

        self.tab = QGroupBox()
        self.tab_layout = QGridLayout()
        
        self.createSystem()
        self.createControlPanel()
        self.createTable()
        
        self.tab_layout.addLayout(self.control_layout, 0, 0)
        self.tab_layout.addWidget(self.main_table, 0, 1)

        self.tab.setLayout(self.tab_layout)

        self.tabs.addTab(self.tab, "Agent 1")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    #app.setStyle(QStyleFactory)

    widget = MainWindow()
    widget.resize(1200, 600)
    widget.show()
    #widget.showMaximized()

    sys.exit(app.exec())