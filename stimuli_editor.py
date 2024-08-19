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

    def __init__(self, main, simulator, stimuli, clip_space):
        QtWidgets.QWidget.__init__(self)

        self.simulator = simulator
        self.main_display = main
        self.stimuli = stimuli
        self.clip_space = clip_space

        self.editorLayout = QVBoxLayout()

        self.stimuliNameLabel = QLabel()
        self.stimuliNameLabel.setText(self.stimuli)
        self.stimuliNameLabel.setFont(QFont('Arial', 20))
        self.editorLayout.addWidget(self.stimuliNameLabel)

        self.createRelationTables()
        self.editorLayout.addWidget(self.tableHolder)

        self.setLayout(self.editorLayout)
        self.actionRelationTable.resizeColumnsToContents()

        self.main_display.setFixedSize(self.main_display.grid.sizeHint())

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
        
        self.actionRelationTable = QTableWidget(len(self.clip_space.in_edges(self.stimuli)), 3)
        self.formatTable(self.actionRelationTable, self.clip_space.in_edges(self.stimuli))

        # Create table for the relations in which the current
        # stimuli was perceived first

        self.perceptRelationTable = QTableWidget(len(self.clip_space.out_edges(self.stimuli)), 3)
        self.formatTable(self.perceptRelationTable, self.clip_space.out_edges(self.stimuli)) 

        self.tableHolder.addTab(self.actionRelationTable, "As Action")
        self.tableHolder.addTab(self.perceptRelationTable, "As Percept")

    # TODO: This function is useful, maybe update the parameter toolbox to include something similar

    def formatTable(self, table: QTableWidget, edge_list):

        """
        The relation table contains three columns:

        Column 1: Name of other stimuli in relation

        Column 2: Is that relation correct? (GREEN = YES, RED = NO)

        Column 3: Strength of the relation
        """

        # TODO: Maybe normalise relation weights

        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        #table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setVisible(False)
        table.setMaximumHeight(table.verticalHeader().length())

        for i, edge in enumerate(edge_list):
            edgeNameLabel = QLabel()
            edgeNameLabel.setText(edge[0])
            table.setCellWidget(i, 0, edgeNameLabel)
            table.setItem(i, 1, QTableWidgetItem())
            if edge[0][1] == self.stimuli[1]:
                table.item(i, 1).setBackground(QColor("Green"))
            else:
                table.item(i, 1).setBackground(QColor("Red"))
            edgeWeightSpinBox = QDoubleSpinBox()
            edgeWeightSpinBox.setValue(self.clip_space.edges[edge[0], edge[1]]['weight'])
            edgeWeightSpinBox.setMaximum(100000)
            edgeWeightSpinBox.setDecimals(5)
            table.setCellWidget(i, 2, edgeWeightSpinBox)
