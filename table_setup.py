# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout

from network_visualizer import NetworkVisualizer
from rdt_visualizer import RDTVisualizer
from heatmap_visualizer import HeatmapVisualizer
from results_display import ResultsDisplay

class TableDisplay(QtWidgets.QWidget):

    def __init__(self, parent, simulator):
        #super(QWidget, self).__init__(parent)
        QtWidgets.QWidget.__init__(self)
        self.layout = QVBoxLayout(self)
        self.simulator = simulator
        self.visualizers = []

        self.tabs = QTabWidget()
        self.network_tab = NetworkVisualizer(self, simulator)
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
        self.results_tab = ResultsDisplay(self.simulator)
        self.tabs.addTab(self.results_tab, "Results")

    def delete_results(self):

        self.tabs.removeTab(self.results_tab)
        self.results_tab.deleteLater()

