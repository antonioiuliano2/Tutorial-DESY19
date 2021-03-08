import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xgboost
import collections
from collections import OrderedDict
import seaborn as sns
from copy import copy


dftot = pd.DataFrame()

MCEvent = [n for n in range(0, 173)]
for shower in MCEvent:
    print(shower)
    df = pd.read_csv('/home/mdeluca/dataset/RUN3/RUN3_data/Theta/ThetaIP_btdata{}.csv'.format(shower))
    del df['Unnamed: 0']
    dftot = pd.concat([dftot, df])

'''
for j in MCEvent:
   if  dftot.query('Ishower=={}'.format(j)).empty:
       print(j)    
'''

dftot.to_csv('/home/mdeluca/dataset/RUN3/RUN3_data/Theta/Final_data_tagliopar.csv')

