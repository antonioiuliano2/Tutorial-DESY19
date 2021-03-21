import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import collections
from collections import OrderedDict
from copy import copy

'''
concatenates dataframes for all showers
First part: after Theta and IP/DeltaZ selections
Second part: after introducing dx, dy, dTX, dTY, after calling Ricerca_new.py (set paths correctly)
'''
def afterthetacut():
 '''Unisce i dataset ottenuti dopo il taglio in Theta e in IP/DeltaZ'''
 dftot = pd.DataFrame()

 MCEvent = [n for n in range(0, 173)]
 for shower in MCEvent:
  try:
    print(shower)
    df = pd.read_csv('Theta/ThetaIP_btdata{}.csv'.format(shower))
    del df['Unnamed: 0']
    dftot = pd.concat([dftot, df])
  except FileNotFoundError:
     print("No file for shower {}".format(shower))

 for j in MCEvent:
    if  dftot.query('Ishower=={}'.format(j)).empty:
     print(j)    

 dftot.to_csv('Theta/Final_data_tagliopar.csv')

def afternewvariables():
 '''Unisce i dataset l'introduzione delle variabili dx, dy, dTX, dTY, da usare dopo Ricerca_new.py'''
 dftot = pd.DataFrame()

 MCEvent = [n for n in range(0, 173)]
 for shower in MCEvent:
  try: 
    print(shower)
    df = pd.read_csv('Event/Event{}.csv'.format(shower))
    del df['Unnamed: 0']
    dftot = pd.concat([dftot, df])
  except FileNotFoundError:
     print("No file for shower {}".format(shower))


 for j in MCEvent:
   if  dftot.query('Ishower=={}'.format(j)).empty:
       print(j)    

 dftot.to_csv('Event/Final_dataset_RUN3.csv')
