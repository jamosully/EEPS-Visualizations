from PySide6 import QtCore, QtWidgets 
from PySide6.QtWidgets import (QTabWidget, QTableWidget, QTableWidgetItem, 
                               QLabel, QDoubleSpinBox, QSizePolicy, 
                               QHeaderView, QVBoxLayout)
from PySide6.QtGui import QFont, QColor

class ExperimentInformation(QtWidgets.QWidget):

    def __init__(self, main, simulator):

        self.main = main
        self.sim = simulator

        self.infoLayout = QVBoxLayout()

    def createInfoTable(self):

        # What should be included:
        # - current training block
        # - current performance
        
        self.table = QTableWidget(0, 3)