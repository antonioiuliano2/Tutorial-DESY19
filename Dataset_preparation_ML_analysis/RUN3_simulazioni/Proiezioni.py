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
dfsignal = pd.read_csv('/home/mdeluca/dataset/RUN3/RUN3.csv')
print(dfsignal)
X_Next = dfsignal['x'].values + dfsignal['TX'].values*dZ/2
Y_Next = dfsignal['y'].values + dfsignal['TY'].values*dZ/2
Z_Next = dfsignal['z'].values+dZ

X_Prev = dfsignal['x'].values - dfsignal['TX'].values*dZ/2
Y_Prev = dfsignal['y'].values - dfsignal['TY'].values*dZ/2
Z_Prev = dfsignal['z'].values-dZ

Theta_signal = pow(dfsignal['TX'],2) + pow(dfsignal['TY'],2)
T_signal = pow(Theta_signal, 1/2)      
Theta = np.arctan(T_signal)

dfsignal['Theta'] = Theta
dfsignal['X_Next'] = X_Next
dfsignal['Y_Next'] = Y_Next
dfsignal['Z_Next'] = Z_Next

dfsignal['X_Prev'] = X_Prev
dfsignal['Y_Prev'] = Y_Prev
dfsignal['Z_Prev'] = Z_Prev
dfsignal['Signal'] = 1
    
print(dfsignal)

dfsignal.to_csv('/home/mdeluca/dataset/RUN3/Proiezioni_RUN3.csv')
