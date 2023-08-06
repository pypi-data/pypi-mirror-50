#! usr/bin/python
# -*- coding: utf-8 -*-
"""
| Combination Maker class |
by Erik van Haeringen

[ Description ] 
Class that uses a recursive function to generate all possible triangles based 
on a set of actors, and stores these combinations in a pandas dataframe.
The recursive algorithm was inspired on a code (in C) submitted by Bateesh to
https://www.geeksforgeeks.org/print-all-possible-combinations-of-r-elements-in-
a-given-array-of-size-n/
"""

__version__="2019.01.12a"

import pandas as pd

class CombinationMaker():
  d_combinations = None             #total number of combinations
  d_counter = 0                     
  
  def __init__(self, actors, r):
    n = len(actors)
                                    #calculate total number of triads
    self.d_combinations = round((1 / 6) * n * (n - 1) * (n - 2)) 
                                    #empty dataframe to hold combinations
    self.d_result = pd.DataFrame(index = range(self.d_combinations), 
      columns = range(r)) 
      
    tempData = [None] * 3           #holds combinations during recursion
                                    #calculate combinations
    self.combinationUtil(actors, tempData, 0, n - 1, 0, r)
    
    
  def combinationUtil(self, arr, data, start, end, index, r):
    if (index == r):                #if complete then add to result
      #print("data:",data)          #uncomment to show the found combination
      self.d_result.loc[self.d_counter,:] = data
      self.d_counter += 1
      return
  
      #replaces index with all possible elements
      #the condition "end - i + 1 >= r - index" makes sure that including 
      #one element at index will make a combination with remaining 
      #elements at remaining positions
    i = start
    while (i <= end) & (end - i + 1 >= r - index): 
      data[index] = arr[i]
      self.combinationUtil(arr, data, i + 1, end, index + 1, r)
      i += 1
     
      
  def getResults(self): #returns pandas data object with all combinations
    return self.d_result 