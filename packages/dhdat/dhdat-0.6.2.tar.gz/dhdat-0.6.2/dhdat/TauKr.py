# -*- coding: utf-8 -*-
"""
| TauKr class |
by Erik van Haeringen

Description: calculates TauKr as defined in Hemelrijk (1989), which measures
unidirectionality between a set of matrices.
"""

__version__="2019.08.13a"

import pandas as pd
import numpy as np
import math

class TauKr():
  d_TauKr = None
  
  
  def __init__(self):
    self.d_TauKr = pd.DataFrame(columns=['TauKr']) #holds calculated Kr score
  
  
  def remove_diag(self, matrix):
    matrix = matrix.astype(float)       #NA values only possible with floats
    np.fill_diagonal(matrix.values, np.nan)
    return matrix
    
  
  def calculate(self, interaction, matrix1, matrix2):
  # function to calculate TauKr from 2 matrices
  
    matrix1 = self.remove_diag(matrix1) #set diagonal to NA
    matrix1 = self.remove_diag(matrix2)
                                        #remove NA values by shifting left
    matrix1 = matrix1.T.apply(lambda x: pd.Series(x.dropna().values)).T 
    matrix2 = matrix2.T.apply(lambda x: pd.Series(x.dropna().values)).T

    self.worker(interaction, matrix1, matrix2)
    
    
  def calculate_T(self, interaction, matrix):
  # function to calculate TauKr from a single matrix compared to the same
  # matrix transposed
    
    matrix = self.remove_diag(matrix)   #set diagonal to NA
                                        #remove NA values by shifting left
    matrix_T = matrix.apply(lambda x: pd.Series(x.dropna().values)).T
    matrix_R = matrix.T.apply(lambda x: pd.Series(x.dropna().values)).T

    self.worker(interaction, matrix_R, matrix_T)


  def calc_tie(self, x): 
    return x * (x - 1)


  def worker(self, interaction, matrix1, matrix2):
    C = matrix1.shape[1]                #number of columns
    R = matrix1.shape[0]                #number of rows

    Kr = 0                              #numerator
    H = 0                               #denominator
    
    #calculates the numerator and denominator per row, and adds these to Kr and H
    for r in range(R):
      k = C - 1                         #number of combinations first focal item
      
                                        #correction ties per matrix according to:
                                        #T = 0.5 * Sum of [Th(Th - 1)]
      T = 0.5 * matrix1.iloc[r,:].value_counts().apply(lambda x: self.calc_tie(x)).sum()
      U = 0.5 * matrix2.iloc[r,:].value_counts().apply(lambda x: self.calc_tie(x)).sum()

      P = 0                             #concordant pairs
      Q = 0                             #discordant pairs
      
      for focal in range(C):
        for partner in range(1, k + 1):
                                        #if pair direction is equal between matrices
          if (                          
              ((matrix1.iloc[r, focal] - matrix1.iloc[r, focal + partner]) < 0 and 
               (matrix2.iloc[r, focal] - matrix2.iloc[r, focal + partner]) < 0
              ) or (
               (matrix1.iloc[r, focal] - matrix1.iloc[r, focal + partner]) > 0 and 
               (matrix2.iloc[r, focal] - matrix2.iloc[r, focal + partner]) > 0)):
            P += 1
                                        #if pair direction is equal between matrices
          elif (                        
              ((matrix1.iloc[r, focal] - matrix1.iloc[r, focal + partner]) < 0 and 
               (matrix2.iloc[r, focal] - matrix2.iloc[r, focal + partner]) > 0
              ) or (
               (matrix1.iloc[r, focal] - matrix1.iloc[r, focal + partner]) > 0 and 
               (matrix2.iloc[r, focal] - matrix2.iloc[r, focal + partner]) < 0)):
            Q += 1
        k -= 1
        
      Kr = Kr + (P - Q)
      H = H + math.sqrt(0.5 * C * (C-1) - T) * math.sqrt(0.5 * (C) * (C-1) - U)      
      
    if (H != 0):
      self.d_TauKr.loc[interaction,'TauKr'] = Kr / H
    