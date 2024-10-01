from PySide6 import QtCore, QtWidgets 
from PySide6.QtWidgets import (QTabWidget, QTableWidget, QTableWidgetItem, 
                               QLabel, QDoubleSpinBox, QSizePolicy, 
                               QHeaderView, QVBoxLayout)
from PySide6.QtGui import QFont, QColor

"""
stimuli_editor.py

The editor can be accessed by clicking on a node in
network via the graph network view. Shows each incoming
and outgoing relation, along with weights
"""

class StimuliEditor(QtWidgets.QWidget):

    """
    Modification panel for changing stimuli weights

    A little cumbersome, but mplcursors doesn't allow
    for the selection of edges so this will have to do
    """

    # TODO: Expand MPLCursors/switch to events for edge weights

    def __init__(self, backend, main, simulator):
        QtWidgets.QWidget.__init__(self)

        self.simulator = simulator
        self.main_display = main
        self.stimulus = None
        self.clip_space = None

        self.editorLayout = QVBoxLayout()

        self.stimulusNameLabel = QLabel()
        self.stimulusNameLabel.setText("")
        self.stimulusNameLabel.setFont(QFont('Arial', 20))
        self.editorLayout.addWidget(self.stimulusNameLabel)

        self.createRelationTables()
        self.editorLayout.addWidget(self.tableHolder)

        self.setLayout(self.editorLayout)
        # self.actionRelationTable.resizeColumnsToContents()

    def set_stimuli(self, stimulus):

        self.stimulus = stimulus
        self.stimulusNameLabel.setText(stimulus)
        self.editorLayout.addWidget(self.tableHolder)

    def createRelationTables(self):

        """
        Two tables: one for relations that are linked to the currently
        chosen stimuli e.g., Y -> X, another where the currently chosen stimuli is related
        to them e.g, X -> Y
        """
        
        # Column One: Stimuli name
        # Column Two: Is this stimuli the correct choice? GREEN = YES, RED = NO
        # Column Three: Strength of relation

        self.tableHolder = QTabWidget()

        # Create table for the relations in which the current
        # stimuli was the chosen response
        
        # self.actionRelationTable = QTableWidget(len(self.clip_space.in_edges(self.stimulus)), 3)
        # self.formatTable(self.actionRelationTable, self.clip_space.in_edges(self.stimulus), 0)

        # # Create table for the relations in which the current
        # # stimuli was perceived first

        # self.perceptRelationTable = QTableWidget(len(self.clip_space.out_edges(self.stimulus)), 3)
        # self.formatTable(self.perceptRelationTable, self.clip_space.out_edges(self.stimulus), 1) 

        self.actionRelationTable = QTableWidget(0, 3)
        self.perceptRelationTable = QTableWidget(0, 3)

        self.actionRelationTable.verticalHeader().setVisible(False)
        self.actionRelationTable.horizontalHeader().setVisible(False)

        self.perceptRelationTable.verticalHeader().setVisible(False)
        self.perceptRelationTable.horizontalHeader().setVisible(False)

        self.tableHolder.addTab(self.actionRelationTable, "As Action")
        self.tableHolder.addTab(self.perceptRelationTable, "As Percept")

    # TODO: This function is useful, maybe update the parameter toolbox to include something similar

    def formatTable(self, table: QTableWidget, edge_list, edgeIndex):

        """
        The relation table contains three columns:

        Column 1: Name of other stimuli in relation

        Column 2: Is that relation correct? (GREEN = YES, RED = NO)

        Column 3: Strength of the relation
        """

        # Add/remove rows using edge list length

        if table.rowCount() < len(edge_list):
            for x in range(len(edge_list) - table.rowCount()):
                table.insertRow(table.rowCount())
        elif table.rowCount() > len(edge_list):
            for x in range(table.rowCount() - len(edge_list)):
                table.removeRow(table.rowCount())

        # TODO: Maybe normalise relation weights

        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        #table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setVisible(False)
        table.setMaximumHeight(table.verticalHeader().length())

        for i, edge in enumerate(edge_list):
            edgeNameLabel = QLabel()
            edgeNameLabel.setText(edge[edgeIndex])
            table.setCellWidget(i, 0, edgeNameLabel)
            table.setItem(i, 1, QTableWidgetItem())
            if edge[edgeIndex][1] == self.stimulus[1]:
                table.item(i, 1).setBackground(QColor("Green"))
            else:
                table.item(i, 1).setBackground(QColor("Red"))
            edgeWeightSpinBox = EdgeWeightSpinBox(edge)
            edgeWeightSpinBox.setValue(self.clip_space.edges[edge[0], edge[1]]['weight'])
            edgeWeightSpinBox.valueChanged.connect(lambda: self.edge_weight_changed(edgeWeightSpinBox.edge, edgeWeightSpinBox.value()))
            table.setCellWidget(i, 2, edgeWeightSpinBox)

        table.resizeColumnsToContents()

    def updateTable(self, table: QTableWidget, edge_list, edge_index):

        # TODO: This method can't add new cells yet? Need to figure out how

        for i, edge in enumerate(edge_list):
            for x in range(table.rowCount()):
                if table.cellWidget(x, 0).text() == edge[edge_index]:
                    table.cellWidget(x, 2).setValue(self.clip_space.edges[edge[0], edge[1]]['weight'])


    def edge_weight_changed(self, edge, new_value):

        self.clip_space.edges[edge[0], edge[1]]['weight'] = new_value
        self.main_display.edits_made = True
        self.main_display.edited_clip_space = self.clip_space

    def populateEditor(self, stimuli, clip_space):

        self.set_stimuli(stimuli)
        self.clip_space = clip_space

        action_edges = clip_space.in_edges(stimuli)
        percept_edges = clip_space.out_edges(stimuli)

        self.formatTable(self.actionRelationTable, action_edges, 0)
        self.formatTable(self.perceptRelationTable, percept_edges, 1)

    def updateEditor(self, clip_space):

        if self.stimulus is not None:
            self.clip_space = clip_space

            action_edges = clip_space.in_edges(self.stimulus)
            percept_edges = clip_space.out_edges(self.stimulus)

            self.updateTable(self.actionRelationTable, action_edges, 0)
            self.updateTable(self.perceptRelationTable, percept_edges, 1)
         

class EdgeWeightSpinBox(QtWidgets.QDoubleSpinBox):

    def __init__(self, edge):
        super(EdgeWeightSpinBox, self).__init__()

        self.edge = edge
        self.setMaximum(100000)
        self.setDecimals(5)

    def update_value(self, new_value):

        self.setValue(new_value)

