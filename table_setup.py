# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout

from network_visualizer import NetworkVisualizer
from rdt_visualizer import RDTVisualizer

class TableDisplay(QtWidgets.QWidget):

    def __init__(self, parent, simulator):
        #super(QWidget, self).__init__(parent)
        QtWidgets.QWidget.__init__(self)
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.network_tab = NetworkVisualizer(self, simulator)
        #self.rdt_tab = RDTVisualizer()

        self.tabs.addTab(self.network_tab, "Network Visualization")
        #self.tabs.addTab(self.rdt_tab, "RDT Visualization")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)




