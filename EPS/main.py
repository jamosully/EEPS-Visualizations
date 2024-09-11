# -*- coding: utf-8 -*-
"""
Last update: Dec. 26, 2019
 
@author: Asieh Abolpour Mofrad 
 
This is the main piece of code for Equivalence Projective Simulation model.
    
This code is used for simulation results reported in an article entitled:

"Equivalence Projective Simulation as a Framework for Modeling Formation of 
Stimulus Equivalence Classes" in Neurol Computation Journal
 
"""

import initialization
import initialization_detail
import environment as env
import agent as agn
import interaction as intrc

environment_detail = initialization_detail.environment_details()
environment_parameter, agent_parameter = initialization.config()

#Give the file_name to just plot a previousely saved simulation
file_name = None

if file_name is None:
    agent_types = ('positive_h', 'negative_h', 'viterbi', 'absorbing')
    agent_ID = 0
    agent_parameter[1][agent_types[agent_ID]]['agent_type'] = agent_types[agent_ID]
    agent_parameter_ = agent_parameter[1][agent_types[agent_ID]]
    agent_ = agn.Agent(agent_parameter_)
    agent = agent_.agent
    environment = env.Environment(environment_parameter)
    interaction = intrc.Interaction(agent, environment, agent_parameter_,
                                                        environment_parameter)
    interaction.run_save("")
    file_name = interaction.file_name
    print(file_name)

plt_ = intrc.Plot_results(file_name)
plt_.showResults()
plt_.print_setting()

