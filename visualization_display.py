# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QHBoxLayout
import pandas as pd
import numpy as np

from network_visualizer import NetworkVisualizer
from rdt_visualizer import RDTVisualizer
from heatmap_visualizer import HeatmapVisualizer
from results_display import ResultsDisplay
from stimuli_editor import StimuliEditor

"""
visualization_display.py

Provides tab display which holds each visualisation
as well as results

Also handles communication with stimuli editor
"""

class VisualizationDisplay(QtWidgets.QWidget):

    """
    Tab display for visualisations and results    
    """

    update_editor = Signal()

    def __init__(self, parent, simulator, simulator_thread, 
                 simulator_mutex, env_params, gui_params, rdt_volume_types, 
                 rdt_density_types, parameter_toolbox, threadpool):
        QtWidgets.QWidget.__init__(self)
        self.layout = QHBoxLayout(self)
        self.simulator = simulator
        self.simulator_thread = simulator_thread
        self.main = parent
        self.visualizers = []

        self.stimEditor = None
        self.edited_clip_space = None
        self.edits_made = False
        self.step_changed = False

        self.resultsTab = None

        self.threadpool = threadpool

        self.tabs = QTabWidget()
        self.networkTab = NetworkVisualizer(self.main, self, simulator, gui_params)
        parameter_toolbox.add_network_visualizer(self.networkTab)
        parameter_toolbox.add_display(self)

        self.visualizers.append(self.networkTab)
        self.rdtTab = RDTVisualizer(self, simulator, env_params, rdt_volume_types, rdt_density_types)
        self.visualizers.append(self.rdtTab)
        self.heatmapTab = HeatmapVisualizer(self, simulator)
        self.visualizers.append(self.heatmapTab)

        self.tabs.addTab(self.networkTab, "Network")
        self.tabs.addTab(self.heatmapTab, "Heatmap")
        self.tabs.addTab(self.rdtTab, "RDT")

        self.simulator.sim_complete.connect(self.add_results)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def add_results(self):

        self.simulator_thread.quit()
        if self.simulator.prev_file:
            self.resultsTab = ResultsDisplay(self.main, self.simulator, self.rdtTab.rdt_volume, self.rdtTab.rdt_density, self.simulator.file_name)
        else:
            self.resultsTab = ResultsDisplay(self.main, self.simulator, self.rdtTab.rdt_volume, self.rdtTab.rdt_density, None)
        self.tabs.addTab(self.resultsTab, "Results")

        #self.stimEditor.hide()
        
        if self.networkTab.vis_settings["create_animation"][0] != "Don't Save":
            self.networkTab.generate_animation("test",
                                               ["A1"],
                                               0.5,
                                               40,
                                               self.threadpool)

    def delete_results(self):

        if self.resultsTab is not None:
            self.tabs.removeTab(self.resultsTab)
            self.resultsTab.deleteLater()
            self.resultsTab = None

    def assignControlPanel(self, controlPanel):

        self.controlPanel = controlPanel

    def assignStimEditor(self, stimEditor):

        self.stimEditor = stimEditor

    def populateEditor(self, stimuli, clip_space):

        if self.edited_clip_space is not None:
            print("edited!")
            self.stimEditor.populateEditor(stimuli, self.edited_clip_space)
        else:
            self.stimEditor.populateEditor(stimuli, clip_space)

    def updateEditor(self):
     
        self.stimEditor.updateEditor()

    def hideEditor(self, value):

        if value[0] == True:
            self.stimEditor.hide()
        elif value[0] == False:
            self.stimEditor.show()

    def update_clip_space(self):

        self.edits_made = False
        self.new_cs = self.edited_clip_space
        self.edited_clip_space = None
        return self.new_cs
    
    def update_step_count(self):

        self.step_changed = False
        return self.controlPanel.step_count
    
    def change_step_counter(self, current_step):

        self.controlPanel.change_step_counter(current_step)

