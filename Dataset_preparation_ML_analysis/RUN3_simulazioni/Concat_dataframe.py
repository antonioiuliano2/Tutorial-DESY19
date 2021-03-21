import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import collections
from collections import OrderedDict
from copy import copy

'''
concatenates dataframes for all showers
First part: after Theta and IP/DeltaZ selections
Second part: after introducing dx, dy, dTX, dTY, after calling Ricerca_new.py
'''

def afterthetacut():
 '''Unisce i dataset ottenuti dopo il taglio in Theta e in IP/DeltaZ'''
 dftot = pd.DataFrame()
 dfu = pd.read_csv('Inizio_sciame_RUN5.csv')

 MCEvent = np.unique(dfu['MCEvent'])

 for shower in MCEvent:
    print(shower)
    try:
     df = pd.read_csv('Theta/Thetabt_{}.csv'.format(shower))
     del df['Unnamed: 0']
     dftot = pd.concat([dftot, df])
    except FileNotFoundError:
     print("No file for shower{}".format(shower))

 for j in MCEvent:
   if  dftot.query('Ishower=={}'.format(j)).empty:
       print(j)    

 dftot.to_csv('Theta/Dataset_tagli.csv')



def afternewvariables():
 '''Unisce i dataset l'introduzione delle variabili dx, dy, dTX, dTY, da usare dopo Ricerca_new.py'''
 dftot = pd.DataFrame()
 dfu = pd.read_csv('Inizio_sciame_RUN5.csv')

 MCEvent = np.unique(dfu['MCEvent'])

 for shower in MCEvent:
    print(shower)
    try:
     df = pd.read_csv('Event/Event{}.csv'.format(shower))
     del df['Unnamed: 0']
     dftot = pd.concat([dftot, df])
    except FileNotFoundError:
     print("No file for shower {}".format(shower))

 for j in MCEvent:
   if  dftot.query('Ishower=={}'.format(j)).empty:
       print(j)    

 dftot.to_csv('Event/Final_dataset.csv')

