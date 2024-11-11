# UI Modules
from PySide6 import QtCore, QtWidgets 
from PySide6.QtWidgets import (QVBoxLayout, QTableWidget, QComboBox, 
                               QLabel, QGroupBox, QSizePolicy, 
                               QHeaderView, QPushButton, QHBoxLayout, 
                               QCheckBox, QDoubleSpinBox, QSpinBox,
                               QTextEdit, QSpacerItem, QFileDialog,
                               QPlainTextEdit)

import EEPS.initialization
import EEPS.initialization_detail

import os.path
from pathlib import Path
import pickle
import json

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
        
        # The parameters are now loaded in from a single 
        # json file, which contains names, values, descriptions,
        # and the type

        self.load_json()

        self.environment_detail = EEPS.initialization_detail.environment_details()

        self.json_env_params = self.json_params['environment_parameters']
        self.json_agent_params = self.json_params['agent_parameters']

        self.model_env_params = self.create_param_dict(self.json_env_params)
        self.model_agent_params = self.create_param_dict(self.json_agent_params)

        print(self.model_agent_params)

        self.agent_label = QLabel(self)
        self.agent_label.setText("Agent Parameters")

        self.env_label = QLabel(self)
        self.env_label.setText("Environment Parameters")

        self.env_toolbox = ParamTable(self, self.json_env_params)
        self.agent_toolbox = ParamTable(self, self.json_agent_params)

        self.createFilenameEntry()

        # TODO: Create a separate function for adding all components

        self.box_layout.addWidget(self.fileTable)
        self.box_layout.addWidget(self.agent_label)
        self.box_layout.addWidget(self.agent_toolbox.table)
        self.box_layout.addWidget(self.agent_toolbox.descriptionField)
        self.box_layout.addWidget(self.env_label)
        self.box_layout.addWidget(self.env_toolbox.table)
        self.box_layout.addWidget(self.env_toolbox.descriptionField)

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

        self.exportParamsButton = QPushButton("Set Default Parameters")
        self.exportParamsButton.setObjectName("Set Default Parameters")
        self.button_layout.addWidget(self.exportParamsButton)
        self.button_layout.setSpacing(10)
        self.exportParamsButton.clicked.connect(self.export_params_to_json)

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

        for i, (param_name, value) in enumerate(self.data['environment_parameter'].items()):
            self.model_env_params[param_name] = value
            for j in range(self.env_toolbox.table.rowCount()):
                if self.env_toolbox.table.cellWidget(j, 1).param_name == param_name:
                    self.env_toolbox.table.cellWidget(j, 1).update_param_value(value[0])

        for i, (param_name, value) in enumerate(self.data['agent_parameter'].items()):
            self.model_agent_params[param_name] = value
            for j in range(self.agent_toolbox.table.rowCount()):
                if self.agent_toolbox.table.cellWidget(j, 1).param_name == param_name:
                    self.agent_toolbox.table.cellWidget(j, 1).update_param_value(value[0]) 
    
    
    def reset_filename(self):

        self.main.filename = None

    def load_json(self):

        with open("initialization.json", 'r', encoding='utf8') as init_params:
            self.json_params = json.load(init_params)

    def create_param_dict(self, detailed_params):

        new_param_dict = {}
        for param in detailed_params:
            new_param_dict[param['name']] = [param['value']]

        return new_param_dict

    def export_params_to_json(self):

        print("Parameters exported")
        with open("initialization.json", "w", encoding="utf8") as init_params:
            json.dump(self.json_params, init_params, indent=4)


    def adjust_params(self, key, value):

        """
        Assigning variable in the dictionary that is used
        by the createSystem function in main.py
        """
        
        if key in self.model_agent_params:
            self.model_agent_params[key] = [value]
            for param in self.json_params['agent_parameters']:
                if param['name'] == key:
                    param['value'] = value
        else:
            self.model_env_params[key] = [value]
            for param in self.json_params['environment_parameters']:
                if param['name'] == key:
                    param['value'] = value


    def createParamWidget(self, key, value, type):

        """
        Based on the type provided in initialization.json,
        create a widget for the table
        """

        match type:
            case 'int':
                widget = ParamSpinBox(key)
                widget.setMinimum(1)
                widget.setMaximum(100000)
                widget.setValue(value)
                widget.valueChanged.connect(lambda: self.adjust_params(key, widget.value()))
                return widget
            case 'unit_interval':
                widget = ParamDoubleSpinBox(key)
                widget.setMaximum(1.00)
                widget.setMinimum(0.00)
                widget.setDecimals(3)
                widget.setValue(value)
                widget.setStepType(QDoubleSpinBox.StepType.AdaptiveDecimalStepType)
                widget.valueChanged.connect(lambda: self.adjust_params(key, widget.value()))
                return widget
            case 'float':
                widget = ParamDoubleSpinBox(key)
                widget.setMinimum(0.01)
                widget.setValue(value)
                widget.setStepType(QDoubleSpinBox.StepType.AdaptiveDecimalStepType)
                widget.valueChanged.connect(lambda: self.adjust_params(key, widget.value()))
                return widget
            case 'bool':
                widget = ParamCheckBox(key)
                widget.setChecked(value)
                widget.clicked.connect(lambda: self.adjust_params(key, widget.checkState()))
                return widget
            case 'env_id':
                widget = ParamComboBox(key)
                for x, (id, details) in enumerate(EEPS.initialization_detail.environment_details().items()):
                    widget.insertItem(x, str(id))
                    if value == id:
                        widget.setCurrentIndex(x)
                widget.currentIndexChanged.connect(lambda: self.adjust_params(key, int(widget.currentText())))
                return widget

class ParamTable(QtWidgets.QWidget):

    """
    Table containing all agent parameters
    """

    def __init__(self, toolbox, params):
        QtWidgets.QWidget.__init__(self)

        self.toolbox = toolbox

        self.table = QTableWidget(len(params), 2)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setMaximumHeight(self.table.verticalHeader().length())
        self.table.setMouseTracking(True)

        for i in range(len(params)):
            param_label = ParamLabel(params[i]['description'])
            param_label.setIndent(5)
            param_label.setText(params[i]['name'] + "  ")
            self.table.setCellWidget(i, 1, self.toolbox.createParamWidget(params[i]['name'], params[i]['value'], params[i]['type']))
            self.table.setCellWidget(i, 0, param_label)

        self.descriptionField = QPlainTextEdit()
        self.descriptionField.setPlainText(" ")
        self.descriptionField.setReadOnly(True)

        self.table.cellEntered.connect(self.cellHover)

        self.table.resizeColumnsToContents()

    def cellHover(self, row, column):

        widget = self.table.cellWidget(row, 0)
        if self.descriptionField.toPlainText != widget.desc:
            self.descriptionField.setPlainText(widget.desc)

class ParamLabel(QtWidgets.QLabel):

    def __init__(self, desc):
        super(ParamLabel, self).__init__()

        self.desc = desc

class ParamDoubleSpinBox(QtWidgets.QDoubleSpinBox):

    def __init__(self, param_name):
        super(ParamDoubleSpinBox, self).__init__()

        self.param_name = param_name

    def update_param_value(self, value):

        self.setValue(value)

class ParamComboBox(QtWidgets.QComboBox):

    def __init__(self, param_name):
        super(ParamComboBox, self).__init__()

        self.param_name = param_name

    def update_param_value(self, value):

        self.setCurrentIndex(value)

class ParamSpinBox(QtWidgets.QSpinBox):

    def __init__(self, param_name):
        super(ParamSpinBox, self).__init__()

        self.param_name = param_name

    def update_param_value(self, value):

        self.setValue(value)

class ParamCheckBox(QtWidgets.QCheckBox):

    def __init__(self, param_name):
        super(ParamCheckBox, self).__init__()

        self.param_name = param_name

    def update_param_value(self, value):

        self.setChecked(value)
    


