import sys
import random

# UI Modules
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QGridLayout, QVBoxLayout, QPushButton, QGroupBox, QSlider
from PySide6.QtCore import Slot, Signal, QThread, QMutex, QWaitCondition
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

# EEPS Modules
import EEPS.initialization as initialization
import EEPS.initialization_detail as initialization_detail
import EEPS.environment as env
import EEPS.agent as agn
import EEPS.interaction as intrc
import pdb


class Simulator(QtCore.QObject):

    wait_for_input = Signal()
    proceed = Signal()

    def __init__(self, mutex):
        QtCore.QObject.__init__(self)
        self.mtx = mutex
        # self.cond = cond

    Slot()
    def initialize_model(self, canvas, step, figure):

        # self.cond.wait(self.mtx)
        self.environment_detail = initialization_detail.environment_details()
        self.environment_parameter, self.agent_parameter = initialization.config()

        # TODO: Allow users to upload files
        
        file_name = None

        if file_name == None:
            self.agent = agn.Agent(self.agent_parameter)
            self.environment = env.Environment(self.environment_parameter)
            self.interaction = intrc.Interaction(self.agent, self.environment, self.agent_parameter,
                                                                self.environment_parameter, step, canvas, figure, self.mtx)
            self.file_name = self.interaction.file_name
            
    Slot()
    def run_sim(self):

        if self.interaction is not None:
            self.interaction.run_save()
            file_name = self.interaction.file_name
            print(file_name)

    Slot()
    def continue_sim(self):

        if self.interaction is not None:
            self.interaction.continue_sim()

    Slot()
    def display_results(self):

        self.results = intrc.Plot_results(self.file_name)
        self.results.showResults()

    Slot()
    def on_pick(self, event):
        artist = event.artist
        x_mouse, y_mouse = event.mouseevent.xdata, event.mouseevent.ydata
        ax = event.canvas.figure.gca()
        print(ax)
        # x, y = artist.get_xdata(), artist.get_ydata()
        print(str(x_mouse) + '\n' + str(y_mouse))


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


class MainWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        # Code sourced from:
        # https://stackoverflow.com/questions/35328916/embedding-a-networkx-graph-into-pyqt-widget
        
        self.setWindowTitle("Affinity.net")

        grid = QGridLayout()
        self.setLayout(grid)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.step = 100

        self.createSimulator()
        self.createVerticalGroupBox()
        self.createStepSlider()

        self.canvas.callbacks.connect('pick_event', self.simulator.on_pick)

        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.verticalGroupBox)
        buttonLayout.addWidget(self.stepslider)

        grid.addWidget(self.toolbar, 0, 1)
        grid.addWidget(self.canvas, 1, 1, 9, 9)
        grid.addLayout(buttonLayout, 1, 0)

    def createSimulator(self):

        self.mutex = QMutex()
        self.cond = QWaitCondition()
        self.simulator = Simulator(self.mutex)
        self.simulator_thread = QThread()

        self.simulator.moveToThread(self.simulator_thread)

        self.simulator_thread.started.connect(self.simulator.run_sim)

    def createVerticalGroupBox(self):
        
        self.verticalGroupBox = QGroupBox()

        layout = QVBoxLayout()

        def addToLayout(button, layout):
            layout.addWidget(button)
            layout.setSpacing(10)
            self.verticalGroupBox.setLayout(layout)

        initSimButton = QPushButton("Initialize Parameters")
        initSimButton.setObjectName("Initialize Parameters")
        addToLayout(initSimButton, layout)
        initSimButton.clicked.connect(self.simulator.initialize_model(self.canvas, self.step, self.figure))

        runSimButton = QPushButton("Run Simulation")
        runSimButton.setObjectName("Run Simulation")
        addToLayout(runSimButton, layout)
        runSimButton.clicked.connect(self.simulator_thread.start)

        stepButton = QPushButton("Step")
        stepButton.setObjectName("Step")
        addToLayout(stepButton, layout)
        stepButton.clicked.connect(self.simulator.mtx.unlock)

    def createStepSlider(self):

        # TODO: Improve this, and link it to self.step
        
        self.stepslider = QSlider()
        self.stepslider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.stepslider.setTickInterval(5)
        self.stepslider.setMinimum(1)
        self.stepslider.setEnabled(True)

        self.stepslider.valueChanged.connect(self.adjust_step_count)

    def adjust_step_count(self, value):
        print(self.step)
        self.step = value * 100

        

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())