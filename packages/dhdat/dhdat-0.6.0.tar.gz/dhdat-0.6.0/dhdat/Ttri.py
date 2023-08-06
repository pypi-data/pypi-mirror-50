#! usr/bin/python
# -*- coding: utf-8 -*-
"""
| Calculate Ttri class |
by Erik van Haeringen

[ Description ]
Calculates Ttri as described in Shizuka and McDonald (2012), based
on the triad motif count of a dominance network. If option 'mutual' is chosen,
mutual triads are included in the calculation of Ttri. Otherwise Ttri is 
calculated only over triads that have directed edges.
"""

__version__="2019.07.02a"

import pandas as pd

class Ttri():
  d_Ttri = None
  d_triadTypes = None
  d_mutual = False
  
  def __init__(self, mutual): 
    self.d_Ttri = pd.DataFrame(columns=['T_tri'])
    self.d_mutual = mutual
    
    if mutual == True: #also consider triad motifs with mutual relations
      self.d_triadTypes = ['003','012','102','021D','021U','021C','111D',
        '111U','030T','030C','201','120D','120U','120C','210','300']
    else: #only directional relations
      self.d_triadTypes = ['003','012','021D','021U','021C','030T','030C']


  def calculate(self, triadCount, interaction):
    if self.d_mutual:
      self.calculateMutual(triadCount, interaction)
    else:
      self.calculateDirected(triadCount, interaction)


  def calculateDirected(self, triadCount, interaction):
    totalTriads = (triadCount.loc[interaction, 'TRI_030T'] +
      triadCount.loc[interaction, 'TRI_030C'])
    
    if (totalTriads) > 0:
      transitivityWeight = (triadCount.loc[interaction, 'TRI_030T'])
      P_t = transitivityWeight / totalTriads
      self.d_Ttri.loc[interaction, 'T_tri'] = (P_t - 0.75) * 4
    else:
      self.d_Ttri.loc[interaction, 'T_tri'] = None
      
      
  def calculateMutual(self, triadCount, interaction):
    totalTriads = (triadCount.loc[interaction, 'TRI_030T'] + 
      triadCount.loc[interaction, 'TRI_030C'] + 
      triadCount.loc[interaction, 'TRI_120D'] + 
      triadCount.loc[interaction, 'TRI_120U'] + 
      triadCount.loc[interaction, 'TRI_120C'] + 
      triadCount.loc[interaction, 'TRI_210'] + 
      triadCount.loc[interaction, 'TRI_300'])
    
    if (totalTriads) > 0:
      transitivityWeight = (triadCount.loc[interaction, 'TRI_030T'] + 
        triadCount.loc[interaction, 'TRI_120D'] + 
        triadCount.loc[interaction, 'TRI_120U'] + 
        0.5 * triadCount.loc[interaction, 'TRI_120C'] + 
        0.75 * triadCount.loc[interaction, 'TRI_210'] + 
        0.75 * triadCount.loc[interaction, 'TRI_300'])
      P_t = transitivityWeight / totalTriads
      self.d_Ttri.loc[interaction, 'T_tri'] = (P_t - 0.75) * 4
    else:
      self.d_Ttri.loc[interaction, 'T_tri'] = None