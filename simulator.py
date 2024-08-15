# UI Modules
from PySide6 import QtCore
from PySide6.QtCore import Slot, Signal

# EEPS Modules
import EEPS.initialization as initialization
import EEPS.initialization_detail as initialization_detail
import EEPS.environment as env
import EEPS.agent as agn
import EEPS.interaction as intrc

import pickle

"""
simulator.py

Responsible for intializing, running, and displaying
results from EEPS. All parameters obtained from a
parameter toolbox
"""

class Simulator(QtCore.QObject):

    """
    Contains all objects related to EEPS \n
    Runs on separate thread to rest of GUI
    """

    sim_complete = Signal()

    def __init__(self, mutex, agent_params, env_params, filename):
        QtCore.QObject.__init__(self)
        self.mtx = mutex
        self.agent_parameter = agent_params
        self.file_name = filename
        self.environment_parameter = env_params
    
    Slot()
    def initialize_model(self, step, memory_visualizer, rdt_visualizer, heat_visualizer):

        # Load parameters from a file, if there is one

        if self.file_name is not None:
            self.open_file()
            self.agent_parameter = self.data['agent_parameter']
            self.environment_parameter = self.data['environment_parameter']

        self.agent = agn.Agent(self.agent_parameter)
        self.environment = env.Environment(self.environment_parameter)

        # TODO: This is a lot of parameters to be passing, see if 
        #       you can reduce them

        self.interaction = intrc.Interaction(self.agent, 
                                                self.environment, 
                                                self.agent_parameter, 
                                                self.environment_parameter, 
                                                step, 
                                                memory_visualizer,
                                                rdt_visualizer,
                                                heat_visualizer,
                                                self.mtx)
        
        # For the RDT visualizer
        rdt_visualizer.createClassButtons(self.environment.num_classes)
            
    Slot()
    def run_sim(self):

        if self.interaction is not None:
            self.results = self.interaction.run_save()
            self.file_name = self.interaction.file_name
            self.sim_complete.emit()

    Slot()
    def continue_sim(self):

        if self.interaction is not None:
            self.interaction.continue_sim()
