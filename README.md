# Affinity: an visualisation tool for Enhanced Equivalence Projective Simulation

The original README can be found here: [EEPS](https://github.com/Asieh-A-Mofrad/Enhanced-Equivalence-Projective-Simulation)

## Motivation and Project Objectives

This project was created as part of a summer project on the foundation year of the Interactive Artificial Intelligence CDT at the University of Bristol. Originally intended as an early foray into computational modelling in Contextual Behavioural Science, the project grew to focus on incorporating Relational Density Theory (RDT) into a pre-exisiting model of Stimulus Equivalence. With this in mind, the key objectives of this prototype are:

1. Create a tool for visualising the the behavior of agent behavior during the training and testing stages of EEPS
2. Explore the inclusion of RDT in EEPS
3. Investigate the effects of Network Enhancement on the agent's clip space
4. Provide the potential foundations of visualising future PS models

## Installation

To run Affinity, it is reccomended that you utilise a custom environment via conda. Once done, install the required packages via

```lang-bash
pip install -r requirements.txt
```

### Common Issues

TODO: Add common issues

## Walkthrough

This section will provide the step-by-step process for recreating the experiments included in the corresponding paper on Affinity.

1. Install Affinity
2. Launch Affinity by running the `main.py` script
3. Set these agent parameters to the following:
   - $\beta_h$ / `beta_h` = 0.1
   - $\beta_t$ / `beta_t` = 4.0
   - $K$ = 1.0
   - $\gamma$ / `gamma_damping` = 0.001
   - $\alpha$ / `alpha` = 0.7
   - `NE_during_training` = :white_square_button: or :white_check_mark:
4. Set these environment parameters to the following:
   - `environment_ID` = 15
   - `max_trial` = 10000
   - `num_agents` = 15
   - `size_action_set` = 4
   - `autogenerate_classes` = :white_check_mark:
5. Click `Create Simulation`
6. Click `Initialize Parameters`
7. Click `Run Simulation`

Once running, the pace of the experiment can be controlled with the step slider and proceed button. Good luck!

## Structure of Affinity

![affinity_structure](Images/software_structure_diagram.png)

## Interface Design

![main_interface](Images/affinity_gui.png)

Affinity's interface is made up of four components:

1. Parameter Toolbox
2. Visualisation Display
3. Control Panel
4. Relation Editor

These components act as the frontend of the software. `main.py` acts as a intermediary between the GUI of Affinity and the backend, which is handled by `simulator.py`. `visualization_display.py` is a container for Affinity's visualisations and results.

### Parameter Toolbox

![parameter_toolbox](Images/parameter_toolbox.png)

The Parameter toolbox is where user can modify agent and environment parameters and load results from previous experiments. Definitions are provided for each parameter, and Affinity utilises a JSON file for saving a deafult set of parameters that are shown each time the software is launched.

### Visualisation Display

The visulisation display is the main components of Affinity, which is comprised of a tab-based interface containing each of the three visualisations, and the results upon the completion of an experiment.

#### Network Visualisation

![network_visualisation](Images/network_visualization.png)

The **Network** tab on the main display contains visualisations of the agents clip space as a graph network. These visualisations are inspired by figures provided in the original EEPS paper, and provide a dynamic

#### Heatmap Visualisation

![heatmap_visualisation](Images/heatmap_visualization.png)

In the **Heatmap** tab, an alternative view of the agent's clip space is provided. This interface is cleaner and less cluttered than the graph network visualisation.

#### Realtional Density Theory Visualisations

![rdt_visualisation](Images/rdt_visualization.png)

Under the **RDT** tab, Affinity provides novel visualisations of metrics provided as part of Belisle and Dixon's Relational Density Theory.

On the top right of the display are two dropdown menus which allow the user to switch between various measures of relational volume and relational mass. Switching between the different measures updates the relational mass figure at the bottom.

##### Relational Volume

|Measure                 |Description|Rationale|
|:-----------------------|:----------|:--------|
|True Nodal Distance     |Total nodal distance between stimuli in a class, where each distance is obtained via the shortest nodal distance between stimuli (including symmetry, transitivity, and equivalence relations)|The transparent memory of agents in EEPS affords this form of nodal distance, which is more susceptible to fluctuations from differences in training structure and Network Enhancement|
|Empirical Nodal Distance|Based on Fields [^fields1984], total nodal distance in a class, where a stimuli is counted as part of the class if it has two trained relations|Utilised by Cotter and Stewart in their study of RDT [^cotter2023], implemented here to allow for comparrisons between the study/further experiments and the simulation|
|Class Size              |Total number of stimuli in each class|Defined as a measure of relational volume in Belisle and Dixon's first paper on RDT [^belisle2020]|
|Number of Relations     |Total number of relations between stimuli in a class (including symmetry, transitivity, and equivalence relations)|Defined as a measure of relational volume in Belisle and Dixon's first paper on RDT [^belisle2020]|

##### Relational Density

|Measure                            |Description|Rationale|
|:----------------------------------|:----------|:--------|
|Mean softmax transition probability|||
|Class Accuracy                     |||
|Mean edge weight/h-value           |||

### Stimuli Editor

### Experiment Designer

### Changes to EEPS

To achieve the aims of this project, several changes were made to the original EEPS code. These are outlined below

#### Visualisation Support

#### Network Enhancement During Training

## Future Work

- [ ] Drag and drop tabs
- [ ] Modifying connections via the heatmap visualisation
- [ ] Integrating the netgraph multi-graph layout
- [ ] An interface for creating new experiments
- [ ] A system for integrating other EEPS/EPS/PS variants within the visualisation framework of Affinity
- [ ] Various keyboard shortcuts
- [ ] Counterconditioning
  
## References

[^fields1984]: Fields, L., Verhave, T. and Fath, S., 1984. Stimulus equivalence and transitive associations: A methodological analysis. Journal of the Experimental Analysis of behavior, 42(1), pp.143-157.

[^cotter2023]: Cotter, Eoin, and Ian Stewart. "The role of volume in relational density theory: Isolating the effects of class size and nodal distance on density and resistance in equivalence classes." The Psychological Record 73.3 (2023): 375-393.

[^belisle2020]: Belisle, J. and Dixon, M.R., 2020. Relational density theory: Nonlinearity of equivalence relating examined through higher-order volumetric-mass-density. Perspectives on Behavior Science, 43(2), pp.259-283.
