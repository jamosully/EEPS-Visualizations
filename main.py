import sys

# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QGridLayout, QVBoxLayout, QStyleFactory, QTabWidget, QGroupBox
from PySide6.QtCore import Slot, Signal, QThread, QMutex, QWaitCondition

from simulator import Simulator
from table_setup import TableDisplay
from control_panel import ControlPanel
from parameter_toolbox import ParameterToolbox

class MainWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Affinity")

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.tabs = QTabWidget()
        self.createParameterMenu()

        self.models = {}
        self.model_num  = 1

        self.filename = None

        self.grid.addWidget(self.parameter_menu.toolbox, 0, 0)
        self.grid.addWidget(self.tabs, 0 , 1)

        self.setFixedSize(self.grid.sizeHint())

    def createSystem(self, agent_params, env_params):

        simulator_dict = {}

        simulator_dict['mutex'] = QMutex()
        simulator_dict['cond'] = QWaitCondition()
        simulator_dict['sim'] = Simulator(simulator_dict['mutex'], agent_params, env_params, self.filename)
        simulator_dict['thread'] = QThread(parent=self)

        simulator_dict['sim'].moveToThread(simulator_dict['thread'])
        simulator_dict['thread'].started.connect(simulator_dict['sim'].run_sim)

        return simulator_dict

    def createParameterMenu(self):

        self.parameter_menu = ParameterToolbox(self)

    def createTable(self, simulator):

        return TableDisplay(self, simulator)

    def createControlPanel(self, main, simulator):

        control_panel = QVBoxLayout()

        button_panel = ControlPanel(main, simulator['sim'], simulator['thread'], simulator['mutex'])

        # TODO: Set the layout of control panel to the vertical group box itself

        control_panel.addWidget(button_panel.verticalGroupBox)

        self.setFixedSize(self.grid.sizeHint())

        return control_panel
    
    Slot()
    def createSim(self):

        self.tab = QGroupBox()
        self.tab_layout = QGridLayout()

        self.models[self.model_num] = {}
        self.models[self.model_num]['simulator'] = self.createSystem(self.parameter_menu.agent_toolbox.agent_params, 
                                                                     self.parameter_menu.env_toolbox.env_params)
        self.models[self.model_num]['main_display'] = self.createTable(self.models[self.model_num]['simulator']['sim'])
        self.models[self.model_num]['control_panel'] = self.createControlPanel(self.models[self.model_num]['main_display'],
                                                                               self.models[self.model_num]['simulator'])

        self.tab_layout.addLayout(self.models[self.model_num]['control_panel'], 0, 0)
        self.tab_layout.addWidget(self.models[self.model_num]['main_display'], 0, 1)

        self.tab.setLayout(self.tab_layout)

        self.tabs.addTab(self.tab, "Agent " + str(self.model_num))

        print(self.models[self.model_num])

        self.setFixedSize(self.grid.sizeHint())

        self.model_num += 1


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    #app.setStyle(QStyleFactory)

    widget = MainWindow()
    widget.resize(1400, 800)
    widget.show()
    #widget.showMaximized()

    sys.exit(app.exec())