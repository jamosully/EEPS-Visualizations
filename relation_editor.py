from PySide6 import QtCore, QtWidgets 
from PySide6.QtWidgets import (QTabWidget, QTableWidget, QTableWidgetItem, 
                               QLabel, QDoubleSpinBox, QSizePolicy, 
                               QHeaderView, QVBoxLayout)
from PySide6.QtGui import QFont, QColor

class RelationEditor(QtWidgets.QWidget):

    def __init__(self, simulator):

        self.editor_layout =  QVBoxLayout()