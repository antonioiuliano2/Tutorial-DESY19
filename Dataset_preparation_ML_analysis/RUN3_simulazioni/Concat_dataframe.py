import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import collections
from collections import OrderedDict
from copy import copy
from argparse import ArgumentParser

'''
concatenates dataframes for all showers
First part: after Theta and IP/DeltaZ selections
Second part: after introducing dx, dy, dTX, dTY, after calling Ricerca_new.py
launch with python -i Concat_dataframe.py -is Inizio_sciame_RUN5.csv
then launch afterthetacut() for the first part, or afternewvariables() for the second part
'''

parser = ArgumentParser()
parser.add_argument("-is","--inputstarters",dest="inputcsvstarters",help="input dataset in csv format with shower injectors (e.g. Inizio_sciame_RUN5.csv)", required=True)
options = parser.parse_args()
dftot = pd.DataFrame()
dfu = pd.read_csv(options.inputcsvstarters)

def afterthetacut():
 '''Concatenate datasets from Theta and IP/DeltaZ cuts'''
 global dftot

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
 '''Concatenate datasets with new variables dx, dy, dTX, dTY, added by Ricerca_new.py'''
 global dftot

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

