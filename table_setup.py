# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout

from network_visualizer import NetworkVisualizer
from rdt_visualizer import RDTVisualizer
from results_display import ResultsWindow

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

        self.tabs.addTab(self.network_tab, "Network Visualization")
        self.tabs.addTab(self.rdt_tab, "RDT Visualization")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.assembleGraphDicts()

    def add_results(self, simulator):

        self.results_tab = ResultsWindow(self, simulator)
        self.tabs.addTab(self.results_tab, "Results")

    def delete_results(self):

        self.tabs.removeTab(self.results_tab)
        self.results_tab.deleteLater()

    def assembleGraphDicts(self):

        self.visualizer_canvas_dict = {}
        self.visualizer_figure_dict = {}
        for visualizer in self.visualizers:
            self.visualizer_canvas_dict[visualizer.name] = visualizer.canvas
            self.visualizer_figure_dict[visualizer.name] = visualizer.figure
