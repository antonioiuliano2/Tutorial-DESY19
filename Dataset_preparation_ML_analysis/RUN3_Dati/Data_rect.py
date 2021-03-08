from __future__ import print_function
from __future__ import division
import math
#import ROOT as R
import numpy as np
import pandas as pd
#import fedrarootlogon
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


dfefake = pd.read_csv('/home/mdeluca/dataset/RUN3/RUN3_data/Inizio_candidati_sciami.csv')
print(dfefake)
#dfnoise = pd.read_csv('/home/mdeluca/dataset/RUN3/RUN3_data/Proiezioni_RUN3data.csv')
dfnoise = pd.read_csv('/home/mdeluca/dataset/RUN3/RUN3_data/New/RUN3data_selected.csv')
print(dfnoise)
#del dfefake['Unnamed: 0']
#del dfnoise['Unnamed: 0']
c = len(dfefake)

df = pd.DataFrame()
dfproiezioni = pd.DataFrame()
dfPID_successivo= pd.DataFrame()
dfnoise_rect = pd.DataFrame()
dfnoise_successivo = pd.DataFrame()
#Ishower = np.unique(dfefake['Ishower'])
Ishower = [n for n in range(19, 20)]

for ishower in Ishower:
    print(ishower)
    dfishower = dfefake.query('Ishower == {}'.format(ishower))
    
    PID_min = np.min(dfishower['PID'])
    PID_max = np.max(dfishower['PID'])
    dfcentrale = dfishower.query('PID== {}'.format(PID_max))
    xc = (dfcentrale['x'].values[0])
    yc = (dfcentrale['y'].values[0])
    
    
    dfsciame_fak = dfnoise.query('PID<={}'.format(PID_max-1))
    dfsciame_fake = dfsciame_fak.query('{}-5000<=x<={}+5000 and {}-5000<=y<={}+5000'.format(xc,xc, yc,yc))
    dfsciame_fake1 = dfsciame_fake.copy()
    dfsciame_fake1['Ishower'] = ishower
    df = pd.concat([dfsciame_fake1, dfishower])
    df.to_csv('/home/mdeluca/dataset/RUN3/RUN3_data/New/Rect_data{}.csv'.format(ishower)) 
            




