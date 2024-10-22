# -*- coding: utf-8 -*-
"""
Last update: Dec. 26, 2019

@author:  Mahdi Rouzbahaneh

This is the main piece of code for Equivalence Projective Simulation model when
using interface for changing parameters and showing the results.

"""

import matplotlib
matplotlib.use("TkAgg")
import sys

sys.path.insert(0, 'gui')

import initialization_gui
import gui
import initialization_detail
import environment as env
import agent as agn
import interaction as intrc

def start(environment_parameter, agent_parameter, showMessage):
    """ 
    To open an interface, set parameters and simulate the given experiment
    """
    agent_ = agn.Agent(agent_parameter)
    agent = agent_.agent
    environment = env.Environment(environment_parameter)
    interaction = intrc.Interaction(agent, environment, agent_parameter,
                                  environment_parameter)
    interaction.run_save(showMessage)
    file_name = interaction.file_name
    print(file_name)
    return file_name 

environment_detail = initialization_detail.environment_details()
environment_parameter, agent_parameter = initialization_gui.config()
interface = gui.EquivalenceView(environment_parameter, agent_parameter, 
                                                environment_detail, start)

interface.mainloop()
