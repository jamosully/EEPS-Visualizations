# -*- coding: utf-8 -*-
"""
Last update:  Dec. 26, 2019

@author: Asieh Abolpour Mofrad

This code is used for simulation results reported in an article entitled:
    
"Equivalence Projective Simulation as a Framework for Modeling Formation of 
Stimulus Equivalence Classes" in Neurol Computation Journal
"""

import numpy as np
import random
import networkx as nx

import initialization_detail as inid

class Environment(object):

    """
    The Environment  (experimenter) based on the experiment details provides

    the training sets (percept and action set) and reflects the feedback (reward)

    to the agent based on its chosen match.

    The Environment evaluate the long-term results of the agent in a block of

    trials and decides if a specific match (say AB) passing the criteria

    and in this case  provides training trials for the next relation (say BC).

    After mastery of all training relations, the testing trials are given to the

    agent without feedback.
    """

    def __init__(self, p):

        """ 
        Initialize the basic PS Environment, p contains the details from 
        initialization_detail file

            - num_classes: integer >=2

            - size_action_set: integer >=2, where size_action_set <= num_classes

            - training order: a dictionary of list of tuples like [('A','B'),('B','C')]

            - testing_order:
                a dictionary of list of tuples like
                {1:[('A','B'),('B','C')],2:[('B','A'),('A','C'),('C','B')]

            - mastery_training: a float number in (0,1)
        """
        
        num_classes, training_order, testing_order, test_block_ID,plot_blocks,\
        plot_blocks_ID, mastery_training = \
        inid.environment_parameters_details(p["environment_ID"][0])

        self.num_classes = num_classes
        self.size_action_set = p["size_action_set"][0]
        self.training_order = training_order
        self.mastery_training = mastery_training
        self.testing_order = testing_order
        self.Training = True
        self.Testing = True
        self.step = 1
        self.t = 0
        self.correct = 0
        self.new_block = True

        if self.Training:
            self.trial_order = self.training_order.copy()
            self._preprocess()
            self.num_trials = 0

        self.Block_list = []
        self.Block_results_training = {}
        self.Block_results_testing = {}
        self.Block_training_order = {}
        self.Block_testing_order = {}
        self.Training_over_time = {}
        self.num_iteration_training = {}

        for i in range(len(self.trial_order)):
            self.Training_over_time[i+1] = []
            self.num_iteration_training[i+1] = 0

        for i in range(len(self.testing_order)):
            self.Block_testing_order[i+1] = [s[0]+s[1] for s in self.testing_order[i+1]]

        self.test_block_ID = test_block_ID
        self.plot_blocks = plot_blocks
        self.plot_blocks_ID = plot_blocks_ID
        self.env_results_test_clip = nx.DiGraph()
        self.env_results_aux = {}

    def _preprocess(self): 

        """To make sure that self.training_order is in the proper format."""

        for k,v in self.trial_order.items():
            new_list = []
            for pair in self.trial_order[k]:
                if len(pair[0]) == 1:
                    for j in range(self.num_classes):
                        repeat_no = pair[2]//self.num_classes
                        percept = pair[0]+str(j+1)
                        action = pair[1]+str(j+1)
                        new_list += [(percept, action, repeat_no)]
            if new_list != []:
                self.trial_order[k] = new_list

    def next_trial(self): 
        
        """
        To send the next trial to the agent, either in training, or testing phase.
        """
        
        if self.new_block:
            self.reset_block()
        if self.Testing:
            for k,v in self.Block_list[self.t].items():
                percept = k
                action_set = v
                self.t+=1
                if self.t == self.num_trials:
                    self.new_block = True

                return percept, action_set
        else:
            return  self.Training, self.Testing

    def form_block(self): 
        
        """
        This method forms a block for training or testing based on the protocol.
        It returns a list of dictioniories where keys are percepts and values
        are the list of actions.
        """

        self.Block_list=[]
        self.num_trials = 0
        for pair in self.trial_order[self.step]:
            repeat_no = pair[2]
            self.num_trials += repeat_no
            percept = pair[0]
            action = pair[1]
            act_list = list(range(self.num_classes))
            act_list.remove(int(action[1])-1)
            for rpt in range(repeat_no):
                action_list = []
                action_list.append(str(action))
                comparison_list = np.random.choice(act_list, 
                                         self.size_action_set-1, replace=False)
                for k in comparison_list:
                    action_list.append(str(pair[1][0]+ str(k+1)))
                self.Block_list.append({percept: random.sample(action_list,
                                                            len(action_list))})
        return random.shuffle(self.Block_list)

    def feedback(self,percept,action): 
        
        """
            This method returns the reward (1 or -1) based on the correct or
            incorrect match of percept and action.
        """
        
        if percept[1] == action[1]:
            reward = 1
            self.correct += 1
        else:
            reward = -1
        return reward

    def reset_block(self): 
        
        """
            This method makes a new block of trials based on the criteria.
        """
        
        if self.t > 0:
            if self.Training:
                self.Training_over_time[self.step].append(self.correct/self.t)
                self.num_iteration_training[self.step] += 1
                if (self.correct/self.t) >= self.mastery_training:
                    self.Block_results_training[self.step] = self.correct/self.t
                    self.Block_training_order[self.step] = [s[0]+s[1]
                     for s in self.trial_order[self.step]]
                    self.step += 1
                    self.continuation_check()
            else:
                self.Block_results_testing[self.step] = self.correct/self.t
                self.step += 1
                self.continuation_check()
            self.t=0
            self.correct = 0
        if (self.Testing or self.Training):
            self.form_block()
            self.new_block = False

    def continuation_check(self): 
        
        """
            This method is to check if training is finished and move to the test
            phase (by turning self.Training = False)
            If self.Training = False checks if the testing phase is finished
            and end the process in that case (by turning self.Testing = False).
        """
        
        if self.Training:
            if self.step == len(self.trial_order)+1:
                self.Training = False
                self.trial_order = self.testing_order.copy()
                self._preprocess()
                # To invert the [('A','B',10)] to [('A1','B1',5),('A2','B2',5)]
                self.step = 1

        elif self.Testing:
            if self.step == len(self.trial_order)+1:
                self.Testing = False

    def test_update(self, percept, action):
        
        """
            This method save test results on a directed graph
        """
        
        if percept not in self.env_results_aux:
            self.env_results_aux[percept] = {}
            self.env_results_aux[percept][action[0]] = 1
        elif action[0] not in self.env_results_aux[percept]:
            self.env_results_aux[percept][action[0]] = 1
        else:
            self.env_results_aux[percept][action[0]] += 1

        if self.env_results_test_clip.has_edge(percept,action) == False:
            self.env_results_test_clip.add_edge(percept, action, weight=1)
        else:
            self.env_results_test_clip[percept][action]['weight'] += 1

        if percept[1] == action[1]:
            self.correct += 1
