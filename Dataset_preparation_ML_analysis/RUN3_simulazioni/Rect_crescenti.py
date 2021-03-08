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

f1 = figure(figsize=(12.5, 7))
ax1 = f1.gca()

f2 = figure(figsize=(12.5,7))
ax2 = f2.gca()

df = pd.DataFrame()
dfproiezioni = pd.DataFrame()
dfPID_successivo= pd.DataFrame()
dfnoise_rect = pd.DataFrame()
dfnoise_successivo = pd.DataFrame()
dft = pd.DataFrame()


dfe = pd.read_csv('/home/mdeluca/dataset/RUN3/Inizio_sciame_RUN3.csv')
del dfe['Unnamed: 0']
print(dfe)
MCEvent = np.unique(dfe['MCEvent'].values)
#MCEvent = [n for n in range(0,360)]

i = int(input('Quanto vale i?')) # i = 140
y = int(input('Quanto vale y?')) #y = 500
#del dfe['Unnamed: 0']

dfo = pd.DataFrame()
for ishower in MCEvent:
    print(ishower)
    #dfshower = pd.read_csv('/home/maria/Scrivania/TestRF/Rect_Fake{}.csv'.format(ishower))
    #dfshower = pd.read_csv('/home/mdeluca/dataset/RUN3/RUN3_3/Rect/Rect{}.csv'.format(ishower))
    dfshower = pd.read_csv('/home/mdeluca/dataset/RUN3/Rect/Rect{}.csv'.format(ishower))
    del dfshower['Unnamed: 0'] 

    dfproiezioni = dfproiezioni[0:0]
    dft = dft[0:0]
    dfPID_successivo = dfPID_successivo[0:0]
    dfnoise_rect = dfnoise_rect[0:0]
    dfnoise_successivo = dfnoise_successivo[0:0]
    dft = dft[0:0]


    PID_min = np.min(dfshower['PID'])
    PID_max = np.max(dfshower['PID'])
    dfcentrale = dfshower.query('PID== {}'.format(PID_max))
    xc = (dfcentrale['x'].values[0])
    yc = (dfcentrale['y'].values[0])
    

    if PID_min>=0:
      for m in range(PID_min, PID_max+1):
        #print(m)
        dfPID = dfshower.query('PID=={}'.format(m)) 
        dfPID_Next = dfshower.query('PID=={}'.format(m-1))
        
        xn = np.unique(dfPID['x'].values)
        zn = np.unique(dfPID['Z_Next'].values)
        yn = np.unique(dfPID['y'].values)
        

        if len(xn)>0:
           xmedia = i*(PID_max-m)+y
           ymedia= i*(PID_max-m)+y
           zmin = min(zn)          
           PIDmedia = m+1 
           xmedia_next = i*(PID_max+1-m)+y
           ymedia_next= i*(PID_max+1-m)+y


           dfxyPID_Next = dfPID_Next.query('{}-{}<x<{}+{} and {}-{}<y<{}+{}'.format(xc,xmedia_next/2,xc,xmedia_next/2, yc,ymedia_next/2,yc,ymedia_next/2))
          
           dfPID_successivo= pd.concat([dfPID_successivo, dfxyPID_Next])
           dfPID_successivo1 = dfPID_successivo.copy()
           dfcentrale1 = dfcentrale.copy()

           dfr = dfPID_successivo.query('Signal==1')
           dfy = dfPID_successivo.query('Signal==0')       
           dft = pd.concat([dfr, dfcentrale1])
           dfo = pd.concat([dft, dfy])
           #print(len(dfo))
           #dfo.to_csv('/home/mdeluca/dataset/RUN3/RUN3_3/Rect_crescenti/Rect_crescenti{}.csv'.format(ishower))
           dfo.to_csv('/home/mdeluca/dataset/RUN3/Rect_crescenti/Rect_crescenti{}.csv'.format(ishower))


