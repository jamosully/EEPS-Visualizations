# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QWidget, QGridLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class NetworkVisualizer(QtWidgets.QWidget):

    def __init__(self, parent, simulator):
        QtWidgets.QWidget.__init__(self)

        grid = QGridLayout()
        self.setLayout(grid)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        #self.toolbar = NavigationToolbar(self.canvas, self)

        grid.addWidget(self.canvas)

        simulator.setCanvasAndFigure(self.canvas, self.figure)