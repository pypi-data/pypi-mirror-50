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
  
  
  def detect(self, rowNew, rowOld, interaction):
    self.d_bursts.loc[interaction, 'burst'] = (
        (rowNew.loc['actor.id'] == rowOld.loc['actor.id']) & 
        (rowNew.loc['receiver.id'] == rowOld.loc['receiver.id']) &
        (rowNew.loc['actor.behavior'] == rowOld.loc['actor.behavior'])
    ) or (
        (rowNew.loc['actor.id'] == rowOld.loc['receiver.id']) & 
        (rowNew.loc['receiver.id'] == rowOld.loc['actor.id']) &
        (rowNew.loc['actor.behavior'] == rowOld.loc['receiver.behavior'])
    )