from PySide6 import QtCore, QtWidgets 
from PySide6.QtWidgets import (QTabWidget, QTableWidget, QTableWidgetItem, 
                               QLabel, QDoubleSpinBox, QSizePolicy, 
                               QHeaderView, QVBoxLayout)
from PySide6.QtGui import QFont, QColor

class StimuliEditor(QtWidgets.QWidget):

    def __init__(self, main, simulator, stimuli, clip_space):
        QtWidgets.QWidget.__init__(self)

        self.simulator = simulator
        self.main_display = main
        self.stimuli = stimuli
        self.clip_space = clip_space

        self.editor_layout = QVBoxLayout()

        self.stimuliNameLabel = QLabel()
        self.stimuliNameLabel.setText(self.stimuli)
        self.stimuliNameLabel.setFont(QFont('Arial', 20))
        self.editor_layout.addWidget(self.stimuliNameLabel)

        self.createRelationTables()
        self.editor_layout.addWidget(self.table_holder)

        self.setLayout(self.editor_layout)
        self.in_relation_table.resizeColumnsToContents()

        self.main_display.setFixedSize(self.main_display.grid.sizeHint())

    def createRelationTables(self):
        
        # Column One: Stimuli name
        # Column Two: Is this stimuli the correct choice? GREEN = YES, RED = NO
        # Column Three: Strength of relation

        self.table_holder = QTabWidget()

        # Create table for the outgoing relations
        # TODO: Find out the name for this particular type of relation
        
        self.in_relation_table = QTableWidget(len(self.clip_space.in_edges(self.stimuli)), 3)
        self.formatTable(self.in_relation_table, self.clip_space.in_edges(self.stimuli))

        self.out_relation_table = QTableWidget(len(self.clip_space.out_edges(self.stimuli)), 3)
        self.formatTable(self.out_relation_table, self.clip_space.out_edges(self.stimuli)) 

        self.table_holder.addTab(self.in_relation_table, "In")
        self.table_holder.addTab(self.out_relation_table, "Out")

    # TODO: This function is useful, maybe update the parameter toolbox to include something similar

    def formatTable(self, table: QTableWidget, edge_list):

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
