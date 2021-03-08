from matplotlib.pyplot import plot, scatter, draw, figure, show
import matplotlib.pyplot as plt
import pylab as pl
import math
from matplotlib import colors
import matplotlib
matplotlib.colors
matplotlib.colors.PowerNorm
matplotlib.axes.Axes.hist2d
matplotlib.pyplot.hist2d
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
import matplotlib.patches as mpatches
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from copy import copy
from collections import OrderedDict
import pandas as pd
import numpy as np


dZ = 1315
dfsignal = pd.read_csv('/home/mdeluca/dataset/RUN3/RUN3_data/RUN3data.csv')
print(dfsignal)
PID_max = np.max(dfsignal['PID'])

X_Next = dfsignal['x'].values + dfsignal['TX'].values*dZ/2
Y_Next = dfsignal['y'].values + dfsignal['TY'].values*dZ/2
Z_Next = dfsignal['z'].values+dZ

X_Prev = dfsignal['x'].values - dfsignal['TX'].values*dZ/2
Y_Prev = dfsignal['y'].values - dfsignal['TY'].values*dZ/2
Z_Prev = dfsignal['z'].values-dZ

Theta_signal = pow(dfsignal['TX'],2) + pow(dfsignal['TY'],2)
T_signal = pow(Theta_signal, 1/2)      
Theta = np.arctan(T_signal)
'''
del dfsignal['Theta'] 
del dfsignal['X_Next']
del dfsignal['Y_Next']
del dfsignal['Z_Next']

del dfsignal['X_Prev']
del dfsignal['Y_Prev']
del dfsignal['Z_Prev']
del dfsignal['Signal'] 

PID = np.unique(dfsignal['PID'])
#PID= [n for n in range(0,3)] 
dfg = pd.DataFrame()
dfc = pd.DataFrame()
for i in PID:
   print(i)
   dfsignal1 = dfsignal.query('PID=={}'.format(PID_max-i))
   dfsignal2 = dfsignal.query('PID=={}'.format(PID_max-i-1))
   z1 = np.unique(dfsignal2['z'])
   z2 = np.unique(dfsignal1['z'])
   dz = z1-z2
   #dz = np.unique(dfsignal2['z'])-np.unique(dfsignal1['x'])

   if i ==PID_max:
    dz = 1350
    X_Next = dfsignal1['x'].values + dfsignal1['TX'].values*dz/2
    Y_Next = dfsignal1['y'].values + dfsignal1['TY'].values*dz/2
    Z_Next = dfsignal1['z'].values+dz
   
    X_Prev = dfsignal1['x'].values - dfsignal1['TX'].values*dz/2
    Y_Prev = dfsignal1['y'].values - dfsignal1['TY'].values*dz/2
    Z_Prev = dfsignal1['z'].values-dz
   
    Theta_signal = pow(dfsignal1['TX'],2) + pow(dfsignal1['TY'],2)
    T_signal = pow(Theta_signal, 1/2)      
    Theta = np.arctan(T_signal)

    dfc = dfsignal1.copy()
    dfc['Theta'] = Theta
    dfc['X_Next'] = X_Next
    dfc['Y_Next'] = Y_Next
    dfc['Z_Next'] = Z_Next

    dfc['X_Prev'] = X_Prev
    dfc['Y_Prev'] = Y_Prev
    dfc['Z_Prev'] = Z_Prev
    dfc['Signal'] = 1
   
   else:
    X_Next = dfsignal1['x'].values + dfsignal1['TX'].values*dz/2
    Y_Next = dfsignal1['y'].values + dfsignal1['TY'].values*dz/2
    Z_Next = dfsignal1['z'].values+dz
   
    X_Prev = dfsignal1['x'].values - dfsignal1['TX'].values*dz/2
    Y_Prev = dfsignal1['y'].values - dfsignal1['TY'].values*dz/2
    Z_Prev = dfsignal1['z'].values-dz
   
    Theta_signal = pow(dfsignal1['TX'],2) + pow(dfsignal1['TY'],2)
    T_signal = pow(Theta_signal, 1/2)      
    Theta = np.arctan(T_signal)

   dfc = dfsignal1.copy()
   dfc['Theta'] = Theta
   dfc['X_Next'] = X_Next
   dfc['Y_Next'] = Y_Next
   dfc['Z_Next'] = Z_Next

   dfc['X_Prev'] = X_Prev
   dfc['Y_Prev'] = Y_Prev
   dfc['Z_Prev'] = Z_Prev
   dfc['Signal'] = 1

   
   if i ==PID_max:
   
 dz = 1350
    X_Next = dfsignal1['x'].values + dfsignal1['TX'].values*dz/2
    Y_Next = dfsignal1['y'].values + dfsignal1['TY'].values*dz/2
    Z_Next = dfsignal1['z'].values+dz
   
    X_Prev = dfsignal1['x'].values - dfsignal1['TX'].values*dz/2
    Y_Prev = dfsignal1['y'].values - dfsignal1['TY'].values*dz/2
    Z_Prev = dfsignal1['z'].values-dz
   
    Theta_signal = pow(dfsignal1['TX'],2) + pow(dfsignal1['TY'],2)
    T_signal = pow(Theta_signal, 1/2)      
    Theta = np.arctan(T_signal)

    dfc = dfsignal1.copy()
    dfc['Theta'] = Theta
    dfc['X_Next'] = X_Next
    dfc['Y_Next'] = Y_Next
    dfc['Z_Next'] = Z_Next

    dfc['X_Prev'] = X_Prev
    dfc['Y_Prev'] = Y_Prev
    dfc['Z_Prev'] = Z_Prev
    dfc['Signal'] = 1
    
    ''' 


#   dfg = pd.concat([dfc, dfg])


dfsignal.to_csv('/home/mdeluca/dataset/RUN3/RUN3_data/Proiezioni_RUN3data.csv')
