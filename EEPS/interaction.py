# -*- coding: utf-8 -*-
"""
Last update: Sep. 2, 2020

@author: Asieh Abolpour Mofrad

To mediate the interaction between agent and environment objects
based on the protocol and initializations.

This code is used for simulation results reported in an article entitled:
    ''Enhanced Equivalence Projective Simulation:
        a Framework for Modeling Formation of Stimulus Equivalence Classes"
        in Neural Computation, MIT Press.

"""

import sys
import copy
import pickle
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import networkx as nx
#import netgraph
import matplotlib.colors as mcolors
import matplotlib.animation
import seaborn as sns; sns.set()
import pdb


class Interaction(object):

    """
    Interaction between agent and environment for Equivalence Projective Simulation
    """

    def __init__(self, 
                 agent, 
                 environment, 
                 agent_parameter, 
                 environment_parameter, 
                 vis_step,
                 vis_display,
                 wait_signal):

        """
        For a given agent, environment and their parameters, run the whole
        experiment and save the results under self.result_file_name.
        The results can be plotted using methods in the class
        """

        self.agent = copy.deepcopy(agent)
        self.environment = copy.deepcopy(environment)
        self.agent_parameter = agent_parameter
        self.environment_parameter = environment_parameter
        self.max_trial = environment_parameter['max_trial'][0]
        self.vis_step = vis_step
        file_name = 'Env_'+ str(environment_parameter['environment_ID'][0])+ \
        '_ExpID_'+ str(environment_parameter['experiment_ID'][0])
        self.file_name = "results/{}.p".format(file_name)#
        self.vis_display = vis_display
        self.pause = wait_signal
        self.num_steps = 0
        self.artists = {}
        self.current_phase = []
        self.figure, self.ax = plt.subplots()

    def run_experiment(self): # Ok!

        """ This method run the experiment for one agent/participant"""

        # TODO: Need a way to jump out of the for loop to update the model's parameters

        self.num_steps = 0
        for self.num_steps in range(self.max_trial):

            percept, action_set_t, new_trial = self.environment.next_trial()

            if self.environment.Training is not True:
                break

            self.agent.trial_preprocess(percept, action_set_t, new_trial)
            action = self.agent.action_selection(percept, action_set_t)
            reward = self.environment.feedback(percept, action)
            self.agent.training_update_network(percept, action_set_t,
                                               action, reward, new_trial)
            #print(self.agent.clip_space.nodes)
            # self.artists[self.num_steps] = nx.Graph.copy(self.agent.clip_space)
            # self.current_phase.append("Phase " + str(self.environment.step))
            #print(self.artists)
            if self.vis_display is not None:
                self.vis_display.rdtTab.track_rdt_data(self.agent.clip_space, self.environment.class_accuracies, new_trial)
                if self.num_steps % self.vis_step == 0:
                    self.vis_display.rdtTab.visualize_rdt_data(self.agent.clip_space)
                    self.vis_display.networkTab.visualize_network(self.agent.clip_space)
                    self.vis_display.heatmapTab.visualize_heatmaps(self.agent.clip_space)
                    self.vis_display.change_step_counter(self.num_steps)
                    self.pause.lock()
                    if self.vis_display.edits_made:
                        self.agent.clip_space = self.vis_display.update_clip_space()
                    if self.vis_display.step_changed:
                        self.vis_step = self.vis_display.update_step_count()

        if self.num_steps == self.max_trial:
            sys.exit("UNABLE TO FINISH TRAINING WITHIN {} STEPS".format(
                                                            self.max_trial))

    def experiment_results(self): # Ok!

        """ This method run the experiment for num_agents and report the results"""

        num_agents = self.environment_parameter['num_agents'][0]

        avg_time_training = {}
        avg_prob_training = {}
        avg_NE_itr = 0

        agent = copy.deepcopy(self.agent)
        environment = copy.deepcopy(self.environment)

        for i_trial in range(num_agents):
            if i_trial > 0:
                self.vis_display.rdtTab.prepare_for_next_agent()
            self.environment = copy.deepcopy(environment)
            self.agent = copy.deepcopy(agent)
            self.run_experiment()

            if self.vis_display is not None:
                self.vis_display.rdtTab.visualize_rdt_data(self.agent.clip_space)
                self.vis_display.networkTab.visualize_network(self.agent.clip_space)
                self.vis_display.heatmapTab.visualize_heatmaps(self.agent.clip_space)

            self.artists[self.num_steps] = self.agent.clip_space
            #self.figure.clear()
            
            if i_trial == 0:
                avg_time_training = self.environment.num_iteration_training.copy()
                avg_prob_training = self.environment.Block_results_training.copy()
                prob_training_clip = self.agent.softmax_matrix()
                W_in, P, Tau, prob_testing_clip = self.agent.Network_Enhancement()
                prob_testing_clip_marginalized = self.agent.marginalized_probability(prob_testing_clip)
                prob_testing_clip_category = self.agent.probability_categorization(prob_testing_clip_marginalized)
                avg_NE_itr += self.agent.NE_itr
                final_clip_space = nx.DiGraph(self.agent.reverse_ne_for_graph(prob_testing_clip, self.agent.beta_h))

            else:
                for k, v in self.environment.num_iteration_training.items():
                    avg_time_training[k] += v

                for k, v in self.environment.Block_results_training.items():
                    avg_prob_training[k] += v

                prob_training_clip += self.agent.softmax_matrix()
               # prob_testing_clip += self.agent.Network_Enhancement()
                W_in_, P_, Tau_, W_new_ = self.agent.Network_Enhancement()
                W_in += W_in_
                P += P_
                Tau += Tau_
                prob_testing_clip += W_new_
                prob_testing_clip_marginalized += self.agent.marginalized_probability(prob_testing_clip)
                prob_testing_clip_category += self.agent.probability_categorization(prob_testing_clip_marginalized)
                avg_NE_itr += self.agent.NE_itr
                final_clip_space = nx.DiGraph(self.agent.reverse_ne_for_graph(W_new_, self.agent.beta_h))
   
            for i in range(20):
                self.artists[self.num_steps + (i + 1)] = final_clip_space
                self.current_phase.append("Network Enhancement")
            if self.vis_display is not None:
                self.vis_display.rdtTab.track_rdt_data(final_clip_space, self.environment.class_accuracies, self.environment.next_step)
                self.vis_display.rdtTab.visualize_rdt_data(final_clip_space)
                self.vis_display.networkTab.visualize_network(final_clip_space)
                self.vis_display.heatmapTab.visualize_heatmaps(final_clip_space)
                self.vis_display.change_step_counter(self.num_steps)

        # community_dict = {}

        # for stimuli in self.artists[self.num_steps]:
        #     community_dict[stimuli] = int(stimuli[1]) - 1
        
        # self.key_positions = []
        # self.fixed_positions = {}
        # self.pos_ready = False
        
        # final_pos = self.community_layout(self.artists[self.num_steps], community_dict)

        # self.key_positions = ["A1", "A2", "A3", "A4"]
        # self.fixed_positions = {k: final_pos[k] for k in self.key_positions}
        # self.pos_ready = True

        # xy = np.array(list(final_pos.values()))
        # self.x_min, self.y_min = np.min(xy, axis=0)
        # self.x_max, self.y_max = np.max(xy, axis=0)
        # self.pad_by = 0.05 # may need adjusting 
        # self.pad_x, self.pad_y = self.pad_by * np.ptp(xy, axis=0)

        # plt.xlim(self.x_min - self.pad_x, self.x_max + self.pad_x)
        # plt.ylim(self.y_min - self.pad_y, self.y_max + self.pad_y)
        
        # try:
        #     ani = matplotlib.animation.FuncAnimation(fig=self.figure, func=self.plot_and_save_graph, interval=40)
        #     #plt.show()
        #     ani.save(filename="test.mp4", writer="ffmpeg")
        # except IndexError:
        #     print("Hahah")
        #ani.save(filename="test.gif", writer="PillowWriter")


        for k, v in avg_time_training.items():
            avg_time_training[k] = v/ num_agents

        for k, v in avg_prob_training.items():
            avg_prob_training[k] = v/ num_agents

        prob_training_clip /= num_agents
        prob_testing_clip  /= num_agents
        prob_testing_clip_marginalized /= num_agents
        prob_testing_clip_category /= num_agents
        W_in /= num_agents
        P /= num_agents
        Tau /= num_agents

        training_df = self.training_dataframe(self.environment.training_order,
                                        avg_time_training, avg_prob_training)

        avg_NE_itr /= num_agents
        print('average number iteration', avg_NE_itr)

        results = [training_df, prob_training_clip, prob_testing_clip,
                   prob_testing_clip_marginalized, prob_testing_clip_category,
                   avg_NE_itr, W_in, P, Tau]

        return results

    def training_dataframe(self, training_order, avg_time_training,
                                                           avg_prob_training): # Ok!

        """
        To create a summery of training, including block size, average number of
        blocks and the final grade (mastery criteria).
        """

        train_list = []
        if self.vis_display is not None:
            trial_list = np.mean(self.vis_display.rdtTab.transition_trials, axis=0)
        size_list = []
        time_list = []
        mastery_list = []
        for k, v in training_order.items():
            train = ''
            size=0
            for pair in v:
                train += pair[0]+pair[1]+', '
                size += pair[2]
            train_list.append(train)
            size_list.append(size)
            time_list.append(avg_time_training[k])
            mastery_list.append(avg_prob_training[k])
        if self.vis_display is not None:
            df = pd.DataFrame({'Training': train_list,
                            'Block Size': size_list,
                                'Time': time_list,
                                "Trials Required": trial_list,
                                'Mastery': mastery_list})
        else:
            df = pd.DataFrame({'Training': train_list,
                            'Block Size': size_list,
                                'Time': time_list,
                                'Mastery': mastery_list})
        return df


    def agent_results_avg(self, relations, prob_dict): #Ok!

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
            avg_relations[k] = np.divide(sum_prob, i)

        return avg_relations


    def df_to_dict(self, df): #Ok!

        """
        This method recieves a dataframe and return its dictionary format.
        """

        df_dict = {}
        for row in df.index:
            for col in df.columns:
                df_dict[row + col] = df.at[row, col]

        return df_dict


    def run_save(self): # Ok!

        """
        This is to save the results into pickle files for plotting
        and further calls.
        """

        results = self.experiment_results()
        show, result = self.plot_data(results)

        Simulation_data = {}
        Simulation_data['agent_parameter'] = self.agent_parameter
        Simulation_data['environment_parameter'] = self.environment_parameter
        Simulation_data['show'] = show
        Simulation_data['result'] = result

        result_save = open( self.file_name , "wb" )
        pickle.dump(Simulation_data, result_save)
        result_save.close()


    def plot_data(self, results): # Ok!

        """
        To save results for plot in the self.filaname address, and training
        results in a latex file.
        """

#        self.save_latex(results)

        training_df, prob_training_clip, prob_testing_clip, \
        prob_testing_clip_marginalized, prob_testing_clip_category, avg_NE_itr,\
        W_in, P, Tau = results

        plot_blocks = self.environment.plot_blocks
        plot_blocks_ID = self.environment.plot_blocks_ID

        show = []
        result = {}

        show.append(('training_df', 'table'))
        result['training_df'] = training_df

        show.append(('W_in' , 'heatmap'))
        result['W_in'] = W_in

        show.append(('P matrix' , 'heatmap'))
        result['P matrix'] = P

        show.append(('Tau matrix' , 'heatmap'))
        result['Tau matrix'] = Tau

        result_1 = prob_testing_clip.copy()
        show.append(('General Pairwise probability', 'heatmap'))
        result['General Pairwise probability'] = result_1

        result_2 = prob_testing_clip_marginalized
        show.append(('Within category probability', 'heatmap'))
        result['Within category probability'] = result_2

        result_3 = prob_testing_clip_category
        show.append(('Category-to-category probability', 'heatmap'))
        result['Category-to-category probability'] = result_3

        test_prob_dict = self.df_to_dict(prob_testing_clip_category)
        index = sorted(test_prob_dict.keys())
        agn_1 = [test_prob_dict[k] for k in index]
        result_4 = pd.DataFrame({'Connection Probabilities': agn_1}, index = index)

        show.append(('Relation results', 'bar'))
        result['Relation results'] = result_4

        if bool(plot_blocks): # returns True if the dict is not empty
            for k_ , v_ in plot_blocks.items():
                agn_prob = self.agent_results_avg(v_, test_prob_dict)
                index = sorted(plot_blocks[k_].keys())
                index = plot_blocks_ID[k_]
                agn_2 = [agn_prob[k] for k in index]
                print(agn_2)
                print(index)
                result_ = pd.DataFrame({'Connection Probabilities': agn_2},
                                        index = index)
                show.append((k_, 'bar'))
                result[k_] = result_

        return show, result
    
    # def plot_and_save_graph(self, n):

    #     """Used for creating animation"""

    #     self.figure.clf()
    #     self.figure.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)

    #     clip_space = self.artists[n]
    #     phase = self.current_phase[n]
    #     print("Creating Frame " + str(n))

    #     counter_condition_relations = [('A1','B2'),('A2','B3'),
    #                                    ('A3','B4'),('A4','B1')]

    #     if phase == "Phase 6":
    #         counterconditioning = True
    #     else:
    #         counterconditioning = False 

    #     subsets = dict()
    #     community_dict = {}
    #     color_map = {}
    #     alt_color_map = []
    #     for stimuli in clip_space:
    #         community_dict[stimuli] = int(stimuli[1]) - 1
    #         color_map[stimuli] = (list(mcolors.TABLEAU_COLORS.keys())[int(stimuli[1]) + 3])
    #         subsets[stimuli] = stimuli[0]
    #     subsets = {k: subsets[k] for k in list(sorted(subsets.keys()))}

    #     community_dict = self.obtain_communities(clip_space)

    #     for item in subsets.items():
    #         alt_color_map.append(list(mcolors.TABLEAU_COLORS.keys())[int(item[0][1]) + 3])
        
    #     nx.set_node_attributes(clip_space, subsets, name="layers")

    #     weight_labels = nx.get_edge_attributes(clip_space, 'weight')

    #     weights = np.array([weight for weight in weight_labels.values()])
    #     normalized_weights = {key: ((weight_labels[key] - np.min(weights)) / (np.max(weights) - np.min(weights))) for key in weight_labels.keys()}
        
    #     ordered_clip_space = nx.DiGraph()
    #     ordered_clip_space.to_directed()
    #     ordered_clip_space.add_nodes_from(sorted(clip_space.nodes(data=True)))
    #     ordered_clip_space.add_weighted_edges_from(clip_space.edges(data=True))

    #     pos = self.community_layout(clip_space, community_dict)

    #     edges = []

    #     nodes = nx.draw_networkx_nodes(clip_space, pos, node_size=500, node_color=alt_color_map)
    #     labels = nx.draw_networkx_labels(clip_space, pos, font_color='white')

    #     self.edge_artist = []
    #     weight_counter = 0
    #     for key, weight in normalized_weights.items():
    #         if counterconditioning and key in counter_condition_relations:
    #                 edges.append(nx.draw_networkx_edges(clip_space,
    #                                     pos,
    #                                     connectionstyle='arc3,rad=0.1',
    #                                     edgelist=[key],
    #                                     arrows=True,
    #                                     edge_color="tab:red",
    #                                     width= 2 + (weight * 6),
    #                                     alpha=max(0.33, weight))) #+ (weights[weight_counter] / 8),
    #                                     #alpha=weight)
    #         else:
    #             edges.append(nx.draw_networkx_edges(clip_space,
    #                                     pos,
    #                                     connectionstyle='arc3,rad=0.1',
    #                                     edgelist=[key],
    #                                     arrows=True,
    #                                     #edge_color=edge_color_map(weight),
    #                                     width= 2 + (weight * 6),
    #                                     alpha=max(0.1, weight))) #+ (weights[weight_counter] / 8),
    #                                     #alpha=weight)
    #         weight_counter += 1

    #     self.ax.set_xlim(self.x_min - self.pad_x, self.x_max + self.pad_x)
    #     self.ax.set_ylim(self.y_min - self.pad_y, self.y_max + self.pad_y)
    #     self.ax.set_aspect("equal")

    #     self.figure.text(0.1,
    #                      0.1,
    #                      phase,
    #                      fontsize=12)

    #     # self.ax.annotate("Test", xy=(1, 0), xycoords='axes fraction', fontsize=16,
    #     #         horizontalalignment='right', verticalalignment='bottom')

    #     # plt.xlim(self.x_min - self.pad_x, self.x_max + self.pad_x)
    #     # plt.ylim(self.y_min - self.pad_y, self.y_max + self.pad_y)

    #     #self.main_display.setFixedSize(self.main_display.grid.sizeHint())
    #     #print(self.ax.containers)
    #     return nodes, edges, labels
    
    # def obtain_communities(self, clip_space: nx.DiGraph):

    #     """
    #     Uses greedy modularity function
    #     """

    #     undirected_clip_space = clip_space.to_undirected()

    #     for stimuli in clip_space:
    #         for linked_stim in nx.neighbors(clip_space, stimuli):
    #             if stimuli in nx.neighbors(clip_space, linked_stim):
    #                 undirected_clip_space.edges[stimuli, linked_stim]["weight"] = (
    #                     clip_space.edges[stimuli, linked_stim]['weight'] + clip_space.edges[linked_stim, stimuli]['weight']
    #                 )

    #     undirected_communities = nx.community.greedy_modularity_communities(
    #         undirected_clip_space, "weight", 1, 1, self.environment.num_classes
    #     )

    #     # undirected_communities = nx.community.asyn_lpa_communities(
    #     #     undirected_clip_space, "weight", 1
    #     # )

    #     #print(undirected_communities)

    #     community_dict = {}
    #     for i, community in enumerate(undirected_communities):
    #         for stimuli in list(community):
    #             community_dict[stimuli] = i

    #     return community_dict
            

    # def community_layout(self, g, partition):
    #     """
    #     Compute the layout for a modular graph.


    #     Arguments:
    #     ----------
    #     g -- networkx.Graph or networkx.DiGraph instance
    #         graph to plot

    #     partition -- dict mapping int node -> int community
    #         graph partitions


    #     Returns:
    #     --------
    #     pos -- dict mapping int node -> (float x, float y)
    #         node positions

    #     """

    #     pos_communities = self._position_communities(g, partition, scale=3.)

    #     pos_nodes = self._position_nodes(g, partition, scale=1.)

    #     # combine positions
    #     pos = dict()
    #     for node in g.nodes():
    #         pos[node] = pos_communities[node] + pos_nodes[node]

    #     return pos

    # def _position_communities(self, g, partition, **kwargs):

    #     # create a weighted graph, in which each node corresponds to a community,
    #     # and each edge weight to the number of edges between communities
    #     between_community_edges = self._find_between_community_edges(g, partition)

    #     communities = set(partition.values())
    #     hypergraph = nx.DiGraph()
    #     hypergraph.add_nodes_from(communities)
    #     for (ci, cj), edges in between_community_edges.items():
    #         hypergraph.add_edge(ci, cj, weight=len(edges))

    #     # find layout for communities
    #     pos_communities = nx.spring_layout(hypergraph, **kwargs, center=[0,0], seed=1)

    #     # set node positions to position of community
    #     pos = dict()
    #     for node, community in partition.items():
    #         pos[node] = pos_communities[community]

    #     return pos

    # def _find_between_community_edges(self, g, partition):

    #     edges = dict()

    #     for (ni, nj) in g.edges():
    #         ci = partition[ni]
    #         cj = partition[nj]

    #         if ci != cj:
    #             try:
    #                 edges[(ci, cj)] += [(ni, nj)]
    #             except KeyError:
    #                 edges[(ci, cj)] = [(ni, nj)]

    #     return edges

    # def _position_nodes(self, g, partition, **kwargs):
    #     """
    #     Positions nodes within communities.
    #     """

    #     communities = dict()
    #     for node, community in partition.items():
    #         try:
    #             communities[community] += [node]
    #         except KeyError:
    #             communities[community] = [node]

    #     pos = dict()
    #     for ci, nodes in communities.items():
    #         subgraph = g.subgraph(nodes)
    #         pos_subgraph = nx.spring_layout(subgraph, **kwargs, seed=1)
    #         pos.update(pos_subgraph)

    #     return pos

#    def save_latex(self, results):
#
#        training_df, prob_training_clip, prob_testing_clip, \
#        prob_testing_clip_marginalized, prob_testing_clip_category, avg_NE_itr,\
#        W_in, P, Tau = results
#
#        tf = open('latex_'+ self.file_name[:-1]+'txt', 'w')
#        tf.write(training_df.to_latex())
#
#        agent_ini = pd.DataFrame()
#        environment_ini = pd.DataFrame()
#        for k,v in self.agent_parameter.items():
#            if k == 'agent_type':
#                agent_ini[k] = [v]
#            else:
#                agent_ini[k] = [v[0]]
#        for k, v in self.environment_parameter.items():
#            environment_ini[k] = [v[0]]
#
#        tf.write(agent_ini.to_latex())
#        tf.write(environment_ini.to_latex())
#        tf.close()


class Plot_results(object):

    """
    This class plot the results which has been stored in 'file name' location.
    """

    def __init__(self, file_name):

        self.file_name=file_name

    def showResults(self, plots):

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
                self.barDiagramShow(name, result, plots[i])    # result is a dataframe
            elif showType == 'heatmap':
                self.heatmapShow(name, result, plots[i])       # result is a dataframe


    def barDiagramShow(self, name, data, plot):

        """ bar plot"""

        data.plot(kind = 'bar', color = ['royalblue','lightgreen', 'red','cyan'], ax=plot)
        plt.legend(fontsize = 20)
        plt.tick_params(labelsize = 20)
        plt.title(name, fontsize = 20)
        plt.ylabel('Correct match ratio', fontsize = 20)
        plt.tight_layout()
        plt.xticks( rotation=45, fontsize = 18, horizontalalignment = 'right')
        plt.show()


    def heatmapShow(self, name, data, plot):

        """ heatmap plot"""

        fig, ax = plt.subplots()
      #  sns.set(font_scale = 1.5)
        sns.heatmap(data.round(3),xticklabels=True, yticklabels=True, annot = True,
                    annot_kws = {"size": 14}, linewidths =.15, fmt="g", cmap="Blues", ax=plot) # cmap="Greens"

        plt.title(name, fontsize = 16)
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
        for k, v in agent_parameter.items():
            if k == 'agent_type':
                agent_ini[k] = [v]
            else:
                agent_ini[k] = [v[0]]
        for k, v in environment_parameter.items():
            environment_ini[k] = [v[0]]

        print("---*Agent Setting*---", agent_ini, sep = '\n')
        print("\n---*Environment Setting*---", environment_ini, sep = '\n')