# UI Modules
from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class ResultsWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Results")
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

    def display_results(self):

        res = ResultsWindow()
        res.show()