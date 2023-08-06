# Dominance Hierarchy Development Analysis Tools (DHDAT)
<table style="text-align:left">
<tr><th>Author</th><th>Erik van Haeringen</th></tr>
<tr><th>Email</th><th>e.s.van.haeringen@student.rug.nl</th></tr>
<tr><th>Date</th><th>July 4th 2019</th></tr>
<tr><th>Description</th><th>DHDAT is a python package with basic tools to produce interaction matrices and calculate several dominance hierarchy related metrics</th></tr>
</table>

## Licence
Copyright (C) 2019, van Haeringen. This package is published under an MIT licence and you are welcome to use or improve upon it. For any publication, whether research or software that uses or includes (partial) copies of (modules of) this package, please cite this work.

## Prerequisites
* [Python 3](https://www.python.org/)
* [Pandas](https://pandas.pydata.org/)

## Install
To install the package for your default Python installation use your terminal to execute the command below.

```
pip install dhdat
```

For other Python installations replace `pip` with the path to its respective pip executable

## Contents
1. [Matrix](#1-matrix)
2. [CombinationMaker](#2-combinationmaker)
3. [Triads](#3-triads)
4. [Ttri](#4-ttri)
5. [NetworkState](#5-networkstate)
6. [ADI](#6-adi)
7. [Xi](#7-xi)
8. [Bursts](#8-bursts)
9. [PairFlips](#9-pairflips)
10. [TauKr](#10-taukr)

## Modules
### 1. Matrix
#### Description
Builds an interaction matrix based on a list of actors and fills this with rows from a pandas dataset.
These Matrix objects are used by the other modules, for example to calculate the dominance index Xi.
Interaction winners are the rows and the losers are the columns.

#### How to use
Create a new matrix object by initiating matrix with a list of the actors identifiers.
This matrix object contains two Pandas DataFrames, one for a cumulative matrix (**d_mC**), a another for a non-cumulative matrix (**d_mNC**).

```python
from dhdat import Matrix

actorIDs = [1,2,3,4]
matrix = Matrix(actorIDs)       #new interaction matrix of size len(actorIDs)

print(matrix.d_mC)              #shows cumulative matrix
print(matrix.d_mNC)             #shows non-cumulative matrix
```

The matrix can be filled with rows from a Pandas DataFrame. This DataFrame should be structured with one row per interaction, containing at least the columns **'actor.id'**, **'actor.behavior'**, **'receiver.id'** and **'receiver.behavior'**.
The **'actor.id'** and **'receiver.id'** columns should contain one of the actorIDs provided to the matrix object on initialization. The **'actor.behavior'** and **'receiver.behavior'** columns should contian either the string "Fight" or "Flee".
Thus actor might be the one who initialized the interaction but can lose the interaction and flee. The Pandas DataFrame should look similar to the example below.

```python
import pandas as pd
                                    #load data from csv file
df = pd.read_csv("exampleDataSet.csv", delimiter="\t")

print(df)
```

Example data set:
```
     time   actor.id   receiver.id   actor.behavior   receiver.behavior
0      23          4             2            Fight                Flee
1     112          2             3             Flee               Fight
2     278          1             3            Fight                Flee
3     315          4             2            Fight                Flee
```

Interactions can be added to the matrix by calling either the cumulative or non-cumulative update function and inserting a row of the DataFrame (= one interaction).
See the example below for a simple for-based loop adding all interactions in the DataFrame *df*.

```python
for interaction in df.index:
                                    #add new interaction to non-cumulative matrix
    matrix.updateNonCumulative(df.loc[interaction,:])

                                    #add new interaction to cumulative matrix
    matrix.updateCumulative(df.loc[interaction,:])

print(matrix.d_mC)                  #shows cumulative matrix
```

Output:
```
   1  2  3  4
1     0  1  0
2  0     0  0
3  0  1     0
4  0  2  0  
```

The dataframes containing the matrices and pair-flips can directly be accessed as shown in the first example.
There are also the functions **exportCumulative** and **exportNonCumulative** that store the respective matrix as a tab-separated csv file.
The functions arguments are *filename* and *run_number*.
This results in the following filename structure: *[filename][run_number]_matrixC.csv*

```python
                                    #produces 'test_5_matrixNC.csv'
matrix.exportNonCumulative("test_", 5)

                                    #produces 'test2_13_matrixC.csv' in subdirectory 'figures'
matrix.exportCumulative("figures/test2_", 14)
```

-----------------------
### 2. CombinationMaker
#### Description
Class that uses a recursive function to generate all possible triangles based on a set of actors, and stores these combinations in a pandas dataframe.
The recursive algorithm was inspired on a example (in C) by [Bateesh](https://www.geeksforgeeks.org/print-all-possible-combinations-of-r-elements-in-a-given-array-of-size-n/).

#### How to use

A combination object is initialized with a list of the elements (actors) that will be combined, and the number of elements per combination. Below is an example for all combinations of three individuals that can be made with four individuals.

```python
from dhdat import CombinationMaker

actorIDs = [1, 2, 3, 4]
                                    #calculate all triad combinations of 4 actors
combinations = CombinationMaker(actorIDs, 3)
```

The combinations are stored in a Pandas DataFrame **d_result**.
This member can be accessed directly, or alternatively the function **getResults** returns this member.

```python
combinations.getResults()
```
Output:
```
   0  1  2
0  1  2  3
1  1  2  4
2  1  3  4
3  2  3  4
```

-----------------------
### 3. Triads
#### Description
Counts triad motifs in a dominance network read from an interaction matrix.
See Wasserman & Faust (1994), or Shizuka & McDonald (2012) for details on triad coding.
This class can count either triad motifs with only directed relationships, in which case mutual (equal) relationships are ignored.
Or it can also count triad motifs that contain one or more mutual relationships.

#### How to use
Triads is initialized with the option for mutual triad motif count (False or True) and a [CombinationMaker](#2-combinationmaker) object containing all possible combinations of actors for triads.

```python
from dhdat import Triads

triads = Triads(False, combinations)
```

A Triads object counts triads with the function **count**, which requires either a cumulative or non-cumulative [matrix](#1-matrix) and the index of the current interaction.
The resulting motif count is stored in a Pandas DataFrame **d_triadCount** at the index supplied to the **count** function.

```python
triads.count(matrix.d_mNC, interaction)

                                    #shows triad count of interaction  
print(triads.d_triadCount.loc[interaction, :])
```

Output:

```
    TRI_003   TRI_012   TRI_021D   TRI_021U   TRI_021C   TRI_030T   TRI_030C
0         0         2          0          1          1          0          0
```

-----------------------
### 4. Ttri
#### Description
Calculates T<sub>tri</sub> as described in Shizuka and McDonald (2012), based on the triad motif count of a dominance network.
If option 'mutual' is chosen, mutual triads are included in the calculation of T<sub>tri</sub>.
Otherwise T<sub>tri</sub> is calculated only over triads that have directed edges.

#### How to use
To calculate T<sub>tri</sub> first a Ttri object must be initialized with the option for triad count of mutual relations (True or False).
This option should correspond to the option chosen to [count](#3-triads) the triad motifs. Because triad count can be either over a cumulative matrix or a non-cumulative matrix, the T<sub>tri</sub> value either measures linearity over the last interaction in each pair (non-cumulative), or includes all previous interactions in each pair (cumulative) to determine the direction of a pair relation. In the paper cited above by Shizuka and McDonald, T<sub>tri</sub> is calculated over the final cumulative interaction matrix including all recorded interactions.

```python
from dhdat import Ttri

ttri = Ttri(False)
```

Then the Ttri object can be fed with the triad count from a [Triads](#3-triads) object, and the index of the current interaction.
Ttri is stored in a Pandas DataFrame d_ttri with one column *'T_tri'*, which can be accessed directly.
Ttri can by definition only be determined when there is at least one complete triad (containing 3 links).
Thus the [example data set](#1-matrix) used in this manual results in no value for *'T_tri'* as there are no complete triads, as was shown in the demonstration of the previous module [Triads](#3-triads).

```python
ttri.calculate(triads.d_triadCount, interaction)

                                    #shows the Ttri value for interaction
print(ttri.d_ttri.loc[interaction, :])
```

Output:
```
   T_tri
0      
```
T<sub>tri</sub> in a directed (non-mutual) network is a scaled ratio of transitive triad motifs divided by the transitive + cyclic triad motifs. In a mutual network it uses the ratio of transitive weights divided by the total number of complete triad motifs, as some mutual triad motifs are defined as partially transitive. This measure ignores motifs with missing links (also called relations or edges). In example given here of T<sub>tri</sub> calculated for a directed network, there are no complete motifs (either transitive, cyclic), which results in a empty field. See Shizuka and McDonald (2012) for further details.

-----------------------
### 5. NetworkState
#### Description
Determines the state of a network of 4 individuals based on triad motif count.
See Lindquist and Chase (2009) for an explanation of triad motifs network
states and nomenclature. Currently only networks of 4 individuals are supported.
Increasing the group size results in an exponential growth of possible network states, and thus quickly becomes unfeasible.

#### How to use
A NetworkState object is created with a list of the actors.
To determine the network state of an interaction matrix, member function **determine** requires the triad state count **d_triadState** of a [Triads](#3-triads) object, and the number of the current interaction as an index to store the result.
Because for some states triads motif count alone is not enough to determine the network state, additionally the non-cumulative matrix **d_mNC** of a [Matrix](#1-matrix) object is a required argument.
States are stored in data member **d_state** as a Pandas DataFrame and can be accessed directly.

```python
from dhdat import NetworkState

actorIDs = [1, 2, 3, 4]
state = NetworkState(actorIDs)      #make a new NetworkState object

                                    #determine NetworkState of interaction
state.determine(triads.d_triadState, interaction, matrix.d_mNC)

                                    #shows the network state of interaction
print(state.d_state.loc[interaction, :])
```

Output:
```
   State
0     13
```


-----------------------
### 6. ADI
#### Description
Calculates the average dominance index (ADI) from a cumulative interaction matrix as described in Hemelrijk et al. (2005).

#### How to use
A ADI object is created with a list of the actors.
Then to calculate the ADI for an interaction call member function **calculate** with a cumulative interaction matrix **d_mC** from a [Matrix](#1-matrix) object, and the number of the current interaction that is used as an index to store the calculated ADI value.
ADI values are stored in Pandas DataFrame **d_ADI** with a column *ADI_[actorID]* for each actor, and can be accessed directly.

```python
from dhdat import ADI

actorIDs = [1, 2, 3, 4]
adi = ADI(actorIDs)

adi.calculate(matrix.d_mC, interaction)

print(adi.d_ADI.loc[interaction, :])
```

Output:
```
   ADI_1   ADI_2   ADI_3   ADI_4
0      1	   0	 0.5	   1

```

-----------------------
### 7. Xi
#### Description
Calculates the dominance index Xi, which is the proportion of aggressive
interaction won, for a cumulative interaction matrix as described in Lindquist
and Chase (2009)

#### How to use
A Xi object is created with a list of the actors.
Then to calculate the Xi for an interaction call member function **calculate** with a cumulative interaction matrix **d_mC** from a [Matrix](#1-matrix) object,
and the number of the current interaction that is used as an index to store the calculated Xi value.
Xi values are stored in Pandas DataFrame **d_Xi** with a column *Xi_[actorID]* for each actor, and can be accessed directly.

```python
from dhdat import Xi

actorIDs = [1, 2, 3, 4]
xi = Xi(actorIDs)

xi.calculate(matrix.d_mC, interaction)

print(xi.d_Xi.loc[interaction, :])
```

Output:
```
   Xi_1   Xi_2   Xi_3   Xi_4
0     1      0    0.5      1

```

-----------------------
### 8. Bursts
#### Description
Detects whether bursts occur, a pattern of repeated consecutive attacks in the same direction within a dyad, as described by Lindquist and Chase (2009).
It does this by comparing the direction of the current interaction with the previous interaction. Note that this definition does not include a time component.

#### How to use
A new Bursts object can by defined without any arguments.
To determine a interaction is part of a burst event, the member function **detect** requires a row of a Pandas DataFrame containing the current interaction, and the row containing the previous interaction, as well as the number of the current interaction to use as a index to store the resulting burst value.
The result (True or False) is stored in data member **d_bursts** and can be accesed directly as shown below.
This example shows how with a simple for loop burst events can be detected for a set of interactions, by storing the previous interaction index.
The first interaction can by definition never be a burst, and thus is skipped.

```python
from dhdat import Bursts
import pandas as pd

df = pd.read_csv("exampleDataSet.csv", delimiter="\t")

bursts = Bursts()                   #defines a new Bursts object
prevInteraction = None              #holds index of previous interaction

for interaction in df.index:
    if prevInteraction != None:
      bursts.detect(df.loc[interaction,:], df.loc[prevInteraction,:], interaction)

    prevInteraction = interaction

print(bursts.d_bursts)              #shows burst values for all interactions
```

Output:
```
    burst
0      
1   False
2   False
3   False
```
The field of the first interaction is empty as a burst is a series of interactions, and thus can only occur if there is a previous interaction.

-----------------------
### 9. PairFlips
#### Description
Detects pair-flip events, which is the reversal of the relationship of pair based on a non-cumulative interaction matrix.
This means that one counter attack is enough to reverse the relation and be marked as a pair-flip event. To detect these events
the direction of the relation of the pair involved in the current interaction, is compared to the non-cumulative interaction matrix of the previous interaction.

#### How to use
A new PairFlips object can by defined without any arguments.
To determine whether a interaction is a pair-flip event, the member function **detect** requires the non-cumulative matrix **d_mC** from a [Matrix](#1-matrix) object of the _previous_ interaction, a row of a Pandas DataFrame containing the current interaction, and the number of the current interaction to use as a index to store the resulting pair-flip value.
The result (True or False) is stored in data member **d_pairFlips** and can be accesed directly as shown below.
This example shows how with a simple for loop pair-flip events can be detected for a set of interactions, by storing the previous non-cumulative matrix.
The first interaction can by definition never be a pair-flip, and thus is skipped.

```python
from dhdat import Matrix
from dhdat import PairFlips
import pandas as pd

df = pd.read_csv("exampleDataSet.csv", delimiter="\t")

actorIDs = [1, 2, 3, 4]             #list of actor identifiers
matrix = Matrix(actorIDs)           
pairFlips = PairFlips()
prevNCMatrix = pd.DataFrame()       #holds previous non-cumulative matrix

for interaction in df.index:
                                    #adds interaction to non-cumulative matrix
    matrix.updateNonCumulative(df.loc[interaction,:])

    if not prevNCMatrix.empty:      #skip if no previous interactions
      pairFlips.detect(prevNCMatrix, df.loc[interaction, :], interaction)

                                    #make sure to copy, not assign a reference
    prevNCMatrix = matrix.d_mNC.copy()

print(pairFlips.d_pairFlips)        #shows pair-flip values for all interactions
```

Output:
```
   pairFlip
0
1     False
2     False
3     False       
```
The field of the first interaction is empty as a pair-flip is a reversal of the direction of attack, and thus per definition requires a previous interaction.

-----------------------
### 10. TauKr
#### Description
Calculates TauKr as defined in Hemelrijk (1989), which measures unidirectionality between a set of matrices.
The example below demonstrates how reciprocity of aggression (initiation) can be calculated using this module.

#### How to use
A new TauKr object can be defined without any arguments. With the function *calculate()* TauKr can be calculated from two matrices directly, or by supplying one matrix to *calculate_T()* TauKr is calculated against the transposed version of the supplied matrix.
The matrix that is supplied must be a Pandas DataFrame as used by the [Matrix](#1-matrix) object. Both functions also require the interaction number to use as an index to store the outcome at.
In the example below reciprocity of aggression (initiations of fights) is determined by calculating the TauKr from the **d_mI** matrix from a [Matrix](#1-matrix) object.

```python
from dhdat import Matrix
from dhdat import TauKr
import pandas as pd

df = pd.read_csv("exampleDataSet.csv", delimiter="\t")

actorIDs = [1, 2, 3, 4]             #list of actor identifiers
matrix = Matrix(actorIDs)           
taukr = TauKr()

for interaction in df.index:
                                    #adds current interaction to initiations of aggression matrix
    matrix.updateInitiated(df.loc[interaction,:])

                                    #calculate reciprocity of aggression
    taukr.calculate_T(interaction, matrix.d_mI)

print(taukr.d_TauKr)                #shows pair-flip values for all interactions
```

Output:
```
   TauKr
1   -0.5
2   -0.5
3   -0.5       
```
Note index 0 is empty as there are insufficient values to calculate TauKr
