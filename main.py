import sys

# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QGridLayout, QVBoxLayout, QStyleFactory, QTabWidget, QGroupBox
from PySide6.QtCore import Slot, Signal, QThread, QMutex, QWaitCondition

from simulator import Simulator
from visualization_display import VisualizationDisplay
from control_panel import ControlPanel
from parameter_toolbox import ParameterToolbox
from stimuli_editor import StimuliEditor

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

        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 4)

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

    def createStimuliEditor(self, main, simulator):

        """
        The editor allows modifications to the agent's clip-space
        via the graph network visualisation (and the heatmap
        visualisation at some point)
        """

        return StimuliEditor(self, main, simulator)

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

        control_panel = ControlPanel(main, simulator['sim'], simulator['thread'], simulator['mutex'])

        #self.setFixedSize(self.grid.sizeHint())

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
        self.models[self.model_num]['simulator'] = self.createSim(self.parameter_menu.model_agent_params, 
                                                                     self.parameter_menu.model_env_params)
        self.models[self.model_num]['main_display'] = self.createTable(self.models[self.model_num]['simulator']['sim'])
        self.models[self.model_num]['control_panel'] = self.createControlPanel(self.models[self.model_num]['main_display'],
                                                                               self.models[self.model_num]['simulator'])
        
        self.models[self.model_num]['main_display'].assign_control_panel(self.models[self.model_num]['control_panel'])

        self.models[self.model_num]['stim_editor'] = self.createStimuliEditor(self.models[self.model_num]['main_display'],
                                                                              self.models[self.model_num]['simulator']['sim'])
        
        self.models[self.model_num]['main_display'].assign_stim_editor(self.models[self.model_num]['stim_editor'])

        self.tab_layout.addWidget(self.models[self.model_num]['control_panel'], 0, 0)
        self.tab_layout.addWidget(self.models[self.model_num]['main_display'], 0, 1)
        self.tab_layout.addWidget(self.models[self.model_num]['stim_editor'], 0, 2)

        self.tab_layout.setColumnStretch(1, 3)

        self.tab.setLayout(self.tab_layout)

        self.tabs.addTab(self.tab, "Agent " + str(self.model_num))

        self.model_num += 1

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    #app.setStyle(QStyleFactory)

    widget = MainWindow()
    widget.resize(1400, 800)
    widget.show()
    widget.showMaximized()

    sys.exit(app.exec())