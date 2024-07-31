# UI Modules
from PySide6 import QtCore, QtWidgets 
from PySide6.QtWidgets import QToolBar, QVBoxLayout, QTableWidget, QComboBox, QLabel, QGroupBox, QSizePolicy

import EEPS.initialization
import EEPS.initialization_detail

import os.path

class ParameterToolbox(QtWidgets.QWidget):

    def __init__(self, parent, simulator):
        QtWidgets.QWidget.__init__(self) 
        self.simulator = simulator

        self.toolbox = QGroupBox(self)

        self.box_layout = QVBoxLayout(self)

        self.environment_detail = EEPS.initialization_detail.environment_details()
        self.environment_parameter, self.agent_parameter = EEPS.initialization.config()

        self.env_toolbox = EnvParamTable(self.simulator, self.environment_detail, self.environment_parameter)
        self.agent_toolbox = AgentParamTable(self.simulator, self.agent_parameter)

        self.box_layout.addWidget(self.agent_toolbox.table)

        self.toolbox.setLayout(self.box_layout)

class EnvParamTable(QtWidgets.QWidget):

    def __init__(self, simulator, env_detail, env_param):
        QtWidgets.QWidget.__init__(self)
        self.simulator = simulator

        self.table = QTableWidget(self)

class AgentParamTable(QtWidgets.QWidget):

    def __init__(self, simulator, agent_params):
        QtWidgets.QWidget.__init__(self)
        self.simulator = simulator

        # TODO: Get the table to fill the whole space better

        self.table = QTableWidget(len(agent_params), 2)
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, 
                                 QSizePolicy.Policy.Expanding)
        self.generate_descriptions()

        for i, (param_name, value) in enumerate(agent_params.items()):
            param_label = QLabel()
            param_label.setText(param_name)
            print(i, param_name, value)
            self.table.setCellWidget(i, 0, param_label)

        self.table.resizeColumnsToContents()

    def generate_descriptions(self):

        with open(os.path.abspath(EEPS.initialization.__file__)) as f:
            read_doc = False
            for line in f:
                strip_line = line.strip()
                if strip_line.startswith('"""'):
                    read_doc = not read_doc
                else:
                    if read_doc:
                        if strip_line.startswith('-'):
                            split_desc = strip_line.split(': ')
                            name = split_desc[0][2:]
                            print(name)
                    
            print("Opened initialization.py")
    


