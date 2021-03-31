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
from argparse import ArgumentParser

'''
   Computing projections of positions in the next and previous plates
   taking into account different dZ.
   dZ is assumed to be the same 
   python Proiezioni.py -i RUN3.csv -o Proiezioni_RUN3.csv
'''

parser = ArgumentParser()
parser.add_argument("-i","--input",dest="inputcsv",help="input dataset in csv format with simulation (e.g. RUN5.csv)", required=True)
parser.add_argument("-o","--output",dest="outputcsv",help="output dataset in csv format with projection (e.g. Proiezioni_RUN5.csv)", required=True)

options = parser.parse_args()

dZconst = 1315
#getting z array
def computedz(zpositions, dZconst):
    '''produce an array with differences in dz between z positions'''
    dZnext = []
    dZprev = []

    dZnext.append(dZconst)
    #loop on all elements except the last
    for i in range(len(zpositions)-1):
     dZprev.append(abs(zpositions[i+1] - zpositions[i]))

    for i in range(1,len(zpositions)):
     dZnext.append(abs(zpositions[i] - zpositions[i-1])) 
    #the last element has no physical sense (distance after last film), we can leave 1315  
    dZprev.append(dZconst) 
    return dZnext, dZprev
dfsignal = pd.read_csv(options.inputcsv)
print(dfsignal)
zlist = dfsignal.groupby("PID").first()["z"].to_numpy() #taking position of all plates 
dZnextlist, dZprevlist = computedz(zlist, dZconst)

dZnext = []
dZprev = []
for PID in dfsignal["PID"].values:
    dZnext.append(dZnextlist[PID])
    dZprev.append(dZprevlist[PID])

print(dfsignal)

PID_max = np.max(dfsignal['PID'])

X_Next = dfsignal['x'].values + dfsignal['TX'].values*dZnext/2
Y_Next = dfsignal['y'].values + dfsignal['TY'].values*dZnext/2
Z_Next = dfsignal['z'].values+dZnext

X_Prev = dfsignal['x'].values - dfsignal['TX'].values*dZprev/2
Y_Prev = dfsignal['y'].values - dfsignal['TY'].values*dZprev/2
Z_Prev = dfsignal['z'].values-dZprev

Theta_signal = pow(dfsignal['TX'],2) + pow(dfsignal['TY'],2)
T_signal = pow(Theta_signal, 1/2)      
Theta = np.arctan(T_signal)

#next scripts do not work, because the columns were not added. Try to add them now
dfsignal['Theta'] = Theta
dfsignal['X_Next'] = X_Next
dfsignal['Y_Next'] = Y_Next
dfsignal['Z_Next'] = Z_Next

dfsignal['X_Prev'] = X_Prev
dfsignal['Y_Prev'] = Y_Prev
dfsignal['Z_Prev'] = Z_Prev
dfsignal['Signal'] = 1
    
print(dfsignal)

dfsignal.to_csv(options.outputcsv)
