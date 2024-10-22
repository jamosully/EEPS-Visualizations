# -*- coding: utf-8 -*-
"""
Last update:  Dec. 24, 2019

@author: Asieh Abolpour Mofrad

To mediate the interaction between agent and environment objects
based on the protocol and initializations.

This code is used for simulation results reported in an article entitled:

"Equivalence Projective Simulation as a Framework for Modeling Formation of 
Stimulus Equivalence Classes" in Neurol Computation Journal

"""

import sys
import copy
import pickle

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns; sns.set()

class Interaction(object):

    """
    Interaction between agent and environment for Equivalence Projective Simulation
    """

    def __init__(self, agent, environment, agent_parameter, environment_parameter):

        """For a given agent, environment and their parameters, run the whole
        experiment and save the results under self.result_file_name.
        The results can be plotted using methods in the class

        """

        self.agent = copy.deepcopy(agent)

        self.environment = copy.deepcopy(environment)

        self.agent_parameter = agent_parameter

        self.environment_parameter = environment_parameter

        file_name = agent_parameter['agent_type']+'_Env_'+\
        str(environment_parameter['environment_ID'][0])+'_ExpID_'+ \
        str(environment_parameter['experiment_ID'][0])

        self.file_name = "results/{}.p".format(file_name)

        self.max_trial=environment_parameter['max_trial'][0]

    def run_experiment(self): 

        """ This method run the experiment for one agent/participant"""

        num_steps = 0
        while (self.environment.Training or self.environment.Testing):
            if num_steps == self.max_trial:
                sys.exit("UNABLE TO FINISH TRAINING WITHIN {} STEPS".format(
                                                               self.max_trial))

            percept, action_set_t=self.environment.next_trial()
            if self.environment.Training:
                num_steps += 1
                self.agent.trial_preprocess(percept, action_set_t)
                action = self.agent.action_selection(percept, action_set_t)
                reward = self.environment.feedback(percept,action)
                self.agent.training_update_network(percept, action_set_t,
                                                   action, reward)

            elif self.environment.Testing:
                action = self.agent.testing_action_selection(percept,
                                                             action_set_t)
                self.environment.test_update(percept, action)

    def experiment_results(self, callback):  

        """ This method run the experiment for num_agents and report the results"""

        num_agents = self.environment_parameter['num_agents'][0]
        agent_type = self.agent_parameter['agent_type']

        avg_time_training = {}
        avg_prob_training = {}
        avg_prob_testing = {}
        avg_exp_steps = {}

        env_test_clip = nx.DiGraph()
        env_test_aux = {}
        prob_training_clip = nx.DiGraph()
        prob_testing_clip = nx.DiGraph()

        agent = copy.deepcopy(self.agent)
        environment=copy.deepcopy(self.environment)
        for i_trial in range(num_agents):
            if callback == "":
                print("Iteration: ", i_trial)
            else:
                callback("Iteration: " + str(i_trial))

            self.environment=copy.deepcopy(environment)
            self.agent=copy.deepcopy(agent)

            self.run_experiment()

            for u, v, d in self.environment.env_results_test_clip.edges(data=True):
                d['weight'] /= self.environment.env_results_aux[u][v[0]]

            if i_trial == 0:
                avg_time_training = self.environment.num_iteration_training.copy()
                avg_prob_training = self.environment.Block_results_training.copy()
                avg_prob_testing = self.environment.Block_results_testing.copy()

                env_test_clip, env_test_aux=self.env_test_clip_update(
                                                    env_test_clip, env_test_aux)
                prob_training_clip = self.agent.unified_h_value_to_pr()
                equivalence_clip = self.agent.Network_update()
                prob_testing_clip = self.agent.unified_h_value_to_pr(
                                                              equivalence_clip)
                if agent_type == 'absorbing':
                    avg_exp_steps = self.agent.expected_steps_avg()
            else:
                if agent_type == 'absorbing':
                    avg_exp_steps=avg_exp_steps.add(self.agent.expected_steps_avg())

                for k, v in self.environment.num_iteration_training.items():
                    avg_time_training[k] += v
                for k, v in self.environment.Block_results_training.items():
                    avg_prob_training[k] += v
                for k, v in self.environment.Block_results_testing.items():
                    avg_prob_testing[k] += v

                env_test_clip,env_test_aux=self.env_test_clip_update(
                                                env_test_clip,env_test_aux)

                for u, v, d in self.agent.unified_h_value_to_pr().edges(data=True):
                    prob_training_clip[u][v]['weight'] += d['weight']

                equivalence_clip=self.agent.Network_update()
                for u, v, d in self.agent.unified_h_value_to_pr(
                                          equivalence_clip).edges(data = True):
                    prob_testing_clip[u][v]['weight'] += d['weight']

        for k, v in avg_time_training.items():
            avg_time_training[k] = v/ num_agents
        for k, v in avg_prob_training.items():
            avg_prob_training[k] = v/ num_agents
        for k, v in avg_prob_testing.items():
            avg_prob_testing[k] = v/ num_agents

        for u, v, d in env_test_clip.edges(data = True):
            d['weight'] /= num_agents

        for u, v, d in prob_training_clip.edges(data = True):
            d['weight'] /= num_agents

        for u, v, d in prob_testing_clip.edges(data = True):
            d['weight'] /= num_agents
        if agent_type == 'absorbing':
            avg_exp_steps = avg_exp_steps/ num_agents

        training_df = self.training_dataframe(self.environment.training_order,
                                          avg_time_training, avg_prob_training)
        results=[training_df, avg_prob_testing, env_test_clip,
                 prob_training_clip, prob_testing_clip, avg_exp_steps]

        return results

    def training_dataframe(self, training_order, avg_time_training,
                                                           avg_prob_training): 

        """
        To create a summery of training, including block size, average number of
        blocks and the final grade (mastery criteria).
        """

        train_list = []
        size_list = []
        time_list = []
        mastery_list = []
        for k,v in training_order.items():
            train = ''
            size=0
            for pair in v:
                train += pair[0]+pair[1]+', '
                size += pair[2]
            train_list.append(train)
            size_list.append(size)
            time_list.append(avg_time_training[k])
            mastery_list.append(avg_prob_training[k])
        df = pd.DataFrame({'Training': train_list,
                           'Block Size': size_list,
                            'Time': time_list,
                            'Mastery': mastery_list})
        return df

    def env_test_clip_update(self, clip, dic):

        """
        To record the test results for each connection in a graph. The block
        format and the order of trials is not important.
        """

        for u, v, d in self.environment.env_results_test_clip.edges(data = True):
            if clip.has_edge(u, v) == False:
                clip.add_edge(u, v, weight = d['weight'])
            else:
                clip[u][v]['weight'] += d['weight']

            if u not in dic:
                dic[u] = {}
                dic[u][v] = 1
            elif v not in dic[u]:
                dic[u][v] = 1
            else:
                dic[u][v] += 1
        return clip, dic

    def probability_categorization(self, clip_prob): 

        """
        This method recieves a clip network with probabilities and returns
        a new clip that nodes are categories say, 'A', 'B', with probabilities.
        """

        clip_category = nx.DiGraph()

        category = set()
        for node in clip_prob.nodes():
            category |= set(node[0])
        for ctg1 in category:
            for ctg2 in category- set([ctg1]):
                pr_sum_correct = 0
                pr_sum_wrong = 0
                OUT_Edges = []
                for node in clip_prob.nodes():
                    if node[0] == ctg1[0]:
                        OUT_Edges = [edge for edge in
                                   clip_prob.out_edges(node, data = True)
                                                         if edge[1][0] == ctg2]
                        for edge in OUT_Edges:
                            if edge[0][1] == edge[1][1]:
                                pr_sum_correct += edge[2]['weight']
                            else:
                                pr_sum_wrong += edge[2]['weight']
                if OUT_Edges != []:
                    ctg_pr = pr_sum_correct/(pr_sum_correct+ pr_sum_wrong)
                    clip_category.add_edge(ctg1, ctg2, weight = ctg_pr)

        return clip_category

    def agent_results_avg(self, relations, prob_dict): 

        """
        This method recieves a set of relations or category pairs like
        {1:['A1B1', 'A2B2'], 2:['C1B1', 'C2B2']} or {1:['AB', 'BC'], 2:['CB', 'CD']}
        and a dictionary which the keys are like 'A1B1' or 'AB' and values are
        a number (probability)
        Output: a dictionary like {1:0.93, 2:0.78} where the numbers are the
        average values
        """

        avg_relations = {}
        for k, v in relations.items():
            sum_prob = 0
            i = 0
            for relation in v:
                sum_prob += prob_dict[relation]
                i += 1
            avg_relations[k] = sum_prob/i

        return avg_relations

    def clip_to_dict(self, clip):

        """
        This method recieves a networkx graph and return its dictionary format.
        """

        clip_dic = {}
        for u, v, d in clip.edges(data = True):
            clip_dic[u+v] = d['weight']
        return clip_dic

    def clip_to_matrix(self,clip, nodelist=None): 

        """
        This method recieves a networkx graph and return its dictionary format.
        """

        if nodelist == None:
            Tr_nodelist = clip.nodes()
        Tr_matrix = nx.to_numpy_matrix(clip, nodelist = Tr_nodelist)

        return Tr_matrix

    def clip_to_table(self, clip, nodelist=None): 
        """
        This method recieves a networkx graph and return its dataframe
        """

        if nodelist == None:
            df_nodelist = sorted(clip.nodes())
        Table_clip = nx.to_pandas_adjacency(clip, nodelist=df_nodelist)

        return Table_clip

    def probability_marginal(self, clip):

        """
        This method computes the marginal probabilities to each category from
        probabilities.
        Output: the network clip with probabilities
        """

        clip_prob = clip.copy()
        category = self.agent.category_set(clip_prob)
        for node in clip_prob.nodes():
            for ctg in category:
                OUT_Edges=[edge for edge in
                           clip_prob.out_edges(node,data=True) if edge[1][0] == ctg]
                if len(OUT_Edges) != 0:
                    H_vector = [edge[2]['weight'] for edge in OUT_Edges]
                    for edge in OUT_Edges:
                        edge[2]['weight'] = edge[2]['weight'] / np.sum(H_vector)

        return clip_prob

    def run_save(self, callback): 

        """
        This is to save the results into pickle files for plotting
        and further calls.
        """

        results = self.experiment_results(callback)
        show,result = self.plot_data(results)

        Simulation_data = {}
        Simulation_data['agent_parameter'] = self.agent_parameter
        Simulation_data['environment_parameter'] = self.environment_parameter
        Simulation_data['show'] = show
        Simulation_data['result'] = result

        result_save = open( self.file_name , "wb" )
        pickle.dump(Simulation_data, result_save)
        result_save.close()

    def plot_data(self,results): 

        """
        To save results for plot in the self.filaname address, and training
        results in a latex file.
        """

        training_df, avg_prob_testing, env_test_clip, prob_training_clip,\
                                    prob_testing_clip, avg_exp_steps = results

#        tf=open('txt_'+ self.file_name[:-1]+'txt', 'w')
#        tf.write(training_df.to_latex())

        agent_ini = pd.DataFrame()
        environment_ini = pd.DataFrame()
        for k,v in self.agent_parameter.items():
            if k == 'agent_type':
                agent_ini[k] = [v]
            else:
                agent_ini[k] = [v[0]]
        for k,v in self.environment_parameter.items():
            environment_ini[k] = [v[0]]

#        tf.write(agent_ini.to_latex())
#        tf.write(environment_ini.to_latex())
#        tf.close()

        test_block_ID = self.environment.test_block_ID
        plot_blocks = self.environment.plot_blocks
        plot_blocks_ID = self.environment.plot_blocks_ID

        test_prob_dict = self.clip_to_dict(self.probability_categorization(
                prob_testing_clip))

        avg_prob_testing_clip = self.agent_results_avg(
                          self.environment.Block_testing_order, test_prob_dict)

        test_env_dict = self.clip_to_dict(self.probability_categorization(
                env_test_clip))

        show = []
        result = {}

        #----------- first result for the blocks
        key_indx = sorted(test_block_ID.keys())
        env_1 = [avg_prob_testing[k] for k in key_indx]
        agn_1 = [avg_prob_testing_clip[k] for k in key_indx]
        index = [test_block_ID[k] for k in key_indx]

        result_1 = pd.DataFrame({'Test Results': env_1,
                  'Connection Probabilities': agn_1}, index=index)

        show.append(('Block results','bar'))
        result['Block results'] = result_1

        #----------- second result for the relations
        index=sorted(test_prob_dict.keys())

        env_2 = [test_env_dict[k] for k in index]
        agn_2 = [test_prob_dict[k] for k in index]

        result_2 = pd.DataFrame({'Test Results': env_2,
                  'Connection Probabilities': agn_2}, index=index)

        show.append(('Relation results','bar'))
        result['Relation results'] = result_2

        #---------- results for plot_blocks
        if bool(plot_blocks): # returns True if the dict is not empty
            for k_ , v_ in plot_blocks.items():
                env_prob=self.agent_results_avg(v_, test_env_dict)
                agn_prob = self.agent_results_avg(v_, test_prob_dict)

                index = sorted(plot_blocks[k_].keys())
                index = plot_blocks_ID[k_]

                env_3 = [env_prob[k] for k in index]
                agn_3 = [agn_prob[k] for k in index]

                result_3 = pd.DataFrame({'Test Results': env_3,
                          'Connection Probabilities': agn_3}, index = index)
                show.append((k_, 'bar'))
                result[k_] = result_3

        if type(avg_exp_steps) != dict: # make sure it is a good condition
            result_4 = pd.DataFrame({'Expected transitions': avg_exp_steps.values},
                                  index = avg_exp_steps.index)

            show.append(('Transition number', 'bar'))
            result['Transition number'] = result_4

#---------------- Now for heatmap - for the clip connections

        result_5 = self.clip_to_table(prob_testing_clip)
        result_5 = result_5.round(3)
        show.append(('Clip pair probability', 'heatmap'))
        result['Clip pair probability'] = result_5

        result_6 = self.clip_to_table(self.probability_marginal(prob_testing_clip))
        result_6 = result_6.round(3)
        show.append(('Clip category pair probability', 'heatmap'))
        result['Clip category pair probability'] = result_6

        result_ = self.probability_categorization(prob_testing_clip)

        result_7 = self.clip_to_table(result_)
        show.append(('Clip category probability', 'heatmap'))
        result['Clip category probability'] = result_7

#---------------- for the environment connections
#
#        result_8 = self.clip_to_table(env_test_clip)
#        result_8 = result_8.round(3)
#        show.append(('Env. pair probability','heatmap'))
#        result['Env. pair probability'] = result_8
#
#        result_9 = self.clip_to_table(self.probability_marginal(env_test_clip))
#        result_9 = result_9.round(3)
#        show.append(('Env. category pair probability', 'heatmap'))
#        result['Env. category pair probability'] = result_9
#
#        result_ = self.probability_categorization(env_test_clip)
#        result_10 = self.clip_to_table(result_)
#        show.append(('Env. category probability','heatmap'))
#        result['Env. category probability'] = result_10

        return show, result

class Plot_results(object):

    """
    This class plot the results which has been stored in 'file name' location.

    """

    def __init__(self, file_name):

        self.file_name=file_name

    def showResults(self):

        """
        reads the data and desired representations and plot them,
        an alternative to plot_results method
        """

        resultFile = open(self.file_name, 'rb')
        data = pickle.load(resultFile)
        resultFile.close()
        for i in range(len(data['show'])):
            result = data['result'][data['show'][i][0]]
            showType = data['show'][i][1]
            name = data['show'][i][0] + '_' + showType

            # show the result
            if showType == 'bar':
                self.barDiagramShow(name, result)    # result is a dataframe
            elif showType == 'heatmap':
                self.heatmapShow(name, result)       # result is a dataframe

    def barDiagramShow(self,name,  data):

        """ bar plot"""

        data.plot(kind='bar',color=['royalblue','lightgreen', 'red','cyan'])
        plt.legend(fontsize = 20)
        plt.tick_params(labelsize = 20)
        plt.title(name,fontsize = 20)
        plt.ylabel('Correct match ratio', fontsize = 20)

        plt.tight_layout()
        plt.xticks( rotation=45, fontsize = 20, horizontalalignment = 'right')
        plt.show()
 # --------------------------------------------------------------------------

    def heatmapShow(self, name, data):

        """ heatmap plot"""

        fig, ax = plt.subplots()
        sns.heatmap(data, annot = True, annot_kws = {"size": 14}, linewidths=.15,
                                                                cmap="Blues") 
        plt.title(name,fontsize = 16)
        plt.tick_params(labelsize = 16)
        plt.tight_layout()
        plt.show()


    def print_setting(self):

        """ for printing the setting of the simulation in the consule"""

        resultFile = open(self.file_name, 'rb')
        data = pickle.load(resultFile)
        resultFile.close()

        agent_parameter = data['agent_parameter']
        environment_parameter = data['environment_parameter']

        agent_ini = pd.DataFrame()
        environment_ini = pd.DataFrame()
        for k,v in agent_parameter.items():
            if k == 'agent_type':
                agent_ini[k] = [v]
            else:
                agent_ini[k] = [v[0]]
        for k,v in environment_parameter.items():
            environment_ini[k] = [v[0]]

        print("---*Agent Setting*---", agent_ini, sep = '\n')
        print("\n---*Environment Setting*---", environment_ini, sep = '\n')
