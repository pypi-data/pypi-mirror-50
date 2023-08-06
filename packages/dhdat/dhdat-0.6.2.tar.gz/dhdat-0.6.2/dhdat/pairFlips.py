#! usr/bin/python
# -*- coding: utf-8 -*-
"""
| PairFlip class |
by Erik van Haeringen

[ Description ] 
Detects pair-flip events, which is the reversal of the relationship of pair 
based on a non-cumulative interaction matrix. This means that one counter 
attack is enough to reverse the relation and be marked as a pair-flip event. 
To detect these events the direction of the relation of the pair involved in 
the current interaction, is compared to the non-cumulative interaction matrix 
of the previous interaction.
"""

__version__="2019.08.15a"

import pandas as pd

class PairFlips():
  d_pairFlips = None
  
  def __init__(self):
    self.d_pairFlips = pd.DataFrame(columns=['pairFlip'])
  
  
  def detect(self, matrix, dataRow, interaction):
#   1: actor wins, -1: receiver wins, 0: neither wins
    directionCurrent = (
          (dataRow.loc['actor.behavior'] == "Fight") - 
          (dataRow.loc['receiver.behavior'] == "Fight")
        )
    if not directionCurrent:
      raise ValueError("Row without fight-flee interaction")
    
#   1: actor won, -1: receiver won, 0: no previous interaction involving pair
    directionPrevious = (
          matrix.loc[dataRow.loc['actor.id'], dataRow.loc['receiver.id']] - 
          matrix.loc[dataRow.loc['receiver.id'], dataRow.loc['actor.id']]
        )
    
#   if previous interaction between pair and direction differs from curent
    self.d_pairFlips.loc[interaction, "pairFlip"] = (
          (directionCurrent != directionPrevious) & 
          (directionPrevious != 0)
        )
