import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xgboost
import collections
from collections import OrderedDict
import seaborn as sns
from copy import copy

# Unisce i dataset ottenuti dopo il taglio in Theta e in IP/DeltaZ#
dftot = pd.DataFrame()
dfu = pd.read_csv('/home/mdeluca/dataset/RUN3/Inizio_sciame_RUN3.csv')

MCEvent = np.unique(dfu['MCEvent'])

for shower in MCEvent:
    print(shower)
    df = pd.read_csv('/home/mdeluca/dataset/RUN3/RUN3/Theta/Thetabt_{}.csv'.format(shower))
    del df['Unnamed: 0']
    dftot = pd.concat([dftot, df])

for j in MCEvent:
   if  dftot.query('Ishower=={}'.format(j)).empty:
       print(j)    

dftot.to_csv('/home/mdeluca/dataset/RUN3/Theta/Dataset_tagli.csv')



# Unisce i dataset l'introduzione delle variabili dx, dy, dTX, dTY, da usare dopo Ricerca_new.py#
'''
for shower in MCEvent:
    print(shower)
    df = pd.read_csv('/home/mdeluca/dataset/RUN3/Event/Event{}.csv'.format(shower))
    del df['Unnamed: 0']
    dftot = pd.concat([dftot, df])

for j in MCEvent:
   if  dftot.query('Ishower=={}'.format(j)).empty:
       print(j)    

dftot.to_csv('/home/mdeluca/dataset/RUN3/RUN3/Event/Final_dataset_RUN3.csv')
'''
