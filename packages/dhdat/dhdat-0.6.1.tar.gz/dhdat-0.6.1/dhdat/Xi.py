#! usr/bin/python
# -*- coding: utf-8 -*-
"""
| Xi Dominance Index class |
by Erik van Haeringen

[ Description ] 
Calculates the dominance index Xi, which is the proportion of aggressive 
interaction won, for a cumulative interaction matrix as described in Lindquist 
and Chase (2009)
"""

__version__="2019.01.15a"

import pandas as pd

class Xi():
  d_Xi = None
  d_actors = None
  
  def __init__(self, actors):
    self.d_actors = actors
    self.d_Xi = pd.DataFrame(columns=("Xi_" + str(s) for s in self.d_actors))
  
  
  def calculate(self, matrix, interaction):     
    for i in self.d_actors:
      win = matrix.loc[i, :].sum() #sum individual's wins
      lose = matrix.loc[:, i].sum() #sum individual's losses
      
      if (win + lose) > 0: #if individual interacted at least once
        self.d_Xi.loc[interaction, "Xi_" + str(i)] = win / (win + lose) #store