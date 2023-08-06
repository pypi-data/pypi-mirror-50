#! usr/bin/python
# -*- coding: utf-8 -*-
"""
| Bursts class |
by Erik van Haeringen

[ Description ] 
Detects whether bursting occurs, a pattern of repeated consecutive attacks in 
the same direction within a dyad, as described by Lindquist and Chase (2009).
It does this by comparing the current interaction with the previous 
interaction.
"""

__version__="2019.01.15a"

import pandas as pd

class Bursts():
  d_bursts = None
  
  def __init__(self):
    self.d_bursts = pd.DataFrame(columns=['burst'])
  
  
  def detect(self, dataRowNew, dataRowOld, interaction):
    newWinnerId = newLoserId = oldWinnerId = oldLoserId = None
    
#   determine involved actors of previous and current interaction
    if (dataRowNew.loc['actor.behavior'] == "Fight") and (
        dataRowNew.loc['receiver.behavior'] == "Flee"):
      newWinnerId = dataRowNew.loc['actor.id']
      newLoserId = dataRowNew.loc['receiver.id']
    elif (dataRowNew.loc['actor.behavior'] == "Flee") and (
        dataRowNew.loc['receiver.behavior'] == "Fight"):
      newWinnerId = dataRowNew.loc['receiver.id']
      newLoserId = dataRowNew.loc['actor.id']
    if (dataRowOld.loc['actor.behavior'] == "Fight") and (
        dataRowOld.loc['receiver.behavior'] == "Flee"):
      oldWinnerId = dataRowOld.loc['actor.id']
      oldLoserId = dataRowOld.loc['receiver.id']
    elif (dataRowOld.loc['actor.behavior'] == "Flee") and (
        dataRowOld.loc['receiver.behavior'] == "Fight"):
      oldWinnerId = dataRowOld.loc['receiver.id']
      oldLoserId = dataRowOld.loc['actor.id']
    
#   if same winner and loser as previous interaction: burst occurs
    if (oldWinnerId == newWinnerId) and (oldLoserId == newLoserId):
      self.d_bursts.loc[interaction, 'burst'] = True
    else:
      self.d_bursts.loc[interaction, 'burst'] = False