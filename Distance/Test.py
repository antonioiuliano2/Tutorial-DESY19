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

dfevent = pd.read_csv('/home/maria/Scrivania/Noise_Signal/Dataset/PID_ric_signal.csv')
#dfevent = pd.read_csv('/home/mariadeluca/Desktop/New_Folder/Distance/PID_ric_signal_new.csv')
#dfric = pd.read_csv('/home/mdeluca/dataset/Event0.csv')
#dfrumore = pd.read_csv('/home/mdeluca/dataset/Noise_Event0.csv')

dfric = dfevent.query('MCEvent==0')
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
dfnuovo = pd.DataFrame()
i = int(input('Quanto vale i?'))
for shower in MCEvent:
    print(shower)
    
    dfshower =dfric.query('MCEvent=={}'.format(shower))
    
    PID_min = np.min(dfshower['PID'])
    PID_max = np.max(dfshower['PID'])
    ax1.plot(PID_max-dfshower['PID'], dfshower['x'],linewidth=0.0,marker='o', color='brown', alpha=1, label='MCEvent=={}'.format(shower)) #PID_max-dfshower['PID']
    ax1.plot(PID_max-dfshower['PID']+1, dfshower['X_Next'],linewidth=0.0,marker='.', color='goldenrod', alpha=1, label='MCEvent=={}'.format(shower))#PID_max+1-dfshower['PID']
    ax2.plot(PID_max-dfshower['PID'], dfshower['y'],linewidth=0.0,marker='o', color='brown', alpha=1, label='MCEvent=={}'.format(shower))#PID_max-dfshower['PID']
    ax2.plot(PID_max-dfshower['PID']+1, dfshower['Y_Next'],linewidth=0.0,marker='.', color='goldenrod', alpha=1, label='MCEvent=={}'.format(shower))
    print(PID_min, PID_max)#PID_max+1-dfshower['PID']
    print('..........................')
    
    if PID_min>=0:
      for m in range(PID_min, PID_max+1):
        print(m)
        #print(PID_max-m+1)
        #print(PID_max-m)
        dfPID = dfshower.query('PID=={}'.format(m))  #PID_max-m+1
        dfPID_Next = dfshower.query('PID=={}'.format(m-1))#PID_max-m
        print('..........................')
        #print(dfPID, dfPID_Next)
        
        #print('..........................................')
        dfcentrale = dfshower.query('PID=={}'.format(PID_max))
        xcentrale = np.unique(dfcentrale['x'].values)
        ycentrale = np.unique(dfcentrale['y'].values)
        #print(dfcentrale, xcentrale, ycentrale)
        xn = np.unique(dfPID['x'].values)
        zn = np.unique(dfPID['z'].values)
        yn = np.unique(dfPID['y'].values)
        xPIDnext = np.unique(dfPID_Next['x'].values)
        
        if len(xn)>0: # len(xPIDnext)>0:
           xc = max(xcentrale)
           yc = max(ycentrale)
           xmax = max(xn)
           xmin = min(xn)
           ymax = max(yn)
           ymin = min(yn)
           zmin = min(zn)
           zmax = max(zn)

           xmedia = i*(PID_max-m+1)+500
           ymedia= i*(PID_max-m+1)+500
           zmedia = (zmax-zmin)+1100
           PIDmedia = m+1 
           dfxy = dfPID.query('{}-{}<=x<={}+{} and {}-{}<=y<={}+{}'.format(xc,xmedia/2,xc,xmedia/2, yc,ymedia/2,yc,ymedia/2))
           dfxynext = dfPID.query('{}-{}<=X_Next<={}+{} and {}-{}<=Y_Next<={}+{}'.format(xc,xmedia/2,xc,xmedia/2, yc,ymedia/2,yc,ymedia/2))
           dfxyPID_next = dfPID_Next.query('{}-{}<=x<={}+{} and {}-{}<=y<={}+{}'.format(xc,xmedia/2,xc,xmedia/2, yc,ymedia/2,yc,ymedia/2))
           if m>PID_min:
              rect2 = mpatches.Rectangle((PID_max-m+1-0.3,xc-xmedia/2),0.7,xmedia, linestyle='--', edgecolor='k', facecolor='none', lw=2) #PID_max+1-m-0.3
              rect = mpatches.Rectangle((PID_max+1-m-0.3,yc-ymedia/2),0.7,ymedia, linestyle='--', edgecolor='k', facecolor='none', lw=2)#PID_max+1-m-0.3
              ax1.add_patch(rect2)
              ax2.add_patch(rect)
           print('PID={}, x_Proiettato_Next={},  y_Proiettato_Next={}, PID_Next = {}, x_PID_Next={}, y_PID_Next={}'.format(np.unique(dfxy['PID'].values), dfxy['X_Next'].values, dfxy['Y_Next'].values, np.unique(dfxyPID_next['PID'].values),dfxyPID_next['x'].values, dfxyPID_next['y'].values))
           #print('-----------------------------------------')
           print('PID = {},  xc={}, yc ={}, xc-xmedia/2 = {},  xc+xmedia/2 = {}, yc-ymedia/2 = {} ,  yc+ymedia/2 = {} , xmedia ={},  ymedia ={}'.format(np.unique(dfxyPID_next['PID'].values), xc, yc, xc-xmedia/2,  xc+xmedia/2, yc-ymedia/2,  yc+ymedia/2,  xmedia, ymedia ))
           #rect2 = mpatches.Rectangle((m-0.4,xmin-250),0.8,xmedia, linestyle='--', edgecolor='k', facecolor='none', lw=2)

           #plt.show()

           xevent = np.unique(dfxyPID_next['x'].values)
           xnext = np.unique(dfxy['X_Next'].values)
           yevent = np.unique(dfxyPID_next['y'].values)
           ynext = np.unique(dfxy['Y_Next'].values)
           TXevent = np.unique(dfxyPID_next['TX'].values)
           TXnext = np.unique(dfxy['TX'].values) 
           TYevent = np.unique(dfxyPID_next['TY'].values)
           TYnext = np.unique(dfxy['TY'].values)
           c = np.unique(len(dfxy))
           C.append(c)
           f = sum(C)
           d = len(dfric)

           for n in range(0, len(xevent)):
               DiffX = xevent[n] - xnext
               
               DiffY = yevent[n] - ynext
               DiffTX = TXevent[n] - TXnext
               DiffTY = TYevent[n] - TYnext
               
               DiffX1.append(DiffX)
               DiffY1.append(DiffY)
               DiffTX1.append(DiffTX)
               DiffTY1.append(DiffTY)
               
               dists_up = np.sqrt((DiffX)**2 + (DiffY)**2)
               dists_upT = np.sqrt((DiffTX)**2 + (DiffTY)**2)
               dists_upT1 =np.arctan(dists_upT)
               if len(dists_up)>0:
                  mindR = np.min(dists_up)
                  mindT = np.min(dists_upT1)
                  min_indR = np.argmin(dists_up)
                  min_indT = np.argmin(dists_upT1)
               else:
                  mindR = -1.
                  mindT = -1.
                  min_indR = -1.
                  min_indT = -1.
               minimumR.append(mindR)
               minimumT.append(mindT)
               min_indexR.append(min_indR)
               min_indexT.append(min_indT)
               #print(mind)
               #min_ind = np.argmin(dists_up)
               #print(min_ind)
               #tx_up = dfevent1.iloc[min_ind]['TX']
               #print('TX',tx_up)
               Dist.append(dists_up)
               DistT.append(dists_upT1)
               #ty_up = dfevent1.iloc[min_ind]['TY']
               #Theta = np.sqrt((dfevent0['TX']-tx_up)**2 + (dfevent0['TY']-ty_up)**2)
               #F = np.hstack([Dist])
           dfnuovo = pd.concat([dfnuovo, dfxynext])
           dfnew= pd.concat([dfnew, dfxyPID_next])
           
    df = pd.concat([dfnuovo, dfnew])
    df = df.reset_index(drop=True)
    df_gpby = df.groupby(list(df.columns)) 
    idx = [x[0] for x in df_gpby.groups.values() if len(x) == 1]
    dft = df.reindex(idx)
    ax1.plot(PID_max-dft['PID'], dft['x'],linewidth=0.0,marker='x', markersize=10, color='navy', alpha=5.0)
    ax2.plot(PID_max-dft['PID'], dft['y'], linewidth=0.0,marker='x', markersize=10, color='navy', alpha=5.0)

ax1.set_xlabel('z[$\mu m$]')
ax1.set_ylabel('x[$\mu m$]')

ax2.set_xlabel('z[$\mu m$]')
ax2.set_ylabel('y[$\mu m$]')
#af10.set_title('Signal distribution')
plt.show()
