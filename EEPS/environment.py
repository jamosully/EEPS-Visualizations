# -*- coding: utf-8 -*-
"""
Last update: Sep. 2, 2020

@author: Asieh Abolpour Mofrad

This code is used for simulation results reported in an article entitled:
    ''Enhanced Equivalence Projective Simulation:
        a Framework for Modeling Formation of Stimulus Equivalence Classes"
        in Neural Computation, MIT Press.

"""

import numpy as np
import random
from string import ascii_uppercase

import EEPS.initialization_detail as inid

class Environment(object):

    """
    The Environment  (experimenter) based on the experiment details provides

    the training sets (percept and action set) and reflects the feedback (reward)

    to the agent based on its chosen match.

    The Environment evaluate the long-term results of the agent in a block of

    trials and decides if a specific match (say AB) passing the criteria

    and in this case  provides training trials for the next relation (say BC).

    There is no testing phase.
    """

    def __init__(self, parameter):

        """
        Initialize the basic EPS Environment from environment_parameters_details
        """

        num_classes, training_order, plot_blocks, plot_blocks_ID, mastery_training = \
        inid.environment_parameters_details(parameter["environment_ID"][0])

        self.num_classes = num_classes
        self.size_action_set = parameter["size_action_set"][0]
        self.autogenerate_classes = parameter["autogenerate_classes"][0]
        self.training_order = training_order
        self.mastery_training = mastery_training
        self.plot_blocks = plot_blocks
        self.plot_blocks_ID = plot_blocks_ID
        self.Training = True
        self.step = 1
        self.trial_no = 0
        self.correct = 0
        self.class_trial_count = dict()
        self.class_reward_count = dict()
        self.class_accuracies = dict()
        self.next_step = False
        self.new_block = True
        self.Block_list = []
        self.Block_results_training = {}
        self.Block_training_order = {}
        self.Training_over_time = {}
        self.num_iteration_training = {}
        self._preprocess()
        self.num_trials = 0

        for i in range(len(self.training_order)):
            self.Training_over_time[i+1] = []
            self.num_iteration_training[i+1] = 0

        for j in range(num_classes):
            self.class_accuracies[j + 1] = 0
            self.class_reward_count[j + 1] = 0
            self.class_trial_count[j + 1] = 0 


    def _preprocess(self): # Ok!

        """To make sure that self.training_order is in the proper format."""

        for k, v in self.training_order.items():
            new_list = []
            for pair in self.training_order[k]:
                if len(pair[0]) == 1:
                    for j in range(self.num_classes):
                        repeat_no = pair[2]//self.num_classes
                        percept = pair[0]+str(j+1)
                        action = pair[1]+str(j+1)
                        new_list += [(percept, action, repeat_no)]
            if new_list != []:
                self.training_order[k] = new_list


    def next_trial(self): #  Ok!

        """
        To send the next trial to the agent during training
        """

        if self.new_block:
            self.reset_block()
        else:
            self.next_step = False
        for k, v in self.Block_list[self.trial_no].items():
            percept = k
            action_set = v
            self.trial_no+=1
            if self.trial_no == self.num_trials:
                self.new_block = True

            return percept, action_set, self.next_step


    def form_block(self): # Ok!

        """
        This method forms a block for training based on the protocol.
        It returns a list of dictioniories where keys are percepts and values
        are the list of actions.
        """

        self.Block_list = []
        self.num_trials = 0
        use_class_range =  False

        if len(list(self.training_order.items())[0][1][1][0]) == 2 and not self.autogenerate_classes:
            self.class_ranges = self.obtain_class_ranges()
            use_class_range = True

        for pair in self.training_order[self.step]:
            repeat_no = pair[2]
            self.num_trials += repeat_no
            percept = pair[0]
            action = pair[1]
            if use_class_range:
                act_list = list(range(self.class_ranges[action[0]]))
            else:
                act_list = list(range(self.num_classes))
            act_list.remove(int(action[1])-1)
            for rpt in range(repeat_no):
                action_list = []
                action_list.append(str(action))
                if not self.autogenerate_classes and use_class_range:
                    if len(act_list) > 1:
                        comparison_list = np.random.choice(act_list,
                                                self.size_action_set-1, replace=False)
                    else:
                        comparison_list = [act_list[0]]
                else:
                    comparison_list = np.random.choice(act_list,
                                         self.size_action_set-1, replace=False)
                for k in comparison_list:
                    action_list.append(str(pair[1][0]+ str(k+1)))
                self.Block_list.append({percept: random.sample(action_list,
                                                            len(action_list))})
        
        return random.shuffle(self.Block_list)

    
    def obtain_class_ranges(self):

        class_ranges = {}

        stimuli = []
        for block in list(self.training_order.items()):
            for pair in block[1]:
                for x in range(2):
                    if pair[x][0] not in list(class_ranges.keys()):
                        class_ranges[pair[x][0]] = 0
                    if pair[x] not in stimuli:
                        stimuli.append(pair[x])
                        class_ranges[pair[x][0]] += 1

        return class_ranges


    def feedback(self, percept, action): # Ok!

        """
            This method returns the reward (1 or -1) based on the correct or
            incorrect match of percept and action.
        """
        self.class_trial_count[int(percept[1])] += 1

        if percept[1] == action[1]:
            reward = 1
            self.class_reward_count[int(percept[1])] += 1
            self.correct += 1
        else:
            reward = -1

        for x in range(self.num_classes):
            if self.class_trial_count[x + 1] != 0:
                self.class_accuracies[x + 1] = (self.class_reward_count[x + 1] / self.class_trial_count[x + 1])
            else:
                self.class_accuracies[x + 1] = 0

        print(self.class_accuracies)
        return reward


    def reset_block(self): # Ok!

        """
            This method makes a new block of trials based on the criteria.
        """

        if self.trial_no > 0:
            self.Training_over_time[self.step].append(self.correct/self.trial_no)
            self.num_iteration_training[self.step] += 1
            if (self.correct/self.trial_no) >= self.mastery_training:
                self.Block_results_training[self.step] = self.correct/self.trial_no
                self.Block_training_order[self.step] = [s[0]+s[1]
                for s in self.training_order[self.step]]
                self.step += 1
                self.next_step = True
                if self.step == len(self.training_order)+1:
                    self.Training = False

            self.trial_no=0
            self.correct = 0
        if self.Training:
            self.form_block()
            self.new_block = False