# UI Modules
from PySide6 import QtCore
from PySide6.QtCore import Slot, Signal

# EEPS Modules
import EEPS.initialization as initialization
import EEPS.initialization_detail as initialization_detail
import EEPS.environment as env
import EEPS.agent as agn
import EEPS.interaction as intrc

class Simulator(QtCore.QObject):

    wait_for_input = Signal()
    proceed = Signal()

    def __init__(self, mutex):
        QtCore.QObject.__init__(self)
        self.mtx = mutex
        # self.cond = cond
        self.agent = None
    
    Slot()
    def initialize_model(self, step, memory_visualizer, rdt_visualizer):

        # self.cond.wait(self.mtx)
        self.environment_detail = initialization_detail.environment_details()
        self.environment_parameter, self.agent_parameter = initialization.config()

        # TODO: Allow users to upload files
        
        self.file_name = None

        if self.file_name == None:
            self.agent = agn.Agent(self.agent_parameter)
            self.environment = env.Environment(self.environment_parameter)
            self.interaction = intrc.Interaction(self.agent, 
                                                 self.environment, 
                                                 self.agent_parameter, 
                                                 self.environment_parameter, 
                                                 step, 
                                                 memory_visualizer,
                                                 rdt_visualizer,
                                                 self.mtx)
            self.file_name = self.interaction.file_name

        rdt_visualizer.createClassButtons(self.environment.num_classes)
            
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