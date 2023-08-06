#! usr/bin/python
# -*- coding: utf-8 -*-
"""
| Matrix class |
by Erik van Haeringen

[ Description ]
Builds an interaction matrix based on a list of actors and fills this with rows
from a pandas dataset. These Matrix objects are used by the other modules, for
example to calculate the dominance index Xi.
"""

__version__="2019.01.15a"

import sys
from pathlib import Path
import pandas as pd

class Matrix():
  d_mC = None #matrix cumulative
  d_mNC = None #matrix non-cumulative
  d_pF = None #pair-flip event in last interaction
  
  def __init__(self, actors):
                                        #create empty cumulative matrix
    self.d_mC = pd.DataFrame(index=actors, columns=actors) 
    self.d_mC = self.d_mC.fillna(0)
                                        #create empty non-cumulative matrix
    self.d_mNC = pd.DataFrame(index=actors, columns=actors) 
    self.d_mNC = self.d_mNC.fillna(0)
    
    self.d_pF = pd.DataFrame(columns=(["pairFlip"])) #holds pair-flip results
  
  
  def updateCumulative(self, dataset):
  # Function to fill the interaction matrix with the fight-flee interactions 
  # from the model output data. 
  # Interaction winners are the rows and the losers are the columns.
  
    if (dataset.loc['actor.behavior'] == "Fight") and (
      dataset.loc['receiver.behavior'] == "Flee"):
      self.d_mC.loc[dataset.loc['actor.id'], dataset.loc['receiver.id']] += 1
    
    elif (dataset.loc['receiver.behavior'] == "Fight") and (
      dataset.loc['actor.behavior'] == "Flee"):
      self.d_mC.loc[dataset.loc['receiver.id'], dataset.loc['actor.id']] += 1
    
    else:
      print("Error: line without fight-flee interaction")
      sys.exit()
  
  
  def updateNonCumulative(self, dataset):
  # Function to fill the interaction matrix with the fight-flee interactions 
  # from the model output data. 
  # Interaction winners are the rows and the losers are the columns.

    if (dataset.loc['actor.behavior'] == "Fight") and (
      dataset.loc['receiver.behavior'] == "Flee"):    
        
      #assign the new direction of the interaction
      self.d_mNC.loc[dataset.loc['actor.id'], dataset.loc['receiver.id']] = 1
      self.d_mNC.loc[dataset.loc['receiver.id'], dataset.loc['actor.id']] = 0
      
    elif (dataset.loc['receiver.behavior'] == "Fight") and (
      dataset.loc['actor.behavior'] == "Flee"):
        
      #assign the new direction of the interaction
      self.d_mNC.loc[dataset.loc['actor.id'], dataset.loc['receiver.id']] = 0
      self.d_mNC.loc[dataset.loc['receiver.id'], dataset.loc['actor.id']] = 1
      
    else:
      print("Error: line without fight-flee interaction")
      sys.exit()
      
  
  def exportCumulative(self, outputFileName, run):
  # Function to write cinteraction matrix to tab-delimited csv file
    self.d_mC.to_csv(Path(outputFileName+str(run)+"_matrixC.csv"), sep="\t")
      
    
  def exportNoncumulative(self, outputFileName, run):
  # Function to write interaction matrix to tab-delimited csv file
    self.d_mNC.to_csv(Path(outputFileName+str(run)+"_matrixNC.csv"), sep="\t")