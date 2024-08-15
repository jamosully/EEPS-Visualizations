# UI Modules
from PySide6 import QtCore, QtWidgets 
from PySide6.QtWidgets import (QVBoxLayout, QTableWidget, QComboBox, 
                               QLabel, QGroupBox, QSizePolicy, 
                               QHeaderView, QPushButton, QHBoxLayout, 
                               QCheckBox, QDoubleSpinBox, QSpinBox,
                               QTextEdit, QSpacerItem, QFileDialog)

import EEPS.initialization
import EEPS.initialization_detail

import os.path
from pathlib import Path
import pickle

"""
parameter_toolbox.py

Customise agent and environment parameters without having to
edit initialization.py. Also load in parameters from a previous
model
"""

class ParameterToolbox(QtWidgets.QWidget):

    """
    Main component of the parameter toolbox
    
    All other components are placed within
    """

    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self) 

        self.toolbox = QGroupBox(self)
        self.main = parent

        self.box_layout = QVBoxLayout(self)
        
        # The parameters and environmental detail are loaded in
        # from the intialization.py and intialization_detail.py
        # respectivly

        # TODO: Improve the parameter and environment definitions
        #       in each file, so they can be loaded in to the toolbox

        self.environment_detail = EEPS.initialization_detail.environment_details()
        self.environment_parameter, self.agent_parameter = EEPS.initialization.config()

        self.agent_label = QLabel(self)
        self.agent_label.setText("Agent Parameters")

        self.env_label = QLabel(self)
        self.env_label.setText("Environment Parameters")

        self.env_toolbox = EnvParamTable(self.environment_detail, self.environment_parameter)
        self.agent_toolbox = AgentParamTable(self.agent_parameter)

        self.createFilenameEntry()

        # TODO: Create a separate function for adding all components

        self.box_layout.addWidget(self.fileTable)
        self.box_layout.addWidget(self.agent_label)
        self.box_layout.addWidget(self.agent_toolbox.table)
        self.box_layout.addWidget(self.env_label)
        self.box_layout.addWidget(self.env_toolbox.table)

        self.createButtons()
        self.box_layout.addLayout(self.button_layout)

        self.toolbox.setLayout(self.box_layout)

    def createButtons(self):

        """
        The butttons at the bottom of the toolbox create the model
        and save parameters to the initialization.py file
        """

        # TODO: Get export parameters button working

        self.button_layout = QHBoxLayout()

        self.createSimButton = QPushButton("Create Simulation")
        self.createSimButton.setObjectName("Create Simulation")
        self.button_layout.addWidget(self.createSimButton)
        self.button_layout.setSpacing(10)
        self.createSimButton.clicked.connect(lambda: self.main.createSystem())

        self.exportParamsButton = QPushButton("Export Parameters")
        self.exportParamsButton.setObjectName("Export Parameters")
        self.button_layout.addWidget(self.exportParamsButton)
        self.button_layout.setSpacing(10)

    def createFilenameEntry(self):

        """
        Users can pick files from previous simulations

        Uses the open_file_dialog, change_filename,
        reset_filename, and updateParamsFromFile functions
        """

        self.fileTable = QTableWidget(2, 2)
        self.fileTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.fileTable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.fileTable.verticalHeader().setVisible(False)
        self.fileTable.horizontalHeader().setVisible(False)
        self.fileTable.setMaximumHeight(self.fileTable.verticalHeader().length())
        self.fileTable.setSizePolicy(QSizePolicy.Policy.Expanding,
                                     QSizePolicy.Policy.Minimum)

        fileEntryLabel = QLabel()
        fileEntryLabel.setIndent(5)
        fileEntryLabel.setText("Filename: ")
        self.fileTable.setCellWidget(0, 0, fileEntryLabel)

        self.fileEntryField = QTextEdit()
        #self.fileEntryField.textChanged.connect(lambda: self.change_filename(self.fileEntryField.text()))
        self.fileTable.setCellWidget(0, 1, self.fileEntryField)

        self.loadFileButton = QPushButton("Load File")
        self.fileTable.setCellWidget(1, 0, self.loadFileButton)
        self.loadFileButton.clicked.connect(self.open_file_dialog)

        self.newFileButton = QPushButton("New File")
        self.fileTable.setCellWidget(1, 1, self.newFileButton)
        self.newFileButton.clicked.connect(self.reset_filename)

    def change_filename(self, text):

        print("Filename: " + text)
        self.main.filename = text

    def open_file_dialog(self):

        self.filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File",
            filter="EEPS Files (*.p)"
        )
        if self.filename:
            self.change_filename(str(Path(self.filename)))
            self.fileEntryField.setText(str(Path(self.filename)))
            self.updateParamsFromFile(self.filename)
    
    def reset_filename(self):

        self.main.filename = None

    def updateParamsFromFile(self, filename):

        """
        Responsible for updating the values in the toolbox
        once a new file is loaded (WIP)
        """

        resultFile = open(filename, 'rb')
        self.data = pickle.load(resultFile)
        resultFile.close()

        # TODO: Get this working
        #       Could be an issue with how tables are generated

        print(self.data['environment_parameter'])

        for i, (param_name, value) in enumerate(self.data['environment_parameter'].items()):
            self.env_toolbox.env_params[param_name] = value
            print(self.env_toolbox.table.item(i, 0))
            if isinstance(self.env_toolbox.table.item(i, 1), QSpinBox):
                self.env_toolbox.table.item(i, 1).setValue(value)
            elif isinstance(self.env_toolbox.table.item(i, 1), QComboBox):
                for x, (id, details) in enumerate(EEPS.initialization_detail.environment_details().items()):
                    if value[0] == id:
                        self.env_toolbox.table.item(i, 1).setCurrentIndex(x)

class EnvParamTable(QtWidgets.QWidget):

    """
    Table containing all environmental parameters
    """

    def __init__(self, env_detail, env_params):
        QtWidgets.QWidget.__init__(self)

        self.table = QTableWidget(len(env_params), 2)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setMaximumHeight(self.table.verticalHeader().length())

        self.env_params = env_params

        for i, (param_name, value) in enumerate(self.env_params.items()):
            param_label = QLabel()
            param_label.setIndent(5)
            param_label.setText(param_name + "  ")
            self.table.setCellWidget(i, 1, self.createTableWidget(value, param_name))
            self.table.setCellWidget(i, 0, param_label)

        self.table.resizeColumnsToContents()

    def createTableWidget(self, value, key):

        """
        Identifies which parameter is added, and adds the correct
        widget for modifying it.
        """

        # TODO: Offset complexity on initialization.py
        #       Each parameter could pass a type stored in intialization.py
        #       Saves this matching shit

        match key:
            case "environment_ID":
                table_widget = QComboBox(self)
                for x, (id, details) in enumerate(EEPS.initialization_detail.environment_details().items()):
                    table_widget.insertItem(x, str(id))
                    if value[0] == id:
                        table_widget.setCurrentIndex(x)
                table_widget.currentIndexChanged.connect(lambda: self.adjust_params(key, table_widget.currentIndex()))
                return table_widget
            case "max_trial" | "size_action_set" | "experiment_ID":
                table_widget = QSpinBox(self)
                table_widget.setMinimum(1)
                table_widget.setMaximum(100000)
                table_widget.setValue(value[0])
                table_widget.valueChanged.connect(lambda: self.adjust_params(key, table_widget.value()))
                return table_widget
            case "num_agents":

                # TODO: Should this parameter be incorporated into the multi-agent mode?
                #       Probably not, will think about it some more

                return

    def adjust_params(self, key, value):

        self.env_params[key] = [value]
        print(self.env_params)

class AgentParamTable(QtWidgets.QWidget):

    """
    Table containing all agent parameters
    """

    def __init__(self, agent_params):
        QtWidgets.QWidget.__init__(self)

        self.table = QTableWidget(len(agent_params), 2)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setMaximumHeight(self.table.verticalHeader().length())

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

        """
        Identifies which parameter is added, and adds the correct
        widget for modifying it.
        """

        match key:
            case "network_enhancement":
                table_widget = QCheckBox(self)
                table_widget.setChecked(value[0])
                table_widget.clicked.connect(lambda: self.adjust_params(key, table_widget.checkState()))
                return table_widget
            case "beta_h" | "K" | "gamma_damping" | "alpha":
                table_widget = QDoubleSpinBox(self)
                table_widget.setMaximum(1.00)
                table_widget.setMinimum(0.00)
                table_widget.setValue(value[0])
                table_widget.setStepType(QDoubleSpinBox.StepType.AdaptiveDecimalStepType)
                table_widget.setDecimals(3)
                table_widget.valueChanged.connect(lambda: self.adjust_params(key, table_widget.value()))
                return table_widget
            case "beta_t":
                table_widget = QDoubleSpinBox(self)
                table_widget.setMinimum(0.01)
                table_widget.setValue(value[0])
                table_widget.setStepType(QDoubleSpinBox.StepType.AdaptiveDecimalStepType)
                table_widget.valueChanged.connect(lambda: self.adjust_params(key, table_widget.value()))
                return table_widget
            
    def adjust_params(self, key, value):

        self.agent_params[key] = [value]
        print(self.agent_params)

    def generate_descriptions(self):

        """
        Using intialization.py, get descriptions of each parameter;
        what they do, value ranges (WIP) 
        """

        # TODO: Fix generate_descriptions

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
    


