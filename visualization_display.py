# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QHBoxLayout

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

    def __init__(self, parent, simulator, simulator_thread, simulator_mutex, env_params):
        QtWidgets.QWidget.__init__(self)
        self.layout = QHBoxLayout(self)
        self.simulator = simulator
        self.simulator_thread = simulator_thread
        self.main = parent
        self.visualizers = []

        self.stim_editor = None
        self.edited_clip_space = None
        self.edits_made = False
        self.step_changed = False

        self.results_tab = None

        self.tabs = QTabWidget()
        self.network_tab = NetworkVisualizer(self.main, self, simulator)
        self.visualizers.append(self.network_tab)
        self.rdt_tab = RDTVisualizer(self, simulator, env_params)
        self.visualizers.append(self.rdt_tab)
        self.heatmap_tab = HeatmapVisualizer(self, simulator)
        self.visualizers.append(self.heatmap_tab)

        self.tabs.addTab(self.network_tab, "Network")
        self.tabs.addTab(self.heatmap_tab, "Heatmap")
        self.tabs.addTab(self.rdt_tab, "RDT")

        self.simulator.sim_complete.connect(self.add_results)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def add_results(self):

        self.simulator_thread.quit()
        self.results_tab = ResultsDisplay(self.main, self.simulator, self.rdt_tab.rdt_volume, self.rdt_tab.rdt_density)
        self.tabs.addTab(self.results_tab, "Results")
        #self.main.setFixedSize(self.main.grid.sizeHint())

    def delete_results(self):

        if self.results_tab is not None:
            self.tabs.removeTab(self.results_tab)
            self.results_tab.deleteLater()
            self.results_tab = None

    def assign_control_panel(self, control_panel):

        self.control_panel = control_panel

    def assign_stim_editor(self, stim_editor):

        self.stim_editor = stim_editor

    def populateEditor(self, stimuli, clip_space):

        self.stim_editor.populateEditor(stimuli, clip_space)

    def updateEditor(self):

        self.stim_editor.updateEditor()

    def update_clip_space(self):

        self.edits_made = False
        self.new_cs = self.edited_clip_space
        self.edited_clip_space = None
        return self.new_cs
    
    def update_step_count(self):

        self.step_changed = False
        return self.control_panel.step_count

