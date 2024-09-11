# -*- coding: utf-8 -*-
"""
    Last update: Dec 26, 2019
    @author:  Mahdi Rouzbahaneh
    This piece of code is ther GUI part of Equivalence Projective Simulation model.
"""
 
import tkinter as tk
import tkinter.ttk as tt
from tkinter import LEFT, TOP, X
from tkinter.filedialog import askopenfilename
import matplotlib as ml
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns
 
ml.use("TkAgg")
 
import pickle
 
#----------------------------------------------------------
class EquivalenceView(tk.Tk):
    env = []        # input parameters
    agn = []        # input parameters
    envDetail = []
    envEntry = {}   # entry collection for environment parameters 
    agnEntry = {}   # entry collection for agent parameters 
    envLabel = {}   # label collection for environment parameters 
    agnLabel = {}   # label collection for agent parameters 
    lblVar = {}
    callback = None
    mainFrame = None
    leftFrame = None
    valid = True
     
    tabs = {}
    fig = {}
    graph = {}
    canvas = {}
    
#------------------------------------------------------
    def __init__(self, environmentParameter, agentParameter, environmentDetailParameter, callback):
        # Inherit from tk.Tk
        super().__init__()

        self.env = environmentParameter
        self.agn = agentParameter
        self.envDetail = environmentDetailParameter
        self.callback = callback
        
        # Title and initial size of the window
        self.title('Equivalence Projective Simulation')
        self.geometry('1000x800')
        
        # Create buttons
        self.toolbar = tk.Frame(self)
        self.toolbar.pack(side=TOP, fill=X)
        self.startButton = tt.Button(self.toolbar, text="Start", command=self.onStart)
        self.startButton.pack(side=LEFT, padx=2, pady=2)
        self.openButton = tt.Button(self.toolbar, text="Open", command=self.onOpen)
        self.openButton.pack(side=LEFT, padx=2, pady=2)
        self.exitButton = tt.Button(self.toolbar, text="Exit", command=self.onExit)
        self.exitButton.pack(side=LEFT, padx=2, pady=2)
        
        self.lblVar['statusBar'] = tk.StringVar()
        self.lblVar['statusBar'].set("Iteration Counter")
        self.statusBar = tt.Label(self.toolbar, textvariable=self.lblVar['statusBar'])
        self.statusBar.pack(side=LEFT, padx=2, pady=2)

        # Create the tabs
        self.notebook = tt.Notebook(self)
        self.notebook.pack(side=TOP, padx=2, pady=2, fill=tk.BOTH)
        
        self.env_tab = tk.Frame(self.notebook)
        self.agn_tab = tk.Frame(self.notebook)

        # Add the tabs to the GUI
        self.notebook.add(self.env_tab, text='environment parameter')
        self.notebook.add(self.agn_tab, text='agent parameter')
        self.initTab(self.env_tab)
        self.initTab(self.agn_tab)
        
        # seve the default values at sixth item, also for recognizing the parameter type
        for k in self.env:
            self.env[k].append(self.env[k][0])
        for k1 in self.agn[1]:
            for k in self.agn[1][k1]:
                self.agn[1][k1][k].append(self.agn[1][k1][k][0])
        
        # Using environment parameters to create the changable form entries
        self.showConfig(self.env_tab, self.env.items(), self.envEntry, self.envLabel, 5)
        
        # Using agent parameters to create the changable form entries
        self.agnLabel['agent_types_0'] = tt.Label(self.agn_tab, text='Agent types').grid(padx=10, pady=0, row=5, column=0, sticky=tk.E)
        self.agnEntry['agent_types'] = tt.Combobox(self.agn_tab, values=self.agn[0]['agent_types'])
        self.agnEntry['agent_types'].grid(padx=5, pady=2, row=5, column=1, sticky=tk.E)  #row=5, column=1, sticky=tk.E)
        self.agnEntry['agent_types'].current(0)
        for i in range(1, 4):
            self.agnLabel['agent_types_'+str(i)] = tt.Label(self.agn_tab, text='')
        self.showConfig(self.agn_tab, self.agn[1][self.agnEntry['agent_types'].get()].items(), self.agnEntry, self.agnLabel, 6)
        self.agnEntry['agent_types'].bind("<<ComboboxSelected>>", self.agentTypeEvent)
        
        self.createEvents(self.envEntry)
        self.createEvents(self.agnEntry)
    
        #style1 = tt.Style()
        #style1.configure("BW.TEntry", foreground="black", background="white")
        style1 = tt.Style()
        style1.configure("B.TEntry", foreground="black")
        style1.configure("R.TEntry", foreground="red")
        style1.configure("B.TLabel", foreground="black")
        style1.configure("R.TLabel", foreground="red")
        
        self.minMaxUpdate(self.env.items(), self.envLabel)
        self.minMaxUpdate(self.agn[1][self.agnEntry['agent_types'].get()].items(), self.agnLabel)
        
#------------------------------------------------------
    def initTab(self, tab):
        # Using environment parameters to create the changable form entries
        title = ('name', 'amount', 'min', 'max', 'comment')
        for i in range(4):
            tt.Label(tab, text=title[i], font="-weight bold").grid(padx=10, pady=2, row=2, column=i, sticky=tk.E)
        tt.Label(tab, text=title[4], font="-weight bold").grid(padx=10, pady=2, row=2, column=4, sticky=tk.W)
        
        tab.grid_columnconfigure(0, minsize=150)
        tab.grid_columnconfigure(1, minsize=160)
        tab.grid_columnconfigure(2, minsize=100)
        tab.grid_columnconfigure(3, minsize=100)

# ---------------------------------------------            
    def showConfig(self, tab, items, txt, lbl, row):
        i = row
        for k, v in items:
            i = i+2
            if v[3] in ('read', 'edit'):
                lbl[k+'_0'] = tt.Label(tab, text=k, style="B.TLabel")
                lbl[k+'_0'].grid(padx=10, pady=2, row=i, column=0, sticky=tk.E)
                
                if v[4] in ('int', 'float'):
                    txt[k] = tt.Entry(tab, style="B.TEntry")
                    txt[k].configure(state='normal')
                    txt[k].insert(0, v[0])
                else:
                    txt[k] = tt.Combobox(tab, values=self.agn[0][v[4]])
                    txt[k].configure(state='normal')
                    txt[k].current(self.agn[0][v[4]].index(v[0]))
                    
                txt[k].grid(padx=5, pady=2, row=i, column=1, sticky=tk.E)   #padx=1, row=i, column=1)

                if v[4] in ('int', 'float'):
                    
                    lbl1 = ''
                    if v[1] is not None:
                        if (type(v[1]) is int):
                            lbl1 = '>='+str(v[1])
                        if (type(v[1]) is float):
                            lbl1 = '>'+str(v[1])
                        if (type(v[1]) is str):
                            lbl1 = v[1]
                        
                        self.lblVar[k+'_1'] = tk.StringVar()
                        self.lblVar[k+'_1'].set(lbl1)
                        lbl[k+'_1'] = tt.Label(tab, textvariable=self.lblVar[k+'_1'])
                        lbl[k+'_1'].grid(padx=10, pady=2, row=i, column=2, sticky=tk.E)
                    else:
                        lbl[k+'_1'] = tt.Label(tab, text='')

                    lbl1 = ''
                    if v[2] is not None:
                        if (type(v[2]) is int):
                            lbl1='<='+str(v[2])
                        if (type(v[2]) is float):
                            lbl1='<'+str(v[2])
                        if (type(v[2]) is str):
                            lbl1 = v[2]
                            
                        self.lblVar[k+'_2'] =tk.StringVar()
                        self.lblVar[k+'_2'].set(lbl1)
                        lbl[k+'_2'] = tt.Label(tab, textvariable=self.lblVar[k+'_2'])
                        lbl[k+'_2'].grid(padx=10, pady=2, row=i, column=3, sticky=tk.E)
                    else:
                        lbl[k+'_2'] = tt.Label(tab, text='')
    
                else:
                    lbl[k+'_1'] = tt.Label(tab, text='')
                    lbl[k+'_2'] = tt.Label(tab, text='')

                lbl[k+'_3'] = tt.Label(tab, text=v[5])
                lbl[k+'_3'].grid(padx=10, pady=2, row=i, column=4, sticky=tk.W)
                            
                if v[3] == 'read':
                    txt[k].configure(state='disabled')
    
# ---------------------------------------------            
    def evalExpression(self, expression):
        expr = expression
        equal = ''
        if expression[0] == '=':
            expr = expr[1:]
            equal = '='

        while expr.find("[") >= 0:
            txt = expr[expr.find("[")+1:expr.find("]")]
            if txt in self.agn[1][self.agnEntry['agent_types'].get()]:
                expr = expr.replace("[" + txt + "]", str(self.agn[1][self.agnEntry['agent_types'].get()][txt][0]), 1)
            elif txt in self.envEntry:
                expr = expr.replace("[" + txt + "]", str(self.envEntry[txt].get()), 1)
            elif int(self.envEntry['environment_ID'].get()) in self.envDetail:
                if txt in self.envDetail[int(self.envEntry['environment_ID'].get())]:
                    expr = expr.replace("[" + txt + "]", str(self.envDetail[int(self.envEntry['environment_ID'].get())][txt]), 1)
            else:
                return equal, ''
            
        try:
            n = eval(expr)
            if type(n) == int:
                return equal, n
            if type(n) == float:
                return equal, int(n*10000)/10000
        except ZeroDivisionError:
            self.valid = False
            return equal, 'ERROR'
                
# ---------------------------------------------                
    def createEvents(self, txt):
        for t in txt:
            #if t.winfo_class() == 'Entry':
            txt[t].bind('<KeyRelease>', self.entryChangeEvent)
        
# ---------------------------------------------            
    def agentTypeEvent(self, *args):
        while len(self.agnEntry) > 1:
            for entry in self.agnEntry:
                if entry != 'agent_types':
                    self.agnEntry[entry].destroy()
                    del self.agnEntry[entry]
                    break
        
        lbl2 = {}
        for lbl1 in self.agnLabel:
            if lbl1[0:11] != 'agent_types':
                lbl2[lbl1] = self.agnLabel[lbl1]

        while len(lbl2) > 0:
            for lbl1 in lbl2:
                self.agnLabel[lbl1].destroy()
                del self.agnLabel[lbl1]
                del lbl2[lbl1]
                break
        
        self.showConfig(self.agn_tab, self.agn[1][self.agnEntry['agent_types'].get()].items(), self.agnEntry, self.agnLabel, 6)
        self.minMaxUpdate(self.agn[1][self.agnEntry['agent_types'].get()].items(), self.agnLabel)
        self.valid = self.checkAll()
        self.createEvents(self.agnEntry)
            
# ---------------------------------------------                
    def entryChangeEvent(self, event):
        self.valid = self.checkAll()
        
# ---------------------------------------------                        
    def checkAll(self):
        if self.readValue() == False:
            return False;
        
        self.minMaxUpdate(self.env.items(), self.envLabel)
        self.minMaxUpdate(self.agn[1][self.agnEntry['agent_types'].get()].items(), self.agnLabel)
        
        return self.minMaxCheck()

# ---------------------------------------------                        
    def readValue(self):
        isValid = True
        for e in self.agnEntry:
            if e != 'agent_types' and self.agn[1][self.agnEntry['agent_types'].get()][e][4] in ('int', 'float'):
                value = self.parse(self.agnEntry[e].get(), self.agn[1][self.agnEntry['agent_types'].get()][e][4])
                if value == 'type-error':
                    self.agnEntry[e].configure(style="R.TEntry")
                    isValid = False
                else:
                    self.agnEntry[e].configure(style="B.TEntry")
                    self.agn[1][self.agnEntry['agent_types'].get()][e][0] = value
                    
        for e in self.envEntry:
            value = self.parse(self.envEntry[e].get(), self.env[e][4])
            if value == 'type-error':
                self.envEntry[e].configure(style="R.TEntry")
                isValid = False
            else:
                self.envEntry[e].configure(style="B.TEntry")
                self.env[e][0] = value
                
        return isValid
        
# ---------------------------------------------                
    def minMaxUpdate(self, items, lbl):
        for k, v in items:
            if v[3] in ('read', 'edit'):
                if v[1] is not None:
                    if (type(v[1]) is str):
                        equal, val = self.evalExpression(v[1])
                        self.lblVar[k+'_1'].set('>' + equal + str(val))
                        if val == 'ERROR':
                            lbl[k+'_1'].configure(style="R.TLabel")
                        else:
                            lbl[k+'_1'].configure(style="B.TLabel")
                            
                if v[2] is not None:
                    if (type(v[2]) is str):
                        equal, val = self.evalExpression(v[2])
                        self.lblVar[k+'_2'].set('<' + equal + str(val))
                        if val == 'ERROR':
                            lbl[k+'_2'].configure(style="R.TLabel")
                        else:
                            lbl[k+'_2'].configure(style="B.TLabel")

# ---------------------------------------------                
    def minMaxCheck(self):
        isValid = True

        for e in self.envEntry:
            if self.envLabel[e+'_1']['text'] != '':
                if eval(self.envEntry[e].get() + self.envLabel[e+'_1']['text']) == False:
                    self.envEntry[e].configure(style="R.TEntry")
                    isValid = False
                else:
                    self.envEntry[e].configure(style="B.TEntry")
            if self.envLabel[e+'_2']['text'] != '':
                if eval(self.envEntry[e].get() + self.envLabel[e+'_2']['text']) == False:
                    self.envEntry[e].configure(style="R.TEntry")
                    isValid = False
                else:
                    self.envEntry[e].configure(style="B.TEntry")

        for e in self.agnEntry:
            if self.agnLabel[e+'_1']['text'] != '':
                if eval(self.agnEntry[e].get() + self.agnLabel[e+'_1']['text']) == False:
                    self.agnEntry[e].configure(style="R.TEntry")
                    isValid = False
                else:
                    self.agnEntry[e].configure(style="B.TEntry")
            if self.agnLabel[e+'_2']['text'] != '':
                if eval(self.agnEntry[e].get() + self.agnLabel[e+'_2']['text']) == False:
                    self.agnEntry[e].configure(style="R.TEntry")
                    isValid = False
                else:
                    self.agnEntry[e].configure(style="B.TEntry")
            
        return isValid

# ---------------------------------------------        
    def parse(self, value, t):
        if t == "int":
            try:
                return int(value)
            except:
                return 'type-error'
            
        elif t == "float":
            try:
                return float(value)
            except:
                return 'type-error'
        else:
            return value
        
# ---------------------------------------------        
    def parse1(self, value, reference):
        if type(reference) == str:
            return str(value)
        
        elif type(reference) == bool:
            if value.lower() in ("yes", "true", "t", "1"):
                return True
            elif value.lower() in ("no", "false", "f", "0"):
                return False
            else:
                return 'type-error'
            
        elif type(reference) == float or type(reference) == int:
            try:
                return int(value)
            except:
                try:
                    return float(value)
                except:
                    return 'type-error'
            
# ---------------------------------------------            
    def onStart(self):
        if self.valid == True:
            selectedAgent = self.agn[1][self.agnEntry['agent_types'].get()]
            selectedAgent['agent_type'] = self.agnEntry['agent_types'].get()
            fileName = self.callback(self.env, selectedAgent, self.showMessage)
            self.showFile(fileName)

# ---------------------------------------------            
    def showMessage(self, message):
        self.lblVar['statusBar'].set(message)
        self.update_idletasks()
        self.update()
        a = message
        
# ---------------------------------------------            
    def onOpen(self):
        fileName =  tk.filedialog.askopenfilename(initialdir = "results/", title = "Select result file", \
            filetypes = (("p files","*.p"),("all files","*.*")))
        self.showFile(fileName)

# ---------------------------------------------            
    def showFile(self, fileName):
        try:
            resultFile = open(fileName, 'rb')
            data = pickle.load(resultFile)
            resultFile.close()
                
            self.showResaltTabs(data);
        except:
            print("No file exists")

# ---------------------------------------------            
    def onExit(self):
        self.destroy()
        
# ---------------------------------------------        
    def OnTrace(self, varname, elementname, mode):
        pass
        
# ---------------------------------------------        
    def showResaltTabs(self, data):
        while len(self.tabs) > 0:
            for tab in self.tabs:
                self.tabs[tab].destroy()
                self.fig[tab].destroy()
                self.canvas[tab].destroy()
                del self.tabs[tab]
                del self.fig[tab]
                del self.canvas[tab]
                break

        for i in range(len(data['show'])):
            result = data['result'][data['show'][i][0]]
            showType = data['show'][i][1]
            name = data['show'][i][0] + '_' + showType
            
            # Add tab
            self.tabs[name] = tk.Frame(self.notebook)
            self.notebook.add(self.tabs[name], text=name)
            
            # Add the figure and canvas to the tab
            self.fig[name] = plt.Figure(figsize=(18, 18), dpi=100)
            self.canvas[name] = FigureCanvasTkAgg(self.fig[name], master=self.tabs[name])
            self.canvas[name].get_tk_widget().pack(fill=tk.BOTH)

            # show the result
            if showType == 'bar':
                self.barDiagramShow(name, result)
            elif showType == 'heatmap':
                self.heatmapShow(name, result)
            elif showType == 'graph':
                self.graphShow(name, result)
            
 # ---------------------------------------------           
#    def barDiagramShow(self, name, data):
#        ax1 = self.fig[name].add_subplot(111)
#        data.plot(kind='bar', ax=ax1)
#        self.canvas[name].draw()
        
 # ---------------------------------------------  
#    def heatmapShow(self, name, data):
#        ax1 = self.fig[name].add_subplot(111)
#        sns.heatmap(data, annot=True, ax=ax1)
#        self.canvas[name].draw()
#        
# # ---------------------------------------------  
    def graphShow(self, name, data):
        ax1 = self.fig[name].add_subplot(111)
        #graphx = nx.from_pandas_dataframe(data, edge_attr=True)
        nx.draw(data, ax=ax1, with_labels=True, font_weight='bold')
        self.canvas[name].draw()
        
# ---------------------------------------------   
    def barDiagramShow(self, name,  data):
        ax1 = self.fig[name].add_subplot(111)
        data.plot(kind='bar', color=['royalblue','lightgreen', 'red','cyan'], ax=ax1)
        ax1.legend(fontsize = 16)
        ax1.tick_params(labelsize = 16, rotation=45)
        ax1.set_title(name, fontsize = 20)
        ax1.set_ylabel('Correct match ratio', fontsize = 20)
        
        for label in ax1.get_xticklabels():
            label.set_ha("right")
            label.set_rotation(45)
            
        ax1.xaxis.label.set_size(20)
        ax1.tick_params(labelsize = 16)
        #self.fig[name].tight_layout()
        self.canvas[name].draw() 
 
# --------------------------------------------- 
    def heatmapShow(self, name, data):
        ax1 = self.fig[name].add_subplot(111)
        sns.heatmap(data, annot = True, annot_kws = {"size": 14}, \
                    linewidths=.15, cmap="Blues", ax=ax1) 
        ax1.set_title(name, fontsize = 16)
        ax1.tick_params(labelsize = 16)
        #self.fig[name].tight_layout()
        self.canvas[name].draw() 
    
# if __name__ == '__main__':
    
