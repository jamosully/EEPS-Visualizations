# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QHBoxLayout

from network_visualizer import NetworkVisualizer
from rdt_visualizer import RDTVisualizer
from heatmap_visualizer import HeatmapVisualizer
from results_display import ResultsDisplay
from stimuli_editor import StimuliEditor

class VisualizationDisplay(QtWidgets.QWidget):

    def __init__(self, parent, simulator):
        #super(QWidget, self).__init__(parent)
        QtWidgets.QWidget.__init__(self)
        self.layout = QHBoxLayout(self)
        self.simulator = simulator
        self.main_display = parent
        self.visualizers = []

        self.stim_editor = None
        self.results_tab = None

        self.tabs = QTabWidget()
        self.network_tab = NetworkVisualizer(self.main_display, self, simulator)
        self.visualizers.append(self.network_tab)
        self.rdt_tab = RDTVisualizer(self, simulator)
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

        print("adding results")
        self.results_tab = ResultsDisplay(self.main_display, self.simulator)
        self.tabs.addTab(self.results_tab, "Results")
        self.main_display.setFixedSize(self.main_display.grid.sizeHint())

    def delete_results(self):

        if self.results_tab is not None:
            self.tabs.removeTab(self.results_tab)
            self.results_tab.deleteLater()
            self.results_tab = None

    Slot()
    def createStimuliEditor(self, stimuli, clip_space):
        
        self.stim_editor = StimuliEditor(self.main_display, self.simulator, stimuli, clip_space)
        self.layout.addWidget(self.stim_editor)

    def deleteStimuliEditor(self):

        if self.stim_editor is not None:
            self.layout.removeWidget(self.stim_editor)
            self.stim_editor.deleteLater()
            self.stim_editor = None

