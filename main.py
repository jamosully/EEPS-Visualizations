import sys

# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QGridLayout, QVBoxLayout, QStyleFactory, QTabWidget, QGroupBox
from PySide6.QtCore import Slot, Signal, QThread, QMutex, QWaitCondition

from simulator import Simulator
from visualization_display import VisualizationDisplay
from control_panel import ControlPanel
from parameter_toolbox import ParameterToolbox

"""
main.py

Primary script. Running main.py will launch Affinity
"""

class MainWindow(QtWidgets.QWidget):

    """
    Essentially the main window of Affinity
    
    All roads start from here.
    """

    values_changed = Signal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Affinity")

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.tabs = QTabWidget()
        self.createParameterMenu()

        # Each model is added to a dictionary, and numbered

        self.models = {}
        self.model_num  = 1

        # Filename is none at start, once a user adds a file it changes

        self.filename = None

        self.grid.addWidget(self.parameter_menu.toolbox, 0, 0)
        self.grid.addWidget(self.tabs, 0 , 1)

        self.setFixedSize(self.grid.sizeHint())

    def createSim(self, agent_params, env_params):

        """
        Provides all nescessary features for this version
        of EEPS, including threading and mutex
        """

        # Create a version of EEPS, and give it a thread + mutex

        simulator_dict = {}

        simulator_dict['mutex'] = QMutex()
        simulator_dict['sim'] = Simulator(simulator_dict['mutex'], agent_params, env_params, self.filename)
        simulator_dict['thread'] = QThread(parent=self)

        simulator_dict['sim'].moveToThread(simulator_dict['thread'])
        simulator_dict['thread'].started.connect(simulator_dict['sim'].run_sim)

        return simulator_dict

    def createParameterMenu(self):

        """
        The parameter toolbox allows the user to set environment 
        and agent parameters, load in existing configurations,
        and save parameters as default in intialization.py
        """

        self.parameter_menu = ParameterToolbox(self)

    def createTable(self, simulator):

        """
        The table display holds visualizations and results
        """

        return VisualizationDisplay(self, simulator)

    def createControlPanel(self, main, simulator):

        """
        Primary source of interaction with visualizations,
        including assigning step values and updating 
        parameters
        """

        control_panel = QVBoxLayout()

        button_panel = ControlPanel(main, simulator['sim'], simulator['thread'], simulator['mutex'])

        # TODO: Set the layout of control panel to the vertical group box itself

        control_panel.addWidget(button_panel.verticalGroupBox)

        self.setFixedSize(self.grid.sizeHint())

        return control_panel
    
    Slot()
    def createSystem(self):

        """
        Called from the parameter toolbox, a system includes 
        EEPS model, control panel, and visualization display.
        Allows for multiple models to be created at once
        """

        # Separate agents exist on separate tabs

        self.tab = QGroupBox()
        self.tab_layout = QGridLayout()

        self.models[self.model_num] = {}
        self.models[self.model_num]['simulator'] = self.createSim(self.parameter_menu.agent_params, 
                                                                     self.parameter_menu.env_params)
        self.models[self.model_num]['main_display'] = self.createTable(self.models[self.model_num]['simulator']['sim'])
        self.models[self.model_num]['control_panel'] = self.createControlPanel(self.models[self.model_num]['main_display'],
                                                                               self.models[self.model_num]['simulator'])

        self.tab_layout.addLayout(self.models[self.model_num]['control_panel'], 0, 0)
        self.tab_layout.addWidget(self.models[self.model_num]['main_display'], 0, 1)

        self.tab.setLayout(self.tab_layout)

        self.tabs.addTab(self.tab, "Agent " + str(self.model_num))

        print(self.models[self.model_num])

        # NOTE: The command below allows Affinity to adjust dynamically
        #       as the user use it. However, it does result in some funky
        #       behavior. TODO: Fix fixed size behavior

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