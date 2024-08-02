# UI Modules
from PySide6 import QtCore, QtWidgets 
from PySide6.QtWidgets import QVBoxLayout, QTableWidget, QComboBox, QLabel, QGroupBox, QSizePolicy, QHeaderView, QPushButton, QHBoxLayout, QCheckBox, QDoubleSpinBox

import EEPS.initialization
import EEPS.initialization_detail

import os.path

class ParameterToolbox(QtWidgets.QWidget):

    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self) 
        #self.simulator = simulator

        self.toolbox = QGroupBox(self)
        self.main = parent

        self.box_layout = QVBoxLayout(self)

        self.environment_detail = EEPS.initialization_detail.environment_details()
        self.environment_parameter, self.agent_parameter = EEPS.initialization.config()

        self.agent_label = QLabel(self)
        self.agent_label.setText("Agent Parameters")

        self.env_label = QLabel(self)
        self.env_label.setText("Environment Parameters")

        self.env_toolbox = EnvParamTable(self.environment_detail, self.environment_parameter)
        self.agent_toolbox = AgentParamTable(self.agent_parameter)

        self.box_layout.addWidget(self.agent_label)
        self.box_layout.addWidget(self.agent_toolbox.table)
        self.box_layout.addWidget(self.env_label)
        self.box_layout.addWidget(self.env_toolbox.table)

        self.createButtons()
        self.box_layout.addLayout(self.button_layout)

        self.toolbox.setLayout(self.box_layout)

    def createButtons(self):

        self.button_layout = QHBoxLayout()

        self.createSimButton = QPushButton("Create Simulation")
        self.createSimButton.setObjectName("Create Simulation")
        self.button_layout.addWidget(self.createSimButton)
        self.button_layout.setSpacing(10)
        self.createSimButton.clicked.connect(lambda: self.main.createSim(1, 1))

        self.exportParamsButton = QPushButton("Export Parameters")
        self.exportParamsButton.setObjectName("Export Parameters")
        self.button_layout.addWidget(self.exportParamsButton)
        self.button_layout.setSpacing(10)


class EnvParamTable(QtWidgets.QWidget):

    def __init__(self, env_detail, env_params):
        QtWidgets.QWidget.__init__(self)

        self.table = QTableWidget(len(env_params), 2)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)

        self.env_params = env_params

        for i, (param_name, value) in enumerate(self.env_params.items()):
            param_label = QLabel()
            param_label.setIndent(5)
            param_label.setText(param_name)
            self.table.setCellWidget(i, 1, self.createTableWidget(value, param_name))
            self.table.setCellWidget(i, 0, param_label)

        self.table.resizeColumnsToContents()

    def createTableWidget(self, value, key):

        # if param_type == bool:
        #     table_widget = QCheckBox(self)
        #     table_widget.setObjectName(key)
        #     table_widget.clicked.connect(lambda: self.adjust_params(table_widget.checkState()))
        #     return table_widget
        # elif param_type ==  int:
        #     if

        match key:
            case "experiment_ID":
                return
            case "environment_ID":
                return
            case "max_trial":
                return
            case "num_agents":
                return
            case "size_action_set":
                return

    def adjust_params(self, value):

        key = self.sender().objectName()
        self.env_params[key] = value

class AgentParamTable(QtWidgets.QWidget):

    def __init__(self, agent_params):
        QtWidgets.QWidget.__init__(self)
        #self.simulator = simulator

        self.table = QTableWidget(len(agent_params), 2)
        # self.table.setSizePolicy(QSizePolicy.Policy.Expanding, 
        #                          QSizePolicy.Policy.Expanding)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)

        self.agent_params = agent_params

        self.generate_descriptions()

        for i, (param_name, value) in enumerate(agent_params.items()):
            param_label = QLabel()
            param_label.setIndent(5)
            param_label.setText(param_name)
            self.table.setCellWidget(i, 1, self.createTableWidget(value, param_name))
            self.table.setCellWidget(i, 0, param_label)

        self.table.resizeColumnsToContents()

    def createTableWidget(self, value, key):

        match key:
            case "network_enhancement":
                table_widget = QCheckBox(self)
                table_widget.setObjectName(key)
                table_widget.clicked.connect(lambda: self.adjust_params(key, table_widget.checkState()))
                return table_widget
            case "beta_h" | "K" | "gamma_damping" | "alpha":
                table_widget = QDoubleSpinBox(self)
                table_widget.setMaximum(1.00)
                table_widget.setMinimum(0.00)
                table_widget.setStepType(QDoubleSpinBox.StepType.AdaptiveDecimalStepType)
                table_widget.setDecimals(3)
                return table_widget
            case "beta_t":
                return
            
    def adjust_params(self, key, value):

        self.agent_params[key] = value


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
    


