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

        self.prev_file = False

    def update_parameters(self, agent_params, env_params):

        self.agent_parameter = agent_params
        self.environment_parameter = env_params
        print("Parameters updated")
    
    Slot()
    def initialize_model(self, step, main_display):

        # Load parameters from a file, if there is one

        if self.file_name is not None:
            # self.agent_parameter = self.data['agent_parameter']
            # self.environment_parameter = self.data['environment_parameter']
            self.prev_file = True
            self.sim_complete.emit()
            return

        self.agent = agn.Agent(self.agent_parameter)
        self.environment = env.Environment(self.environment_parameter)

        self.step = step

        # TODO: This is a lot of parameters to be passing, see if 
        #       you can reduce them

        self.interaction = intrc.Interaction(self.agent, 
                                                self.environment, 
                                                self.agent_parameter, 
                                                self.environment_parameter, 
                                                step, 
                                                main_display,
                                                self.mtx)
        
        # For the RDT visualizer
        main_display.rdtTab.createClassButtons(self.environment.num_classes)
            
    Slot()
    def run_sim(self):

        # Some thoughts on how to build modularity
        # Need to operate each step of the run_save function
        # at the top level of this model,
        # rather than in the bottom level in the interaction

        # run_save:
        # results = self.experiment_results()
        # show, result = self.plot_data(results)

        # Simulation_data = {}
        # Simulation_data['agent_parameter'] = self.agent_parameter
        # Simulation_data['environment_parameter'] = self.environment_parameter
        # Simulation_data['show'] = show
        # Simulation_data['result'] = result

        # result_save = open( self.file_name , "wb" )
        # pickle.dump(Simulation_data, result_save)
        # result_save.close()

        # Focus would be to overide this function
        # at the top level, from the simulator

        # Maybe users should pick their:
        # - experiment function
        # - loop function
        # - results function
        # - saving function

        # Maybe look at basics contained in projective simulation

        if self.interaction is not None:
            self.results = self.interaction.run_save()
            self.file_name = self.interaction.file_name
            self.sim_complete.emit()

    Slot()
    def continue_sim(self):

        if self.interaction is not None:
            self.interaction.continue_sim()
