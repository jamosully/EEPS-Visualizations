# -*- coding: utf-8 -*-
"""
Last update:  Dec. 26, 2019
 
@author: Asieh Abolpour Mofrad & Mahdi Rouzbahaneh
 
Initialization values 
"""

def config():
    return environment_parameters(), agent_parameters()
 
def environment_parameters():
    
    """
    The initial setting data. which are positive digits.
    Experiment_ID: is for saving the results
    environment_ID: is the ID of experiment (say protocol sheet)
    num_agents: The results is an average over this value
    size_action_set: is to be the number of comparison stimuli (actions) in each trial
    """
    
    environment_parameter = {"experiment_ID": [0],
        "environment_ID": [1],
        "max_trial": [10000],
        "num_agents": [1000],
        "size_action_set": [2]}
 
    return environment_parameter

def agent_parameters():

    """
    This is an initialization for agent parameters based on the agent type.
    """

    agent_types = ['positive_h', 'negative_h', 'viterbi', 'absorbing']
    policy_type = ['standard', 'softmax']
    category = ['True', 'False']
    nodal_theta = ['Not', 'Lin', 'Pow']
    types = {"agent_types": agent_types, "policy_type": policy_type, 
                              "category": category, "nodal_theta": nodal_theta}
 
    agent_parameter = {
            'positive_h':
            {
            "policy_type": ['standard'],
            "beta_softmax": [0.02],
            "K1": [1],
            "K2": [0.9],
            "K3": [0.5],
            "K4": [0.45],
            "gamma_damping": [0.01],
            "memory_sharpness": [0.5],
            "nodal_theta": ['Lin'],
            "gamma_nodal": [0.8],
            "category": ["False"]
             },
 
            'negative_h':
            {
            "policy_type": ['softmax'],
            "beta_softmax": [0.05],
            "K1": [1],
            "K2": [0.9],
            "gamma_damping": [0.001],
            "category": ["False"]
             },
 
            'viterbi':
            {
            "policy_type": ['standard'],
            "beta_softmax": [0.05],
            "K1": [1],
            "K2": [0.9],
            "K3": [0.5],
            "K4": [0.45],
            "gamma_damping": [0.001],
            "memory_sharpness": [1],
            "nodal_theta": ['Not'],
            "gamma_nodal": [0.05],
            "category": ["False"]
             },
 
            'absorbing':
            {
            "policy_type": ['standard'],
            "beta_softmax": [0.05],
            "K1": [1],
            "K2": [0.9],
            "K3": [0.5],
            "K4": [0.45],
            "gamma_damping": [0.001],
            "category": ["False"]
             }
        }
 
    return types, agent_parameter
