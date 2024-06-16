import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QCheckBox, QWidget, QGridLayout, QHBoxLayout
from PySide6.QtWidgets import QMainWindow, QLineEdit, QLabel, QComboBox
import initialization
import initialization_detail
import environment as env
import agent as agn
import interaction as intrc
import pdb
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        """
        Code sourced from:
        https://stackoverflow.com/questions/12459811/how-to-embed-matplotlib-in-pyqt
        """

        self.setWindowTitle("Affinity.net")

        control_widget = QWidget(self)
        control_layout = QGridLayout(control_widget)
        control_layout.setColumnStretch(1, 1)

        self.figure = Figure()

        canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(canvas, self)

        main_widget = QWidget(self)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setStretch(0, 1)
        main_layout.addWidget(control_widget)
        main_layout.addWidget(canvas)

        # self.button = QtGui.QPushButton('Plot')
        # self.button.clicked.connect(self.plot_agent_memory)

        # layout = QtGui.QVBoxLayout()
        # layout.addWidget(self.toolbar)
        # layout.addWidget(self.canvas)
        # layout.addWidget(self.button)
        # self.setLayout(layout)

    @QtCore.Slot()
    def plot_agent_memory(self):
        return

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())