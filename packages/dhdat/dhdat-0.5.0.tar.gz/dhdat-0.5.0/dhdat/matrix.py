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

__version__="2019.08.13a"

import sys
from pathlib import Path
import pandas as pd

class Matrix():
  d_mC = None #matrix cumulative
  d_mNC = None #matrix non-cumulative
  d_mI = None
  
  def __init__(self, actors):
    self.d_mI = pd.DataFrame(index=actors, columns=actors) 
    self.d_mI = self.d_mI.fillna(0)
    
    self.d_mC = pd.DataFrame(index=actors, columns=actors) 
    self.d_mC = self.d_mC.fillna(0)
    
    self.d_mNC = pd.DataFrame(index=actors, columns=actors) 
    self.d_mNC = self.d_mNC.fillna(0)
    
  
  def update(self, dataset):
    # Function to update all the interaction matrices from a row of a Pandas 
    # DataFrame. This row  must at least contain the columns: 'actor.id' &
    # 'receiver.id' (indicating who initiated the fight against who), and 
    # 'actor.behaviour' & 'receiver.behaviour', indicating the fight's outcome
      self.updateCumulative(dataset)
      self.updateNonCumulative(dataset)
      self.updateInitiated(dataset)
      
    
  def updateInitiated(self, dataRow):
  # matrix with the initations of aggression. The rows are the initiators and 
  # the columns are the receivers.
      self.d_mI.loc[dataRow.loc['actor.id'], dataRow.loc['receiver.id']] += 1
      
    
  def updateCumulative(self, dataRow):
  # cumulative interaction matrix with the outcomes of the fights. Interaction 
  # winners are the rows and the losers are the columns.
  
    if (dataRow.loc['actor.behavior'] == "Fight") and (
      dataRow.loc['receiver.behavior'] == "Flee"):
      self.d_mC.loc[dataRow.loc['actor.id'], dataRow.loc['receiver.id']] += 1
    
    elif (dataRow.loc['receiver.behavior'] == "Fight") and (
      dataRow.loc['actor.behavior'] == "Flee"):
      self.d_mC.loc[dataRow.loc['receiver.id'], dataRow.loc['actor.id']] += 1
    
    else:
      raise ValueError("Row without fight-flee interaction")
      sys.exit()
  
  
  def updateNonCumulative(self, dataRow):
  # non-cumulative interaction matrix with the outcomes of the fights. 
  # Interaction winners are the rows and the losers are the columns.

    if (dataRow.loc['actor.behavior'] == "Fight") and (
      dataRow.loc['receiver.behavior'] == "Flee"):    
        
      #assign the new direction of the interaction
      self.d_mNC.loc[dataRow.loc['actor.id'], dataRow.loc['receiver.id']] = 1
      self.d_mNC.loc[dataRow.loc['receiver.id'], dataRow.loc['actor.id']] = 0
      
    elif (dataRow.loc['receiver.behavior'] == "Fight") and (
      dataRow.loc['actor.behavior'] == "Flee"):
        
      #assign the new direction of the interaction
      self.d_mNC.loc[dataRow.loc['actor.id'], dataRow.loc['receiver.id']] = 0
      self.d_mNC.loc[dataRow.loc['receiver.id'], dataRow.loc['actor.id']] = 1
      
    else:
      raise ValueError("Row without fight-flee interaction")


  def exportInitiated(self, outputFileName, run):
  # Function to write cinteraction matrix to tab-delimited csv file
    self.d_mI.to_csv(Path(outputFileName +"_I_run" + str(run)+".csv"), sep="\t")      
  
  
  def exportCumulative(self, outputFileName, run):
  # Function to write cinteraction matrix to tab-delimited csv file
    self.d_mC.to_csv(Path(outputFileName +"_C_run" + str(run)+".csv"), sep="\t")
    
    
  def exportNoncumulative(self, outputFileName, run):
  # Function to write interaction matrix to tab-delimited csv file
    self.d_mNC.to_csv(Path(outputFileName +"_NC_run" + str(run)+".csv"), sep="\t")