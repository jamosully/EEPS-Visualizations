# -*- coding: utf-8 -*-
"""
Last update:  Dec. 26, 2019

@author: Asieh Abolpour Mofrad & Mahdi Rouzbahaneh

Initialization values details:  training and testing blocks and 
the desired plots must be determined here
"""

def environment_parameters_details(ID):
    d = environment_details()
    return d[ID]['num_classes'], d[ID]['training_order'], d[ID]['testing_order'],\
    d[ID]['test_block_ID'], d[ID]['plot_blocks'], d[ID]['plot_blocks_ID'],\
    d[ID]['mastery_training']
    

def environment_details():
    """
    Here the information for the environment will be provided.
    The number is what in the interaction file must be specified.
    plot_blocks is a tuple that shows what extra representation, 
    rather than the testing blocks is desired.
    """
    environment_parameters_detail = {
    1: { # This is the example at the paper
        "num_classes":3,
        "training_order": {1:[('A','B',30)],
                        2:[('B','C',30)],
                        3:[('D','C',30)]},
        "testing_order": {1:[('A','B',9),('B','C',9),('D','C',9)],
                       2:[('B','A',9),('C','B',9), ('C','D',9)],
                       3:[('A','C',9)],
                       4:[('C','A',9),('B','D',9),('D','B',9),('A','D',9),
                          ('D','A',9)]},
        "test_block_ID": {1:'Baseline', 2:'Symmetry', 3:'Transivity', 4:'Equivalence'},
        # this is the label of the data for each block in test phase
 
        "plot_blocks": {'relatin_type':{'Direct':['AB','BC','DC'],
                        'Derived':['BA','CB','CD','AC','CA','BD','DB','AD','DA']}},
                    
        "plot_blocks_ID": {'relatin_type':['Direct','Derived']},
 
        "mastery_training":  0.9 },
 
 
    2: { # This is the Sidman and Tailby experiment (1982)
        "num_classes": 3,
        "training_order": {1:[('A1','B1',10),('A2','B2',10)],
                        2:[('A1','B1',10),('A3','B3',10)],
                        3:[('A2','B2',10),('A3','B3',10)],
                        4:[('A1','B1',10),('A2','B2',10),('A3','B3',10)],
                        5:[('A1','C1',10),('A2','C2',10)],
                        6:[('A1','C1',10),('A3','C3',10)],
                        7:[('A2','C2',10),('A3','C3',10)],
                        8:[('A1','C1',10),('A2','C2',10),('A3','C3',10)],
                        9: [('A1','B1',5),('A2','B2',5),('A3','B3',5),
                            ('A1','C1',5),('A2','C2',5), ('A3','C3',5)],
                        10: [('D1','C1',10),('D2','C2',10)],
                        11:[('D1','C1',10),('D3','C3',10)],
                        12: [('D2','C2',10),('D3','C3',10)],
                        13:[('D1','C1',10),('D2','C2',10),('D3','C3',10)],
                        14:[('A1','B1',5),('A2','B2',5),('A3','B3',5),
                            ('A1','C1',5),('A2','C2',5), ('A3','C3',5),
                            ('D1','C1',5),('D2','C2',5),('D3','C3',5)]
                        },
 
        "testing_order":{1:[('A','B',30)],
                       2:[('A','C',30)],
                       3:[('D','C', 30)],
                       4:[('B','A',30)],
                       5:[('C','A',30)],
                       6:[ ('C','D',30)],
                       7:[('A','D',30)],
                       8:[('D','A',30)],
                       9:[('C','B',30)],
                      10:[('B','C',30)],
                      11:[('B','D',30)],
                      12:[('D','B',30)]
                      },
        "test_block_ID": {1:'AB', 2:'AC', 3:'DC', 4:'BA',5:'CA',6:'CD',
                          7:'AD',8:'DA',9:'CB',10:'BC',11:'BD',12:'DB'},
 
        "plot_blocks": {'relatin_type':{'Baseline':['AB','AC','DC'],
                        'Symmetry':['BA','CA','CD'],
                        'Equivalence':['BC','CB','BD','DB','AD','DA']}},
                                        
        "plot_blocks_ID": {'relatin_type':['Baseline','Symmetry','Equivalence']},
 
        "mastery_training": 0.9 },
 
#----------------------------
 
    3: { # This is the Devany et. al. experiment (1986)
        "num_classes": 2,
        "training_order": {1:[('A1','B1',10)],
                        2:[('A2','B2',10)],
                        3:[('A1','B1',5),('A2','B2',5)],
                        4:[('A1','C1',10)],
                        5:[('A2','C2',10)],
                        6:[('A1','C1',5),('A2','C2',5)],
                        7: [('A1','B1',2),('A2','B2',2),('A1','C1',2),('A2','C2',2)]
                        },
 
        "testing_order": {1:[('A','B',20)],
                       2:[('A','C',20)],
                       3:[('B','A', 20)],
                       4:[('C','A',20)],
                       5:[('B','C',20)],
                       6:[('C','B',20)]
                       },
 
        "test_block_ID": {1:'AB', 2:'AC', 3:'BA',4:'CA',5:'BC',6:'CB'},
 
        "plot_blocks": {'relatin_type':{'Baseline':['AB','AC'],'Symmetry':['BA','CA'],
                     'Equivalence':['BC','CB']}},
        
        "plot_blocks_ID": {'relatin_type':['Baseline','Symmetry','Equivalence']},
        
        "mastery_training": 0.9 },
 
#----------------------------
 
    4: { # This is the Spencer and Chase experiment (1996)
        "num_classes": 3,
        "training_order": {1:[('A','B',48)],
                        2:[('A','B',24),('B','C',24)],
                        3:[('A','B',12),('B','C',12),('C','D',24)],
                        4:[('A','B',9),('B','C',9),('C','D',9),('D','E',24)],
                        5:[('A','B',6),('B','C',6),('C','D',6),('D','E',6),
                           ('E','F',24)],
                        6:[('A','B',3),('B','C',3),('C','D',3),('D','E',6),
                           ('E','F',9),('F','G',24)],
                        7:[('A','B',3),('B','C',3),('C','D',3),('D','E',3),
                           ('E','F',3),('F','G',3)]
                        },
 
        "testing_order": {1:[('A','B',9),('B','C',9),('C','D',9),('D','E',9),
                          ('E','F',9),('F','G',9)],
                       2:[('B','A',9),('C','B',9),('D','C',9),('E','D',9),
                          ('F','E',9),('G','F',9)],
                       3:[('A','C',9),('A','D',9),('A','E',9),('A','F',9),
                          ('A','G',9),('B','D',9),('B','E',9),('B','F',9),
                          ('B','G',9),('C','E',9),('C','F',9),('C','G',9),
                          ('D','F',9),('D','G',9),('E','G',9)],
                       4:[('C','A',9),('D','A',9),('E','A',9),('F','A',9),
                          ('G','A',9),('D','B',9),('E','B',9),('F','B',9),
                          ('G','B',9),('E','C',9),('F','C',9),('G','C',9),
                          ('F','D',9),('G','D',9),('G','E',9)]
                       },
 
        "test_block_ID": {1:'Baseline', 2:'Symmetry', 3:'Transivity',4:'Equivalence'},
 
 
        "plot_blocks": {'nodal_distance':{'Bsl':['AB','BC','CD','DE','EF','FG'],
                     'Sym':['BA','CB','DC','ED','FE','GF'],
                     '1-Tr':['AC','BD','CE','DF','EG'],
                     '2-Tr':['AD','BE','CF','DG'],
                     '3-Tr':['AE','BF','CG'],
                     '4-Tr':['AF','BG'],
                     '5-Tr':['AG'],
                     '1-Eq':['CA','DB','EC','FD','GE'],
                     '2-Eq':['DA','EB','FC','GD'],
                     '3-Eq':['EA','FB','GC'],
                     '4-Eq':['FA','GB'],
                     '5-Eq':['GA']}},
         "plot_blocks_ID": {'nodal_distance':['Bsl','Sym','1-Tr','2-Tr','3-Tr',
                     '4-Tr','5-Tr','1-Eq','2-Eq','3-Eq','4-Eq','5-Eq']},
                                          
        "mastery_training": 0.9 },
 
#----------------------------
    5: { # This is the Spencer and Chase experiment (1996)- with the test based on node distance
        "num_classes": 3,
        "training_order": {1:[('A','B',48)],
                        2:[('A','B',24),('B','C',24)],
                        3:[('A','B',12),('B','C',12),('C','D',24)],
                        4:[('A','B',9),('B','C',9),('C','D',9),('D','E',24)],
                        5:[('A','B',6),('B','C',6),('C','D',6),('D','E',6),
                           ('E','F',24)],
                        6:[('A','B',3),('B','C',3),('C','D',3),('D','E',6),
                           ('E','F',9),('F','G',24)],
                        7:[('A','B',3),('B','C',3),('C','D',3),('D','E',3),
                           ('E','F',3),('F','G',3)]
                        },
 
        "testing_order": {1:[('A','B',9),('B','C',9),('C','D',9),('D','E',9),
                          ('E','F',9),('F','G',9)],
                       2:[('B','A',9),('C','B',9),('D','C',9),('E','D',9),
                          ('F','E',9),('G','F',9)],
                       3:[('A','C',9),('B','D',9),('C','E',9),('D','F',9),
                          ('E','G',9)],
                       4:[('A','D',9),('B','E',9),('C','F',9),('D','G',9)],
                       5:[('A','E',9),('B','F',9),('C','G',9)],
                       6:[('A','F',9),('B','G',9)],
                       7:[('A','G',9)],
                       8:[('C','A',9),('D','B',9),('E','C',9),('F','D',9),
                          ('G','E',9)],
                       9:[('D','A',9),('E','B',9),('F','C',9),('G','D',9)],
                      10:[('E','A',9),('F','B',9),('G','C',9)],
                      11:[('F','A',9),('G','B',9)],
                      12:[('G','A',9)]},
 
        "test_block_ID": {1:'Bsl',2:'Sym',3:'1-Tr',4:'2-Tr',5:'3-Tr',6:'4-Tr',
                       7:'5-Tr', 8:'1-Eq',9:'2-Eq',10:'3-Eq',11:'4-Eq',12:'5-Eq'},
 
        "plot_blocks": {'relatin_type':{'Baseline':['AB','BC','CD','DE','EF','FG'],
                     'Symmetry':['BA','CB','DC','ED','FE','GF'],
                     'Transivity':['AC','BD','CE','DF','EG','AD','BE','CF','DG',
                                   'AE','BF','CG','AF','BG','AG'],
                     'Equivalence':['CA','DB','EC','FD','GE','DA','EB','FC','GD',
                                    'EA','FB','GC','FA','GB','GA']}
                     },
        
        "plot_blocks_ID": {'relatin_type':['Baseline','Symmetry',
                     'Transivity','Equivalence']},

        "mastery_training": 0.9 },
 
#----------------------------
    6: { # This is the Spencer and Chase experiment (1996)- with the test based on node distance
        "num_classes": 3,
        "training_order": {1:[('A','B',48)],
                        2:[('A','B',24),('B','C',24)],
                        3:[('A','B',12),('B','C',12),('C','D',24)],
                        4:[('A','B',9),('B','C',9),('C','D',9),('D','E',24)],
                        5:[('A','B',6),('B','C',6),('C','D',6),('D','E',6),
                           ('E','F',24)],
                        6:[('A','B',3),('B','C',3),('C','D',3),('D','E',6),
                           ('E','F',9),('F','G',24)],
                        7:[('A','B',3),('B','C',3),('C','D',3),('D','E',3),
                           ('E','F',3),('F','G',3)]},
 
        "testing_order": {12:[('A','B',9),('B','C',9),('C','D',9),('D','E',9),
                          ('E','F',9),('F','G',9)],
                       11:[('B','A',9),('C','B',9),('D','C',9),('E','D',9),
                          ('F','E',9),('G','F',9)],
                       10:[('A','C',9),('B','D',9),('C','E',9),('D','F',9),
                          ('E','G',9)],
                       9:[('A','D',9),('B','E',9),('C','F',9),('D','G',9)],
                       8:[('A','E',9),('B','F',9),('C','G',9)],
                       7:[('A','F',9),('B','G',9)],
                       6:[('A','G',9)],
                       5:[('C','A',9),('D','B',9),('E','C',9),('F','D',9),
                          ('G','E',9)],
                       4:[('D','A',9),('E','B',9),('F','C',9),('G','D',9)],
                      3:[('E','A',9),('F','B',9),('G','C',9)],
                      2:[('F','A',9),('G','B',9)],
                      1:[('G','A',9)]},
 
        "test_block_ID": {12:'Bsl',11:'Sym',10:'1-Tr',9:'2-Tr',8:'3-Tr',7:'4-Tr',
                       6:'5-Tr', 5:'1-Eq',4:'2-Eq',3:'3-Eq',2:'4-Eq',1:'5-Eq'},
 
        "plot_blocks": {},
        "plot_blocks_ID": {},
 
        "mastery_training":  0.9 },
        
        #----------------------------
    7: { # This is the Spencer and Chase experiment (1996)- with the test based on node distance
        "num_classes": 3,
        "training_order": {1:[('A','B',48)],
                        2:[('A','B',24),('B','C',24)],
                        3:[('A','B',12),('B','C',12),('C','D',24)],
                        4:[('A','B',9),('B','C',9),('C','D',9),('D','E',24)],
                        5:[('A','B',6),('B','C',6),('C','D',6),('D','E',6),
                           ('E','F',24)],
                        6:[('A','B',3),('B','C',3),('C','D',3),('D','E',6),
                           ('E','F',9),('F','G',24)],
                        7:[('A','B',3),('B','C',3),('C','D',3),('D','E',3),
                           ('E','F',3),('F','G',3)]},
 
        "testing_order": {1:[('A','B',9),('B','C',9),('C','D',9),('D','E',9),
                          ('E','F',9),('F','G',9),('B','A',9),('C','B',9),
                          ('D','C',9),('E','D',9),('F','E',9),('G','F',9),
                          ('A','C',9),('B','D',9),('C','E',9),('D','F',9),
                          ('E','G',9),('A','D',9),('B','E',9),('C','F',9),
                          ('D','G',9),('A','E',9),('B','F',9),('C','G',9),
                          ('A','F',9),('B','G',9),('A','G',9),('C','A',9),
                          ('D','B',9),('E','C',9),('F','D',9),
                          ('G','E',9),('D','A',9),('E','B',9),('F','C',9),
                          ('G','D',9),('E','A',9),('F','B',9),('G','C',9),
                          ('F','A',9),('G','B',9),('G','A',9)]},
 
        "test_block_ID": {1:'Mixed'},                 
                        
        "plot_blocks": {'relatin_type':{'Baseline':['AB','BC','CD','DE','EF','FG'],
                     'Symmetry':['BA','CB','DC','ED','FE','GF'],
                     'Transivity':['AC','BD','CE','DF','EG','AD','BE','CF','DG',
                                   'AE','BF','CG','AF','BG','AG'],
                     'Equivalence':['CA','DB','EC','FD','GE','DA','EB','FC','GD',
                                    'EA','FB','GC','FA','GB','GA']
                     },
                    'nodal_distance':{'Bsl':['AB','BC','CD','DE','EF','FG'],
                     'Sym':['BA','CB','DC','ED','FE','GF'],
                     '1-Tr':['AC','BD','CE','DF','EG'],
                     '2-Tr':['AD','BE','CF','DG'],
                     '3-Tr':['AE','BF','CG'],
                     '4-Tr':['AF','BG'],
                     '5-Tr':['AG'],
                     '1-Eq':['CA','DB','EC','FD','GE'],
                     '2-Eq':['DA','EB','FC','GD'],
                     '3-Eq':['EA','FB','GC'],
                     '4-Eq':['FA','GB'],
                     '5-Eq':['GA']}},
        
        "plot_blocks_ID": {'relatin_type':['Baseline','Symmetry','Transivity',
                     'Equivalence'],
                    'nodal_distance':['Bsl','Sym','1-Tr','2-Tr','3-Tr','4-Tr',
                     '5-Tr','1-Eq','2-Eq','3-Eq','4-Eq','5-Eq']},
 
        "mastery_training":  0.9 },
        
    8: { # This is an alternative to the Sidman and Tailby experiment (1982) 
        "num_classes": 3,
        "training_order": {1:[('A1','B1',10),('B2','A2',10)],
                        2:[('A1','B1',10),('A3','B3',10)],
                        3:[('B2','A2',10),('A3','B3',10)],
                        4:[('A1','B1',10),('B2','A2',10),('A3','B3',10)],
                        5:[('A1','C1',10),('C2','A2',10)],
                        6:[('A1','C1',10),('A3','C3',10)],
                        7:[('C2','A2',10),('A3','C3',10)],
                        8:[('A1','C1',10),('C2','A2',10),('A3','C3',10)],
                        9: [('A1','B1',5),('B2','A2',5),('A3','B3',5),
                            ('A1','C1',5),('C2','A2',5), ('A3','C3',5)],
                        10: [('D1','C1',10),('C2','D2',10)],
                        11:[('D1','C1',10),('D3','C3',10)],
                        12: [('C2','D2',10),('D3','C3',10)],
                        13:[('D1','C1',10),('C2','D2',10),('D3','C3',10)],
                        14:[('A1','B1',5),('B2','A2',5),('A3','B3',5),
                            ('A1','C1',5),('C2','A2',5), ('A3','C3',5),
                            ('D1','C1',5),('C2','D2',5),('D3','C3',5)]
                        },
 
        "testing_order":{1:[('A','B',30)],
                       2:[('A','C',30)],
                       3:[('D','C', 30)],
                       4:[('B','A',30)],
                       5:[('C','A',30)],
                       6:[ ('C','D',30)],
                       7:[('A','D',30)],
                       8:[('D','A',30)],
                       9:[('C','B',30)],
                      10:[('B','C',30)],
                      11:[('B','D',30)],
                      12:[('D','B',30)]
                      },
        "test_block_ID": {1:'AB', 2:'AC', 3:'DC', 4:'BA',5:'CA',6:'CD',
                          7:'AD',8:'DA',9:'CB',10:'BC',11:'BD',12:'DB'},
 
        "plot_blocks": {'relatin_type':{'Baseline':['AB','AC','DC'],
                        'Symmetry':['BA','CA','CD'],
                     'Equivalence':['BC','CB','BD','DB','AD','DA']}},
                                        
        "plot_blocks_ID": {'relatin_type':['Baseline','Symmetry','Equivalence']},
 
        "mastery_training": 0.9 },
 #----------------------------
 
    9: { # This is the Devany et. al. experiment (1986), by changing the training.
        "num_classes": 2,
        "training_order": {1:[('A1','B1',10)],
                        2:[('B2','A2',10)],
                        3:[('A1','B1',5),('B2','A2',5)],
                        4:[('A1','C1',10)],
                        5:[('C2','A2',10)],
                        6:[('A1','C1',5),('C2','A2',5)],
                        7: [('A1','B1',2),('B2','A2',2),('A1','C1',2),('C2','A2',2)]
                        },
 
        "testing_order": {1:[('A','B',20),('A','C',20),('B','A', 20),('C','A',20),
                             ('B','C',20),('C','B',20)]
                       },
 
        "test_block_ID": {1:'Mixed'},
 
        "plot_blocks": {},
        
        "plot_blocks_ID": {},
        
        "mastery_training": 0.9 }
        }
 
#----------------------------
        
    return environment_parameters_detail