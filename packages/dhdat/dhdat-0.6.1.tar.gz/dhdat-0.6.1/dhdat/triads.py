#! usr/bin/python
# -*- coding: utf-8 -*-
"""
| Count Triads class |
by Erik van Haeringen

[ Description ] 
Counts triad motifs in a dominance network read from an interaction matrix. 
See Wasserman & Faust (1994), or Shizuka & McDonald (2012) for details on
triad coding. This class can count either triad motifs with only directed 
relationships, in which case mutual (equal) relationships are ignored. Or it 
can also count triad motifs that contain one or more mutual relationships.
"""

__version__="2019.01.12a"

import pandas as pd

class Triads():
  d_combinations = 0
  d_triadCount = None #holds counts of triad motifs in network
  d_triadState = [] #stores network state described as collection of 4 triads
  d_triadTypes = None #names for triad motifs
  d_triadDictionairy = None #converts edges to triad
  d_triadNumberDictionairy = None #converts triad census code to single number
  
  
  def __init__(self, mutual, combinations):                                  
    self.d_combinations = combinations #store triad combinations 
    self.buildTriadDictionairy() #translates edge count to triad motif
    self.buildTriadNumberDictionairy() #codes triad to single number
    
    if mutual == True: #also consider triad motifs with mutual relations
      self.d_triadTypes = ['003','012','102','021D','021U','021C','111D',
        '111U','030T','030C','201','120D','120U','120C','210','300']
    else: #only directional relations
      self.d_triadTypes = ['003','012','021D','021U','021C','030T','030C']
      
    self.d_triadCount = pd.DataFrame(
      columns=["TRI_" + str(s) for s in self.d_triadTypes]) #holds triad count
      
  
  def count(self, matrix, interaction):       
    self.d_triadState = []

    self.d_triadCount.loc[interaction, :] = 0 #set all counts to zero

    for index, triadNodes in self.d_combinations.iterrows():   
      triadEdges = [0, 0, 0]
                              #code relation of each edge in a triad    
                              #0 if node 0 has won more from node 1 than v.v.
                              #1 if node 1 has won more from node 0 than v.v.
                              #2 if equal and more than 0 wins
                              #3 if both no wins
      triadEdges[0] = (
        0 if (matrix.loc[triadNodes[0], triadNodes[1]] - 
          matrix.loc[triadNodes[1], triadNodes[0]]) < 0 
        else 1 if (matrix.loc[triadNodes[0], triadNodes[1]] - 
          matrix.loc[triadNodes[1], triadNodes[0]]) > 0 
        else 2 if matrix.loc[triadNodes[0], triadNodes[1]] > 0 
        else 3)                     
        
      triadEdges[1] = (
        0 if (matrix.loc[triadNodes[0], triadNodes[2]] - 
          matrix.loc[triadNodes[2], triadNodes[0]]) < 0 
        else 1 if (matrix.loc[triadNodes[0], triadNodes[2]] - 
          matrix.loc[triadNodes[2], triadNodes[0]]) > 0 
        else 2 if matrix.loc[triadNodes[0], triadNodes[2]] > 0 
        else 3)
        
      triadEdges[2] = (
        0 if (matrix.loc[triadNodes[1], triadNodes[2]] - 
          matrix.loc[triadNodes[2], triadNodes[1]]) < 0 
        else 1 if (matrix.loc[triadNodes[1], triadNodes[2]] - 
          matrix.loc[triadNodes[2], triadNodes[1]]) > 0 
        else 2 if matrix.loc[triadNodes[1], triadNodes[2]] > 0 
        else 3)

      result = self.d_triadDictionairy[''.join(str(dyad) for dyad in 
        triadEdges)] #get triad type from edge combination in dictionairy

                              #increment triad type count
      if result in self.d_triadTypes:
        self.d_triadCount.loc[interaction, "TRI_" + result] += 1 
                              #store triad set with triads as single numbers
      self.d_triadState.append(self.d_triadNumberDictionairy[result])
      
  
  def buildTriadDictionairy(self):
    # Triad census including mutual relations.
    # See book Wasserman & Faust (1994) for details on triad coding.
    # 64 possible combinations of 4 values in 3 positions with 
    # repetitions and ordered.
    self.d_triadDictionairy = {       
      #1) 003
      '333': '003',
      #2) 012
      '133': '012','313': '012','331': '012','033': '012','303': '012',
      '330': '012',         
      #3) 102
      '233': '102','323': '102','332': '102',    
      #4) 021D
      '113': '021D','031': '021D','300': '021D',     
      #5) 021U
      '311': '021U','130': '021U','003': '021U',
      #6) 021C
      '131': '021C','301': '021C','103': '021C','030': '021C','310': '021C',
      '013': '021C',
      #7) 111D
      '321': '111D','023': '111D','203': '111D','230': '111D','312': '111D',
      '132': '111D',
      #8) 111U
      '320': '111U','123': '111U','213': '111U','231': '111U','302': '111U',
      '032': '111U',
      #9) 030T
      '111': '030T','110': '030T','100': '030T','011': '030T','001': '030T',
      '000': '030T',
      #10) 030C
      '010': '030C','101': '030C',
      #11) 201
      '223': '201','322': '201','232': '201',
      #12) 120D
      '021': '120D','200': '120D','112': '120D',
      #13) 120U
      '120': '120U','211': '120U','002': '120U',
      #14) 120C
      '121': '120C','201': '120C','102': '120C','020': '120C','210': '120C',
      '012': '120C',
      #15) 210
      '122': '210','221': '210','202': '210','022': '210','220': '210',
      '212': '210',
      #16) 300
      '222': '300'
    }
  
  
  def buildTriadNumberDictionairy(self):
    self.d_triadNumberDictionairy = {
      #non-mutual triads
      '003':1,'012':2,'021D':3,'021U':4,'021C':5,'030T':6,'030C':7,
      #mutual triads
      '102':8,'111D':9,'111U':10,'201':11,'120D':12,'120U':13,'120C':14,
      '210':15,'300':16
    }
