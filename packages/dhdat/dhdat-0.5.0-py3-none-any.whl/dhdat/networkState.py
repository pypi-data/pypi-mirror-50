#! usr/bin/python
# -*- coding: utf-8 -*-
"""
| Network State class |
by Erik van Haeringen

[ Description ] 
Determines the state of a network of 4 individuals based on triad motif count. 
See Lindquist and Chase (2009) for an explanation of triad motifs network 
states and nomenclature. Currently only networks of 4 individuals are 
supported. Increasing the group size results in an exponential growth of 
possible network states, and thus quickly becomes unfeasible.
"""

__version__="2019.01.15a"

import pandas as pd

class NetworkState():
  d_state = None
  d_stateDictionary = None
  d_actors = None
  
  def __init__(self, actors):
    self.d_actors = actors
    self.d_state = pd.DataFrame(columns=['State']) #holds determined states
    self.buildStateDictionary()
  
  
  def determine(self, triadState, interaction, matrix):
    triadState.sort(reverse=True) #sort the triad types from high to low
    self.d_state.loc[interaction, 'State'] = self.d_stateDictionary[
      ''.join(str(triad) for triad in triadState)] #get state from triad set    
    
#   [ solve cases where triad set alone could not fully determine the state ]
    if self.d_state.loc[interaction, 'State'] == "18and20":
      #if the individual with 1 edge wins, then state 20, else state 18
      for i in self.d_actors:
        win = matrix.loc[i, :].sum() #sum individual's wins
        lose = matrix.loc[:, i].sum() #sum individual's losses
        
        if (win == 0) and (lose == 1):
          self.d_state.loc[interaction,'State'] = '18'
          break
        if (win == 1) and (lose == 0):
          self.d_state.loc[interaction,'State'] = '20'
          break
    
    if self.d_state.loc[interaction, 'State'] == "25and26":
      #if most dominant individual (dom, 2 wins) won from the the least 
      #dominant (sub, 0 wins), then state 26
      #if there is no interaction between dom and sub, then state 25
      dom = None
      sub = None
      for i in self.d_actors:
        win = matrix.loc[i, :].sum() #sum individual's wins
        if win == 2:
          dom = i
        if win == 0:
          sub = i
      if matrix.loc[dom,sub] == 0:
        self.d_state.loc[interaction, 'State'] = '25'
      else:
        self.d_state.loc[interaction, 'State'] = '26'
    
    if self.d_state.loc[interaction, 'State'] == "39and40":
      #if 1 indvidual dominant over all others, then state 39, else state 40
      for i in self.d_actors:
        win = matrix.loc[i, :].sum() #sum individual's wins
        lose = matrix.loc[:, i].sum() #sum individual's losses
        
        if (win == 3) and (lose == 0):
          self.d_state.loc[interaction, 'State'] = "39"
          break
        else:
          self.d_state.loc[interaction, 'State'] = "40"
          
          
  def buildStateDictionary(self):
    self.d_stateDictionary = {
      #0 edges
      '1111':'0',
      #1 edges
      '2211':'1',
      #2 edges
      '3221':'2','5221':'3','4221':'4','2222':'5',
      #3 edges
      '3331':'6','5531':'7','5541':'8','4441':'9','6222':'10',
      '7222':'11','4322':'12','5422':'13','5322':'14','5522':'15',
      #4 edges
      '6332':'16','6532':'17','6552':'18and20','7532':'19','6542':'21',
      '6442':'22','7542':'23','4433':'24','5543':'25and26','5555':'27',
      #5 edges
      '6633':'28','6653':'29','6643':'30','6655':'31','6654':'32',
      '6644':'33','7653':'34','7655':'35','7743':'36','7654':'37',
      #6 edges
      '6666':'38','7666':'39and40','7766':'41'   
    }
    