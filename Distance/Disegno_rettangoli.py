'''
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

#df = pd.read_csv('/home/chiara/Scrivania/Noise_Signal/Dataset/Proiezioni_Run3.csv')
dfevent = pd.read_csv('/home/mariadeluca/Desktop/Noise_Signal/Dataset/PID_ric_signal.csv')
#dfric = pd.read_csv('/home/mdeluca/dataset/Event0.csv')
#dfrumore = pd.read_csv('/home/mdeluca/dataset/Noise_Event0.csv')

dfric = dfevent.query('MCEvent==120')
MCEvent= np.unique(dfric['MCEvent'])   # 128,233, 257
f1 = figure(figsize=(12,7.5), dpi=80)
f2 = figure(figsize=(12,7.5), dpi=80)
f3 = figure(figsize=(12,7.5), dpi=80)
ax1 = f1.gca()
ax2 = f2.gca()
ax3 = f3.gca()
C=[]
DiffX1 = []
DiffY1 =[]
DiffTX1=[]
DiffTY1=[]
Dist = []
DistT =[]
DiffX1noise = []
DiffY1noise =[]
DiffTX1noise =[]
DiffTY1noise =[]
minimumR = []
minimumT = []
min_indexR = []
min_indexT = []

dfnew = pd.DataFrame()

i = int(input('Quanto vale i?'))
for shower in MCEvent:
    print(shower)
    
    dfshower =dfric.query('MCEvent=={}'.format(shower))
    
    PID_min = np.min(dfshower['PID'])
    PID_max = np.max(dfshower['PID'])
    ax1.plot(PID_max-dfshower['PID'], dfshower['x'],linewidth=0.0,marker='o', color='brown', alpha=1, label='MCEvent=={}'.format(shower))
    ax1.plot(PID_max-dfshower['PID']+1, dfshower['X_Next'],linewidth=0.0,marker='.', color='goldenrod', alpha=1, label='MCEvent=={}'.format(shower))
    ax2.plot(PID_max-dfshower['PID'], dfshower['y'],linewidth=0.0,marker='o', color='brown', alpha=1, label='MCEvent=={}'.format(shower))
    ax2.plot(PID_max-dfshower['PID']+1, dfshower['Y_Next'],linewidth=0.0,marker='.', color='goldenrod', alpha=1, label='MCEvent=={}'.format(shower))
    
    for m in range(PID_min+1,PID_max+1):
        dfPID = dfshower.query('PID=={}'.format(m))
        dfPID_Next = dfshower.query('PID=={}'.format(m-1))

        print('PID = {}'.format(m), dfPID, dfPID_Next)

'''
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


dfevent = pd.read_csv('/home/mariadeluca/Desktop/Noise_Signal/Dataset/PID_ric_signal.csv')
print(dfevent)

#dfshower = dfevent.query('MCEvent==120')
f1 = figure(figsize=(12,7.5), dpi=80)
ax1 = f1.gca()
MCEvent = [120]


i = int(input('Parametro altezza rettangolo:'))
for shower in MCEvent:
    dfshower = dfevent.query('MCEvent=={}'.format(shower))
    PID_min = np.min(dfshower['PID'])
    PID_max = np.max(dfshower['PID'])
    ax1.scatter(PID_max-dfshower['PID'], dfshower['x'], color='brown', marker='o')
    ax1.scatter(PID_max-dfshower['PID']+1, dfshower['X_Next'], color='goldenrod', marker='.')
        
    dfcentrale = dfshower.query('PID=={}'.format(PID_max))
    xcentrale = np.unique(dfcentrale['x'].values)
    ycentrale = np.unique(dfcentrale['y'].values)
      
    
    
    for m in range(PID_min+1, PID_max+1):
        dfPID = dfshower.query('PID=={}'.format(m))
        dfPID_Next =dfshower.query('PID=={}'.format(m-1))
        print(m, dfPID, dfPID_Next)
        xn = np.unique(dfPID['x'].values)
        zn = np.unique(dfPID['z'].values)
        yn = np.unique(dfPID['y'].values)
        xPIDnext = np.unique(dfPID_Next['x'].values)
  
        if len(xn)>0:  #len(xPIDnext)>0
           xc = max(xcentrale)
           yc = max(ycentrale)
           xmax = max(xn)
           xmin = min(xn)
           ymax = max(yn)
           ymin = min(yn)
           zmin = min(zn)
           zmax = max(zn)

           xmedia = i*(PID_max-m)+500 #PID_max-m
           ymedia= i*(PID_max-m)+500
           rect2 = mpatches.Rectangle((PID_max-m+0.7,xc-xmedia/2),0.7,xmedia, linestyle='--', edgecolor='k', facecolor='none', lw=2) #
           ax1.add_patch(rect2)

           dfxy = dfPID.query('{}-{}<=x<={}+{} and {}-{}<=y<={}+{}'.format(xc,xmedia/2,xc,xmedia/2, yc,ymedia/2,yc,ymedia/2))
           dfxynext = dfPID.query('{}-{}<=X_Next<={}+{} and {}-{}<=Y_Next<={}+{}'.format(xc,xmedia/2,xc,xmedia/2, yc,ymedia/2,yc,ymedia/2))
           dfxyPID_next = dfPID_Next.query('{}-{}<=x<={}+{} and {}-{}<=y<={}+{}'.format(xc,xmedia/2,xc,xmedia/2, yc,ymedia/2,yc,ymedia/2))



        
