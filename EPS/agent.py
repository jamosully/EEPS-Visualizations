# -*- coding: utf-8 -*-
"""
Last update: Dec. 26, 2019

@author: Asieh Abolpour Mofrad

This code is used for simulation results reported in an article entitled:

"Equivalence Projective Simulation as a Framework for Modeling Formation of 
Stimulus Equivalence Classes" in Neurol Computation Journal

"""

import numpy as np
import networkx as nx
import pandas as pd
import math

class Agent(object):

    """
    This class contains various Equivalence Projective Simulation agents.
    The agents are basically different in computation of derived relations.
    The chosen agent is initialized based on the given dictionry of parameters p.

    Agent_basic class: The basis for all other agents, without formation of
    derived relations derived relation.

    Agent_positive class: The case with which derived relations are calculated
    with max-product algorithm

    Agent_negative class: The case that only 'softmax' computation is possible and
    h-values get any value, i.e. h_0 is not the lower bound for h-values.
    Derived relations is computed with max-product

    Agent_Viterbi class: The case that a trellis diagram used to fint the
    max-product probability

    Agent_absorbing class: The case that derived relations are computed based
    on a random walk, when action_set form the absorbing states.

    """

    def __init__(self, p):

        if p["agent_type"] == 'positive_h':
            self.agent = Agent_positive(
                    p["gamma_damping"][0], p["beta_softmax"][0],
                    p["category"][0], p["K1"][0], p["K2"][0], p["K3"][0],
                    p["K4"][0], p["policy_type"][0], p["gamma_nodal"][0],
                    p["memory_sharpness"][0], p["nodal_theta"][0])

        elif p["agent_type"] == 'negative_h':
            self.agent = Agent_negative(
                    p["gamma_damping"][0], p["beta_softmax"][0],
                    p["category"][0], p["K1"][0], p["K2"][0])

        elif p["agent_type"] == 'viterbi':
            self.agent = Agent_Viterbi(
                    p["gamma_damping"][0], p["beta_softmax"][0],
                    p["category"][0], p["K1"][0], p["K2"][0], p["K3"][0],
                    p["K4"][0], p["policy_type"][0], p["gamma_nodal"][0],
                    p["memory_sharpness"][0], p["nodal_theta"][0])

        elif p["agent_type"]=='absorbing':
            self.agent = Agent_absorbing(
                    p["gamma_damping"][0], p["beta_softmax"][0],
                    p["category"][0], p["K1"][0], p["K2"][0], p["K3"][0],
                    p["K4"][0], p["policy_type"][0])


class Agent_basic(object):

    """
    The basic Projective Simulation agent, other agents inheritance from 
    Agent_basic.

    """

    def __init__(self, gamma_damping, beta_softmax, category, K1, K2, K3, K4,
                                                                  policy_type):

        """
        Initialize the basic EPS agent. Arguments:

        - gamma_damping: float between 0 and 1, controls forgetting/damping
        of h-values

        - policy_type: string, 'standard' or 'softmax'; toggles the rule used
        to compute probabilities from h-values

        - beta_softmax: float >=0, probabilities are proportional to
        exp(beta*h_value). If policy_type != 'softmax', then this is irrelevant.

        - K1 > 0 is the parameter for direct reinforcement

        - 0 < K2 < K1 is the parameter for symmetric reinforcement

        0 < K3 <= K1/(size_action_set -1) is parameter for direct
        reinforcement when a wrong match is chosen

        - 0 < K4 <= K2/(size_action_set -1) is parameter for symmetric
        reinforcement when a wrong match is chosen
        """

        self.gamma_damping = gamma_damping

        self.beta_softmax = beta_softmax

        self.category=category

        self.K1 = K1

        self.K2 = K2

        self.K3 = K3

        self.K4 = K4

        self.policy_type = policy_type

        self.clip_space = nx.DiGraph()

        self.percept_set = set()

        self.action_set = set()

    def trial_preprocess(self, percept, action): 

        """
        Takes a percept and an action set, updates percept_set,
        action_set, and clip_space if required.
        """

        self.percept_set |= set([percept])

        for act in action:
            self.action_set |= set([act])

        for act in  action:
            if (percept, act) not in self.clip_space.edges():
                self.clip_space.add_edge(percept, act, weight = 1)
                self.clip_space.add_edge(act, percept, weight = 1)

    def action_selection(self, percept, action_set_t, clip = None): 

        """
        Given a percept and an action set, this method returns the next action

        Arguments:
            - percept: any immutable object (as specified for trial_preprocess),
            - action_set_t: a list of any immutable object (as specified for
                                                            trial_preprocess),
        Output: action
        """

        if clip is None:
            clip = self.clip_space.copy()

        probability_distr = self.probability_distribution_trial(
                                                  percept, action_set_t,clip)
        size_action_set = len(action_set_t)
        Action = np.random.choice(size_action_set, p = probability_distr)

        return action_set_t[Action]


    def probability_distribution_trial(self,percept, action_set_t, clip = None): 

        """
        Given a percept and an action set and a clip network, this method computes a
        probability distribution over action_set according to policy_type,
        The clip must have direct connections with h_values.

        Arguments:

            - percept: any immutable object (as specified for trial_preprocess),
            - action_set_t: a list of any immutable object (as specified
                                                            for trial_preprocess),
            - clip: is the network, defult is self.clip_space

        Output: probability distribution
        """

        if clip is None:
            clip = self.clip_space.copy()

        h_vector = [clip[percept][action]['weight']
        for action in action_set_t]

        if self.policy_type == 'standard':
            probability_distr = h_vector/ np.sum(h_vector)

        elif self.policy_type == 'softmax':
            probability_distr = self.softmax(h_vector)

        return probability_distr

    def training_update_network(self, percept, action_set_t, action, reward): 

        """
        Given a history of what happend, i.e. the percept, the action set,
        the chosen action by the agent
        and the reward, this method updates the clip_space,
        the method is for the case where h_valuse >= h_0 >=1.

        Arguments:

            - percept: any immutable object (as specified for trial_preprocess),
            - action_set_t: a list of any immutable object (as specified for
                                                            trial_preprocess),
            - action: what agent chose for the above percept and action_set_t
            - reward: 1 or -1
        """

        for u,v,d in self.clip_space.edges(data = True):
            d['weight'] = d['weight'] - self.gamma_damping * (d['weight']-1)
            # This is the forgetting factor that acts on all connections

        if reward == 1:
            self.clip_space[percept][action]['weight'] += self.K1
            self.clip_space[action][percept]['weight'] += self.K2

        elif reward == -1:
            for act in set(action_set_t) - set([action]):
                self.clip_space[percept][act]['weight'] += self.K3
                self.clip_space[act][percept]['weight'] += self.K4

    def softmax(self,h_vec): 

        """Compute softmax values for each sets of h-values in h_vec."""

        h = [i* self.beta_softmax for i in h_vec]
        e_h = np.exp(h - np.max(h))
        prob = e_h / np.sum(e_h)

        return prob

    def softmax_revers(self, prob): 

        """
        Compute h-values from a probability distribution vector. The h_vec is
        a positive vector with minimum value 1.
        """

        h = [i/ self.beta_softmax for i in np.log(prob)]
        h_vec = h - np.min(h)+1

        return h_vec

    def testing_action_selection(self, percept, action_set_t): 

        """Given a percept and an action set, this method computes a
        probability distribution over action_set according to policy_type,
        then returns the next action. If the relation between percept and
        action_set appears the first time and as a transivity, or equivalence
        relation, the shortwst path must be found.

        Arguments:

            - percept: any immutable object (as specified for trial_preprocess),
            - action_set: a set of any immutable object (as specified for
                                                         trial_preprocess),

        Output: action
        """

        for u,v,d in self.clip_space.edges(data = True):
            d['weight'] = d['weight'] - self.gamma_damping * (d['weight']-1)
            # This is the forgetting factor that acts on all connections

        edge_exists = True
        for action in action_set_t:
            if (percept,action) not in self.clip_space.edges():
                edge_exists = False

        if edge_exists:
            clip_temp = self.clip_space.copy()
        else:
            clip_temp = self.derived_connections(percept, action_set_t)

        return self.action_selection(percept, action_set_t,clip_temp)

    def derived_connections(self, percept, action_set_t, clip =  None): 

        """
        This method establish new connections randomely. This is the naive senario.
        It can be considered as an agent without ability to make equivalence
        relations.

        Output: A new clip_space
        """

        if clip is None:
            clip = self.clip_space

        clip_derived = clip.copy()
        for action in action_set_t:
            clip_derived.add_edge(percept, action, weight = 1)

        return clip_derived

    def h_value_to_probability(self, clip = None):

        """
        This method computes the transition probabilities from h-values.
        Output: the network clip with probabilities
        """

        if clip is None:
            clip = self.clip_space

        clip_prob = clip.copy()
        for node in clip_prob.nodes():
            OUT_Edges = clip_prob.out_edges(node, data = True)
            if len(OUT_Edges) != 0:
                H_vector = [edge[2]['weight'] for edge in OUT_Edges]

                if self.policy_type == 'standard':
                    for edge in OUT_Edges:
                        edge[2]['weight'] = edge[2]['weight'] / np.sum(H_vector)
                if self.policy_type == 'softmax':
                    pr_vector = self.softmax(H_vector)
                    i = 0
                    for edge in OUT_Edges:
                        edge[2]['weight'] = pr_vector[i]
                        i += 1
        return clip_prob

    def h_value_to_probability_category(self, clip = None):

        """
        This method computes the transition probabilities from h-values.
        This method computes marginal probabilities to each category.
        Output: the network clip with probabilities
        """

        if clip is None:
            clip = self.clip_space
        clip_prob = clip.copy()
        category = self.category_set(clip_prob)
        for node in clip_prob.nodes():
            for ctg in category:
                OUT_Edges = [edge for edge in
                           clip_prob.out_edges(node, data = True)
                                                          if edge[1][0] == ctg]
                if len(OUT_Edges) != 0:
                    H_vector = [edge[2]['weight'] for edge in OUT_Edges]

                    if self.policy_type == 'standard':
                        for edge in OUT_Edges:
                            edge[2]['weight'] = edge[2]['weight'] / np.sum(H_vector)
                    if self.policy_type == 'softmax':
                        pr_vector = self.softmax(H_vector)
                        i = 0
                        for edge in OUT_Edges:
                            edge[2]['weight'] = pr_vector[i]
                            i += 1
        return clip_prob

    def unified_h_value_to_pr(self, clip = None): 

        """ To choose either of scenarios based on the category value"""

        if clip is None:
            clip = self.clip_space
        if self.category == 'False':
            clip_prob = self.h_value_to_probability(clip)
        elif self.category == 'True':
            clip_prob = self.h_value_to_probability_category(clip)
        return clip_prob

    def Network_update(self, clip = None): 

        """
        This method computes all the possible direct connections and h-values
        """

        if clip is None:
            clip = self.clip_space

        new_clip_space = clip.copy()
        category = self.category_set(new_clip_space)
        for node in clip.nodes():
            category_node = category - set(node[0])
            for ctg in category_node:
                head=[v for v in new_clip_space.nodes() if v[0] == ctg[0]]
                if len(head)> 0:
                    no_edge = False
                    for action in head:
                        if (node,action) not in new_clip_space.edges():
                                no_edge = True
                    if no_edge:
                        new_clip = self.derived_connections(
                                node, head, clip)
                        new_clip_space.add_edges_from(new_clip.edges(data = True))

        return new_clip_space

    def category_set(self,clip):

        """ To find the set of categories from the clip space"""

        category = set()
        for node in clip.nodes():
            category |= set(node[0])
        return category


class Agent_positive(Agent_basic):

        """
        Projective Simulation agent for Equivalence Class formation.

        This is for the case that h-values are postitive.
        """

        def __init__(self,
                     gamma_damping, beta_softmax, category, K1, K2, K3, K4,
                     policy_type, gamma_nodal, memory_sharpness, nodal_theta):

                 super(Agent_positive, self).__init__(gamma_damping,
                      beta_softmax, category, K1, K2, K3, K4, policy_type)

                 self.gamma_nodal = gamma_nodal

                 self.memory_sharpness = memory_sharpness

                 self.nodal_theta = nodal_theta

        def derived_connections(self, percept, action_set_t, clip = None): 

            """
            This method establish new connections based on max-product using
            Dijekstra algorithm.
            This is to be used in testing phase when there is a path between
            percept and action_set_t members, but not a direct connection.

            The clip is a network that weights are h-values

            Output: A new clip_space
            """

            if clip is None:
                clip = self.clip_space

            clip_derived = clip.copy()
            clip_ = self.local_clip(percept, action_set_t, clip)
            clip_temp = self.probability_to_nlog(
                                             self.unified_h_value_to_pr(clip_))

            for action in action_set_t:
                sh_path = nx.dijkstra_path(clip_temp, percept, action,
                                                             weight = 'weight')

                cost_sum = self.path_weight(clip_temp, sh_path)
                clip_temp.add_edge(percept, action, weight = cost_sum)

            path = nx.shortest_path(clip_, percept, action)
            D_nodal=len(path)-2

            p_vector = [math.exp(-clip_temp[percept][action]['weight'])
                                                    for action in action_set_t]
            p_vector = p_vector/ np.sum(p_vector)
            p_vector = self.nodal_effect(D_nodal, p_vector)

            if self.policy_type == 'standard':
                h_vector = p_vector/ np.min(p_vector)
            elif self.policy_type == 'softmax':
                h_vector = self.softmax_revers(p_vector/ np.sum(p_vector)) 

            i = 0
            for action in action_set_t:
                clip_derived.add_edge(percept, action, weight = h_vector[i])
                i += 1

            return clip_derived

        def probability_to_nlog(self, clip_prob): 

            """
            This method gets a clip network with probabilities and return a clip
            network with -log values

            Output: A new clip_space
            """

            clip_nlog = clip_prob.copy()

            for u, v, d in clip_nlog.edges(data = True):
                d['weight'] =  -math.log(d['weight'])

            return clip_nlog

        def nodal_effect(self, D_nodal, p_vector): 

            """ 
            for the case that sharpness is adjusting. The three cases is
            considered
            self.nodal_theta == Not: is the case that theta does not change with
            nodal distance
            self.nodal_theta==Lin: is the case that theta changes linearly with
            nodal distance
            self.nodal_theta==Pow: is the case that theta changes with nodal distance
            in a power law format
            Just for Standard scenario.
            """

            p_vector_random = [1/len(p_vector)]* len(p_vector)
            if self.nodal_theta == "Not":
                theta = self.memory_sharpness
            elif self.nodal_theta == "Lin":
                theta = max(0, self.memory_sharpness - (D_nodal* self.gamma_nodal))
            elif self.nodal_theta == "Pow":
                theta = self.memory_sharpness* pow(D_nodal, -1* self.gamma_nodal)

            probability_distr = [p_vector[i]* theta+ p_vector_random[i]* (1-theta)
            for i in range(len(p_vector))]

            return probability_distr

        def path_weight(self, clip, path): 

            """
            This method gets a clip network with a path and return the weight of path

            Output: path weight
            """

            cost_sum = 0
            for i in range(len(path)-1):
                cost_sum += clip[path[i]][path[i+1]]['weight']

            return cost_sum

        def local_clip(self, percept, action_set, clip): 

            """ This is for the case that a part of clip network is to be used
            It is just passing the clip for now
            """

            return clip.copy()

#------------------------------------------------------------------------------
class Agent_negative(Agent_positive):

        """
        Projective Simulation agent for Equivalence Class formation.

        This is for the case that h-values are negative, i.e. Positive_h = False
        """

        def __init__(self,
                     gamma_damping, beta_softmax, category, K1, K2, K3 = 1, 
                     K4 = 1, policy_type = 'softmax', gamma_nodal = 0,
                 memory_sharpness = 1, nodal_theta = "Not"):

                 super(Agent_negative, self).__init__(
                         gamma_damping, beta_softmax, category, K1, K2, K3, K4,
                         policy_type, gamma_nodal, memory_sharpness, nodal_theta)

        def training_update_network(self, percept, action_set_t, action, reward): 

            """
            Given a history of what happend, i.e. the percept, the action set,
            the chosen action by the agent
            and the reward, this method updates the clip_space,
            the method is for the case where h_valuse could get negative values
            and can be used in the cases where policy_type = 'softmax'

            Arguments:

                - percept: any immutable object (as specified for trial_preprocess),
                - action_set_t: a list of any immutable object (as specified for
                                                                trial_preprocess),
                - action: what agent chose for the above percept and action_set_t
                - reward: 1 or -1
            """

            for u,v,d in self.clip_space.edges(data = True):
                d['weight'] = (1- self.gamma_damping) *d['weight']
                # This is the forgetting factor that acts on all connections

            self.clip_space[percept][action]['weight'] += (self.K1 * reward)
            self.clip_space[action][percept]['weight'] += (self.K2 * reward)

#------------------------------------------------------------------------------
class Agent_Viterbi(Agent_positive):

        """
        Projective Simulation agent for Formation of Stimulus Equivalence Classes.

        This is for the case that  a trellis diagram used to fint the 
        max-product probability

        """

        def __init__(self,
                     gamma_damping, beta_softmax, category, K1, K2, K3, K4,
                     policy_type, gamma_nodal, memory_sharpness, nodal_theta):

                 super(Agent_Viterbi, self).__init__(
                         gamma_damping, beta_softmax, category, K1, K2, K3, K4,
                         policy_type, gamma_nodal, memory_sharpness, nodal_theta)

        def local_clip(self,percept,action_set,clip): 

            """
            Remove extra connections and path the connections in the trellis diagram
            """

            path = nx.shortest_path(clip, source = percept, target = action_set[0])
            path_ = [i[0] for i in path]

            elist = [(u,v,d) for u,v,d in clip.edges(data = True) if (u[0] in
                   path_ and v[0] in path_ and path_.index(u[0]) < path_.index(v[0]))]
            trellis_clip = nx.DiGraph()
            trellis_clip.add_edges_from(elist)

            return trellis_clip

class Agent_absorbing(Agent_basic):

        """
        Projective Simulation agent for Formation of Stimulus Equivalence Classes.

        Features: this is for the case that probabilities in the test phase
        is calculated based on the assumption that action clips are
        Markov absorbing states.
        """

        def __init__(self,
                     gamma_damping, beta_softmax, category, K1, K2, K3, K4,
                                                                  policy_type):
                 super(Agent_absorbing, self).__init__(
                         gamma_damping, beta_softmax, category, K1, K2, K3, K4,
                                                                   policy_type)

                 self.expected_steps = pd.Series()
                 self.expected_steps_aux = pd.Series()

        def derived_connections(self, percept, action_set_t, clip = None):

            """
            This method establish new connections based on absorbing state MC.
            This is to be used in testing phase when there is a path between
            percept and action_set_t members, but not a direct connection.

            Output: A new clip_space
            """

            if clip is None:
                clip = self.clip_space

            clip_derived = clip.copy()
            M = self.absorbing_probabilities(action_set_t, clip)
            p_vector = M.loc[percept,:]

            if self.policy_type == 'standard':
                h_vector = p_vector/ np.min(p_vector)
            elif self.policy_type == 'softmax':
                h_vector = self.softmax_revers(p_vector/ np.sum(p_vector))

            i = 0
            for action in action_set_t:
                clip_derived.add_edge(percept, action, weight = h_vector[i])
                i += 1

            return clip_derived

        def absorbing_probabilities(self, action_set, clip = None): #Ok

                """
                This method is supposed to compute the absorbing probabilities
                for the action set when there is no direct connections.
                action_set: is a list of clips all from the same ctegory
                say ['C1','C3','C2']
                """

                if clip is None:
                    clip = self.clip_space

                clip_absorbing = clip.copy()
                ebunch = [edge for edge in clip_absorbing.out_edges(
                                                      action_set, data = True)]
                clip_absorbing.remove_edges_from(ebunch)
                for act in action_set:
                    clip_absorbing.add_edge(act, act, weight = 1)

                Q_list = [node for node in clip_absorbing.nodes() if node
                                                             not in action_set]
                Tr_nodelist = Q_list+ action_set
                # make the canonical form of transition matrix
                df_tr_matrix = nx.to_pandas_adjacency(clip_absorbing,
                                                        nodelist = Tr_nodelist)
                if self.policy_type == 'standard':
                    df_tr_matrix['sum']= df_tr_matrix.sum(axis = 1)
                    Tr_matrix = df_tr_matrix.div(df_tr_matrix['sum'], axis = 0)
                    Tr_matrix = Tr_matrix.drop(['sum'],axis = 1)
                if self.policy_type == 'softmax':
                    Tr_matrix = self.softmax_matrix(df_tr_matrix)

                Q = Tr_matrix.loc[Q_list, Q_list]
                R = Tr_matrix.loc[Q_list, action_set]

                I = Q.copy()
                I[:] = 0
                for i in Q_list:
                    I[i][i] = 1
                I_Q = I - Q
                N = pd.DataFrame(np.linalg.pinv(I_Q.values), I_Q.columns,
                                                                     I_Q.index)
                one_vec = pd.Series([1]* len(Q_list),Q_list)
                exp_steps = N.dot(one_vec)

                category = self.category_set(clip)
                if self.expected_steps.empty:
                    cat_list = [cat1+cat2 for cat1 in category for cat2 in
                                                      category if cat1 != cat2]
                    cat_list.sort()
                    self.expected_steps = pd.Series([0.0]*len(cat_list), cat_list)
                    self.expected_steps_aux = pd.Series([0.0]*len(cat_list), cat_list)

                catg = action_set[0][0]
                category_ = category - set(catg)
                for cat in category_ :
                    self.expected_steps.at[cat+catg] += np.average([v for k, v in
                                          exp_steps.items() if k[0] == cat])
                    self.expected_steps_aux.at[cat+catg] += 1

                M = N.dot(R)

                return M

        def softmax_matrix(self, Tr_matrix):

            """Compute softmax values for each row of the matrix."""

            prob_matrix = Tr_matrix.copy()
            for i in Tr_matrix.index:
                h = self.beta_softmax* Tr_matrix.loc[i,:]
                e_h = np.exp(h - np.max(h))
                for j in range(len(h)):
                    if h[j] == 0:
                        e_h[j] = 0
                prob_matrix.loc[i,:]=e_h/ np.sum(e_h)

            return prob_matrix

        def expected_steps_avg(self):

            """
            This is to compute the expected steps to reach an action based on
            the data collected in the test phase
            """

            exp_steps_avg = self.expected_steps.divide(self.expected_steps_aux)

            return exp_steps_avg
