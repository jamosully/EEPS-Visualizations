from PySide6 import QtCore, QtWidgets 
from PySide6.QtWidgets import (QVBoxLayout, QTableWidget, QComboBox, 
                               QLabel, QGroupBox, QSizePolicy, 
                               QHeaderView, QPushButton, QHBoxLayout, 
                               QCheckBox, QDoubleSpinBox, QSpinBox,
                               QTextEdit, QSpacerItem, QFileDialog)

class StimuliEditor(QtWidgets.QWidget):

    def __init__(self, parent, simulator):

        self.simulator = simulator