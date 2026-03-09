# -*- coding: utf-8 -*-
"""
This is a modified version of the environment script created by
Asieh Abolpour Mofrad.

"""

import numpy as np
import random
from string import ascii_uppercase
import json

import EEPS.initialization_detail as inid

class Environment(object):

    """
    This environment is streamlined for RFT-based experiments, where
    an additional contextual cue is passed in the experiment
    """

    def __init__(self, environment_num, env_params):

        """
        Initialize the basic EPS Environment from environment_parameters_details
        """

        # Obtain results from initialization_detail file
        # TODO: Replace with JSON approach
        self.num_classes, self.training_order, self.plot_blocks, self.plot_blocks_ID, self.mastery_training = \
        list(self.open_environment_config(environment_num).values())
        print(self.num_classes)
        # self.environment_config = self.open_environment_config(environment_num)
        # print(self.environment_config.items())
        # self.training_order = self.environment_config["training_order"]
        # self.num_classes = self.environment_config["num_classes"]
        # self.mastery_training = self.environment_config["mastery_training"]
        # self.plot_blocks = self.environment_config["plot_blocks"]

        # Obtain parameters set in Affinity/initialization script
        # self.size_action_set = env_params["size_action_set"][0]
        self.size_action_set = 2
        self.autogenerate_classes = False
        #self.autogenerate_classes = env_params["autogenerate_classes"][0]

        self.Training = True
        self.testing_phase = False
        self.progress = False

        if not all(isinstance(key, int) for key in self.training_order.keys()):
            self.steps = list(self.training_order.keys())
            self.step_counter = 0
            self.step = self.steps[self.step_counter]
        else:    
            self.step = 1
        
        self.create_RDT_variables()

        self.next_step = False
        self.new_block = True
        self.counter_conditioning = False
        self.Block_list = []
        self.Block_results_training = {}
        self.Block_training_order = {}
        self.Training_over_time = {}
        self.num_iteration_training = {}
        self._preprocess()
        self.num_trials = 0

        for i in range(len(self.training_order)):
            self.Training_over_time[self.steps[i]] = []
            self.num_iteration_training[self.steps[i]] = 0

    def open_environment_config(self, experiment_no):

        """
        Opens the environment JSON file to select experiments
        """

        with open("RFT/rft_experiments.json", "r") as config_file:
            return json.load(config_file)[experiment_no]

    def create_RDT_variables(self):

        """
        Create the variables necessary for tracking RDT behavior
        """

        self.trial_no = 0
        self.correct = 0
        self.class_trial_count = dict()
        self.class_reward_count = dict()
        self.class_accuracies = dict()
        self.transition_trial = False

        for j in range(self.num_classes):
            self.class_accuracies[j + 1] = 0
            self.class_reward_count[j + 1] = 0
            self.class_trial_count[j + 1] = 0 

    def _preprocess(self): # Ok!

        """
        To make sure that self.training_order is in the proper format
        """

        for k, v in self.training_order.items():
            new_list = []
            for step in self.training_order[k]:
                if len(step["sample"]) == 1:
                    for j in range(self.num_classes):
                        repeat_no = step["repeat_num"] // self.num_classes
                        percept = step["sample"] + str(j+1)
                        action = step["comparison"] + str(j+1)
                        contextual_cue = step["contextual_cue"] + str(j + 1)
                        new_list += [(percept, action, contextual_cue, repeat_no)]
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
            self.transition_trial = False
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

        TODO: EDIT TO WORK WITH JSON FILE
        """

        self.Block_list = []
        self.num_trials = 0
        use_class_range =  False

        print(list(self.training_order.items()))
        if len(list(self.training_order.items())[0][1][0]["sample"]) == 2 and not self.autogenerate_classes:
            self.class_ranges = self.obtain_class_ranges()
            use_class_range = True

        for step in self.training_order[self.step]:
            repeat_no = step["repeat_num"]
            self.num_trials += repeat_no
            percept = step["sample"]
            action = step["comparison"]

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
                    action_list.append(str(step["comparison"][0]+ str(k + 1)))
                self.Block_list.append({percept: random.sample(action_list,
                                                            len(action_list))})
        
        return random.shuffle(self.Block_list)

    
    def obtain_class_ranges(self):

        # TODO: EDIT TO WORK WITH JSON
        
        class_ranges = {}

        stimuli = []
        for block in list(self.training_order.items()):
            for step in block[1]:
                for stimulus in [step["sample"], step["comparison"]]:
                    if stimulus[0] not in list(class_ranges.keys()):
                        class_ranges[stimulus[0]] = 0
                    if stimulus not in stimuli:
                        stimuli.append(stimulus)
                        class_ranges[stimulus[0]] += 1

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

        return reward
    
    def reset_block(self): # Ok!

        """
        This method makes a new block of trials based on the criteria.

        TODO: EDIT TO WORK WITH JSON APPROACH
        """

        if self.trial_no > 0:

            self.Training_over_time[self.step].append(self.correct/self.trial_no)
            self.num_iteration_training[self.step] += 1

            # Check if the agent has passed mastery for this specific training phase
            if (self.correct/self.trial_no) >= self.mastery_training or self.progress:
                self.Block_results_training[self.step] = self.correct/self.trial_no
                self.Block_training_order[self.step] = [s["sample"] + s["comparison"] for s in self.training_order[self.step]]
                self.progress = False

                if isinstance(self.step, int):
                    self.step += 1
                    self.next_step = True
                    if self.step == len(self.training_order)+1:
                        self.Training = False
                else:
                    self.step_counter += 1
                    self.next_step = True
                    if self.step_counter == len(self.training_order):
                        self.Training = False
                    else:
                        self.step = self.steps[self.step_counter]
                        if "test" in self.step:
                            self.Training = False
                            self.testing_phase = True

            self.trial_no=0
            self.correct = 0
        if self.Training:
            self.form_block()
            self.new_block = False

    def complete_testing_phase(self):

        """
        Utilised by the interaction class to move onto the next stage of
        training once a testing phase has been complete
        """

        self.testing_phase = False
        self.Training = True
        self.progress = True