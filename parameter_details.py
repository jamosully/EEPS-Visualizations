# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QToolBar, QVBoxLayout, QTableWidget, QComboBox

import EEPS.initialization
import EEPS.initialization_detail

class ParameterToolbox(QtWidgets.QWidget):

    def __init__(self, simulator):
        QtWidgets.QWidget.__init__(self) 
        self.simulator = simulator

        self.environment_detail = EEPS.initialization_detail.environment_details()
        self.environment_parameter, self.agent_parameter = EEPS.initialization.config()

class EnvParamTable(QtWidgets.QWidget):

    def __init__(self, simulator, env_detail, env_param):
        QtWidgets.QWidget.__init__(self)
        self.simulator = simulator

        self.table = QTableWidget(self)

class AgentParamTable(QtWidgets.QWidget):

    def __init__(self, simulator, agent_param):
        QtWidgets.QWidget.__init__(self)
        self.simulator = simulator

        self.table = QTableWidget(self)

