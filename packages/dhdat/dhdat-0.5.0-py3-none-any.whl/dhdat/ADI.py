#! usr/bin/python
# -*- coding: utf-8 -*-
"""
| Average Dominance Index (ADI) class |
by Erik van Haeringen

[ Description ] 
Calculates the average dominance index (ADI) from an cumulative interaction 
matrix as described in Hemelrijk et al. (2005).
"""

__version__="2019.01.15a"

import pandas as pd

class ADI():
  d_ADI = None
  d_actors = None
  
  def __init__(self, actors):
    self.d_actors = actors
    self.d_ADI = pd.DataFrame(columns=("ADI_" + str(s) for s in self.d_actors))
  
  
  def calculate(self, matrix, interaction):   
#   [ STEP 1 ]
#   calculate for each individual relation the relative wins devided by total 
#   interactions
                                          #holds results of the first step
    temp = pd.DataFrame(index = self.d_actors, columns = self.d_actors) 
  
    for i in self.d_actors:
      for j in self.d_actors:
        if matrix.loc[i, j] > 0 or matrix.loc[j, i] > 0:
          temp.loc[i, j] = matrix.loc[i, j] / (matrix.loc[i, j] + 
            matrix.loc[j, i])
    #print(temp) uncomment to see interaction table of step 1

#   [ STEP 2 ]
#   calculate the average relative wins for each individual over all 
#   interactions by taking the average of the row 
    for index, actor in temp.iterrows():
      self.d_ADI.loc[interaction,"ADI_" + str(index)] = actor.mean(skipna=True) 
