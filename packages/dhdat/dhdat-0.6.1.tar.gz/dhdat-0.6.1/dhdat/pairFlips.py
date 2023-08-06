#! usr/bin/python
# -*- coding: utf-8 -*-
"""
| PairFlips class |
by Erik van Haeringen

[ Description ] 
Detects pair-flip events, which is the reversal of the relationship of pair 
based on a non-cumulative interaction matrix. This means that one counter 
attack is enough to reverse the relation and be marked as a pair-flip event. 
To detect these events the direction of the relation of the pair involved in 
the current interaction, is compared to the non-cumulative interaction matrix 
of the previous interaction.
"""

__version__="2019.03.27a"

import pandas as pd

class PairFlips():
  d_pairFlips = None
  
  def __init__(self):
    self.d_pairFlips = pd.DataFrame(columns=['pairFlip'])
  
  
  def detect(self, matrix, row, interaction):
    self.d_pairFlips.loc[interaction, "pairFlip"] = False

    if (row.loc['actor.behavior'] == "Fight") and (
      row.loc['receiver.behavior'] == "Flee"):
           
                                      #check if there is a pairflip event
      if (matrix.loc[row.loc['actor.id'], row.loc['receiver.id']] == 0) and (
        matrix.loc[row.loc['receiver.id'], row.loc['actor.id']] == 1):
        self.d_pairFlips.loc[interaction, "pairFlip"] = True
    
    
    elif (row.loc['receiver.behavior'] == "Fight") and (
          row.loc['actor.behavior'] == "Flee"):
            
                                      #check if there is a pairflip event
      if (matrix.loc[row.loc['actor.id'], row.loc['receiver.id']] == 1) and (
        matrix.loc[row.loc['receiver.id'], row.loc['actor.id']] == 0):
        self.d_pairFlips.loc[interaction, "pairFlip"] = True
        