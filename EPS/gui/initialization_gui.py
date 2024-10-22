# -*- coding: utf-8 -*-
"""
Last update: Dec 26, 2019
 
@author: Asieh Abolpour Mofrad & Mahdi Rouzbahaneh
 
Initialization values
"""

# how the parameters are defined:
# default value, min, max, (hide, read, edit), (float, int, custome type), comment
 
def config():
    return environment_parameters(), agent_parameters()
 
 
def environment_parameters():
    """
    The initial setting data. which are positive digits.
    """
    environment_parameter = {
        "experiment_ID":[1, 0, None, "edit", "int",
        "A positive number which is used for saving the results"],
        "environment_ID":[1, 1, 9, "edit", "int",
        "The defult Experiment ID, more Experiments can be defined in initialization_detail.py"],
        "max_trial":[5000, 1000, None, "edit", "int",
        "The maximum number of allowed trials in the training phase"],
        "num_agents":[10, 1, None, "edit", "int",
        "The number of participants (agents); the output " +
        "results will be an average over num_agent independent simulations"],
        "size_action_set":[3, 2, "=[num_classes]", "edit", "int",
        "The number of comparison stimuli in the experiment."]} 
 
    return environment_parameter
 

 
def agent_parameters():
    """
    This is an initialization for agent parameters based on the agent type.
    """
    agent_types = ['positive_h','negative_h','viterbi','absorbing']
    policy_type = ['standard', 'softmax']
    category = ['True', 'False']
    nodal_theta = ['Not','Lin','Pow']
    types = {"agent_types": agent_types, "policy_type": policy_type, "category": category, "nodal_theta": nodal_theta}
 
    agent_parameter={
            'positive_h':
            {
            "policy_type":['standard',None,None,"edit","policy_type","The two alternative policy " +
                           "types are 'standard' and 'softmax'. adjusts the rule " +
                           "used to compute probabilities from h-values"],
            "beta_softmax":[0.05,0,None,"edit","float","probabilities are proportional " +
                            "to exp(beta*h_value). If policy_type = 'standard', " +
                            "this is irrelevant."],
            "K1":[1,0.0,None,"edit","float","K1 > 0 is the parameter for direct reinforcement"],
            "K2":[0.9,0.0,"[K1]","edit","float","0 < K2 < K1 is the parameter for symmetric " +
                  "reinforcement"],
            "K3":[ 0.5,0.0,"=[K1]/([size_action_set]-1)","edit","float"," 0 < K3 <= K1/(size_action_set -1) " +
                  "is parameter for direct reinforcement when a wrong match is chosen"],
            "K4":[0.45,0.0,"=[K2]/([size_action_set]-1)","edit","float","0 < K4 <= K2/(size_action_set -1) " +
                  "is parameter for symmetric reinforcement when a wrong match is chosen"],
            "gamma_damping":[0.0001,0,1,"edit","float","A float number between 0 and 1, " +
                             "controls forgetting/damping of h-values"],
            "memory_sharpness":[0.9,0,1,"edit","float","This is for 'standard' policy and controls " +
                                "transitivity relation formation"],
            "nodal_theta":['Lin', None,None,"edit","nodal_theta","Could be 'Not', 'Lin' or " +
                           "'Pow' and irrelevant for 'softmax' policy. " ],
                           #+
                           #"nodal_theta=Not: is the case that theta does not " +
                           #"change with nodal distance and equals memory sharpness " +
                           #"nodal_theta=Lin: is the case that theta changes " +
                           #"linearly with nodal distance and " +
                           #"nodal_theta=Pow: is the case that theta changes " +
                           #"with nodal distance in a power law format."],
             "gamma_nodal":[0.05,0,1,"edit","float","a parameter for computing nodal_theta " +
                            "for linear and power law cases"],
             "category":["False",None,None,"edit","category","By True " +
                         "marginal probabilities to each category is computed " +
                         "from h-values."]
             },
 
            'negative_h':
            {
            "policy_type":['softmax',None,None,"read","policy_type","the 'standard' policy " +
                           "type needs positive h-values."],
            "beta_softmax":[0.05,0,None,"edit","float","float >=0, probabilities are proportional " +
                            "to exp(beta*h_value)."],
            "K1":[1,0.0,None,"edit","float","K1 > 0 is the parameter for direct reinforcement"],
            "K2":[0.9,0.0,"[K1]","edit","float","0 < K2 < K1 is the parameter for symmetric " +
                  "reinforcement"],
            "gamma_damping":[0.001,0,1,"edit","float","A float number between 0 and 1, " +
                             "controls forgetting/damping of h-values"],
             "category":["False",None,None,"edit","category","By True " +
                         "marginal probabilities to each category is computed " +
                         "from h-values."]
             },
 
            'viterbi':
            {
            "policy_type":['standard',None,None,"edit","policy_type","The two alternative policy " +
                           "types are 'standard' and 'softmax'. adjusts the rule " +
                           "used to compute probabilities from h-values"],
            "beta_softmax":[0.05,0,None,"edit","float","float >=0, probabilities are proportional " +
                            "to exp(beta*h_value). If policy_type = 'standard', " +
                            "this is irrelevant."],
            "K1":[1,0.0,None,"edit","float","K1 > 0 is the parameter for direct reinforcement"],
            "K2":[0.9,0.0,"[K1]","edit","float","0 < K2 < K1 is the parameter for symmetric " +
                  "reinforcement"],
            "K3":[ 0.5,0.0,"=[K1]/([size_action_set]-1)","edit","float"," 0 < K3 <= K1/(size_action_set -1) " +
                  "is parameter for direct reinforcement when a wrong match is chosen"],
            "K4":[0.45,0.0,"=[K2]/([size_action_set]-1)","edit","float","0 < K4 <= K2/(size_action_set -1) " +
                  "is parameter for symmetric reinforcement when a wrong match is chosen"],
            "gamma_damping":[0.001,0,1,"edit","float","A float number between 0 and 1, " +
                             "controls forgetting/damping of h-values"],
            "memory_sharpness":[0.9,0,1,"edit","float","This is for 'standard' policy and shows " +
                                "how much memory is used. (compared to the " +
                                "direct memory)"],
            "nodal_theta":['Lin', None,None,"edit","nodal_theta","Could be 'Not', 'Lin' or " +
                           "'Pow' and irrelevant for 'softmax' policy. "],
                           #+
                           #"nodal_theta=Not: is the case that theta does not " +
                           #"change with nodal distance and equals memory sharpness " +
                           #"nodal_theta=Lin: is the case that theta changes " +
                           #"linearly with nodal distance and " +
                           #"nodal_theta=Pow: is the case that theta changes " +
                           #"with nodal distance in a power law format."],
             "gamma_nodal":[0.05,0,1,"edit","float","a parameter for computing nodal_theta " +
                            "for linear and power law cases"],
             "category":["False",None,None,"hide","category","Not relevant"]
             },
 
            'absorbing':
            {
            "policy_type":['standard',None,None,"edit","policy_type","The two alternative policy " +
                           "types are 'standard' and 'softmax'. adjusts the rule " +
                           "used to compute probabilities from h-values"],
            "beta_softmax":[0.05,0,None,"edit","float","float >=0, probabilities are proportional " +
                            "to exp(beta*h_value)."],
            "K1":[1,0.0,None,"edit","float","K1 > 0 is the parameter for direct reinforcement"],
            "K2":[0.9,0.,"[K1]","edit","float","0 < K2 < K1 is the parameter for symmetric " +
                  "reinforcement"],
            "K3":[ 0.5,0.0,"=[K1]/([size_action_set]-1)","edit","float","0 < K3 <= K1/(size_action_set -1) " +
                  "is parameter for direct reinforcement when a wrong match is chosen"],
            "K4":[0.45,0.0,"=[K2]/([size_action_set]-1)","edit","float","0 < K4 <= K2/(size_action_set -1) " +
                  "is parameter for symmetric reinforcement when a wrong match is chosen"],
            "gamma_damping":[0.001,0,1,"edit","float","A float number between 0 and 1, " +
                             "controls forgetting/damping of h-values"],
             "category":["False",None,None,"hide","category","Not relevant"]
             }
        }
 
    return types, agent_parameter
