# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout

class SidePanel(QWidget):

    def __init__(self, parent):

        self.verticalGroupBox = QGroupBox()

        layout = QVBoxLayout()

        def addToLayout(button, layout):
            layout.addWidget(button)
            layout.setSpacing(10)
            self.verticalGroupBox.setLayout(layout)

