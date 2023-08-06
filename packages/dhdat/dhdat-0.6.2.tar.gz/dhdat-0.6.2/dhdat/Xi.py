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

__version__="2019.08.14a"

import pandas as pd

class Xi():
  d_Xi = None
  d_actors = None
  
  def __init__(self, actors):
    self.d_actors = actors
    self.d_Xi = pd.DataFrame(columns=["Xi_" + str(s) for s in self.d_actors])
  
  def calculate(self, matrix, interaction): 
    result = matrix.sum(axis = 1) / (matrix.sum(axis = 1) + matrix.transpose().sum(axis = 1))
    self.d_Xi.loc[interaction,:] = result.values #store result