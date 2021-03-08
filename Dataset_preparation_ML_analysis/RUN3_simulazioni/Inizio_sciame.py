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


#Punto di inizio dello sciame#

dfevent = pd.read_csv('/home/mdeluca/dataset/RUN3/Proiezioni_RUN3.csv')
del dfevent['Unnamed: 0']
f1 = figure()
ax1 = f1.gca()

f2 = figure()
ax2 = f2.gca()

Lung = []
#MCEvent = np.unique(dfevent['MCEvent'].values)
MCEvent = [m for m in range(0, 360)]
MCEvent.remove(57)
PID = np.unique(dfevent['PID'].values)
PID1 = []
Lung[:] = []
m = []
Piatto = []
Piatto2 = []
dfnew = pd.DataFrame()
dfs = pd.DataFrame()
df = pd.DataFrame()
dfn = pd.DataFrame()
dft = pd.DataFrame()
dfc = pd.DataFrame()
dfm = pd.DataFrame()
dfg = pd.DataFrame()
dfp = pd.DataFrame()
dfr = pd.DataFrame()
dfq = pd.DataFrame()
dfu = pd.DataFrame()


for shower in MCEvent:
    print(shower)
    dfshower = dfevent.query('MCEvent=={}'.format(shower))
    PID_max = int(np.max(dfshower['PID'].values))
    PID_min = int(np.min(dfshower['PID'].values))
    print(PID_min, PID_max)
    del Lung[:]
    del m[:]
    dfs = dfs[0:0]
    for pid in range(PID_min,PID_max+1):
        dfPID = dfshower.query('PID=={}'.format(pid))
        c = (len(dfPID))
        Lung.append(c)
    dfs['PID'] = [m for m in range(PID_min,PID_max+1)]
    #dfs['PID'] = PID_max+1-PID_min
    dfs['Lunghezza'] =Lung
    PID = dfs['PID'].values
    #df = pd.concat([dfs, df])
    PID_max= np.max(dfs['PID'])
    dft = dfs.query('PID=={}'.format(PID_max))
    Lunghezza = dft['Lunghezza'].values
    
    if Lunghezza==2:
       platenumber=PID_max
       Piatto2.append(platenumber)       
    else: 
       plate = min(dfs.loc[(dfs['Lunghezza']==0) | (dfs['Lunghezza']==1)]['PID'])
       Piatto = max(dfs.loc[(dfs['Lunghezza']>1) & (dfs['Lunghezza']<=10)]['PID']+1)
       dft = dfshower.query('PID>={}'.format(Piatto))
       dfy = dfshower.query('PID=={}'.format(Piatto))
       #piattonew = min(dft.loc[(dft['Lunghezza']==1)]['PID'])
       #print(dft)
       if dfy.empty:
          n=1
          platenumber = Piatto+n
          dfv = dfshower.query('PID=={}'.format(platenumber))
          for n in range(1, 20, 1):
            if dfv.empty:
               n = n+1
               platenumber = Piatto+n
               dfv = dfshower.query('PID=={}'.format(platenumber))
               Piatto2.append(platenumber) 
            else:
               platenumber = Piatto+n
               Piatto2.append(platenumber) 
               break
       elif plate==Piatto:
          platenumber=plate
          Piatto2.append(platenumber)
       elif plate>Piatto:
          platenumber=plate
          Piatto2.append(platenumber)
       else:
          platenumber=Piatto
          Piatto2.append(platenumber)      

    dfsciame = dfshower.query('PID<{}'.format(platenumber))
    dfe = dfshower.query('PID=={}'.format(platenumber))
    ID =np.min(dfe['ID'])
    g = len(dfe)
    if g==2:
        dfn = dfe.query('ID=={}'.format(ID))
        dfp = pd.concat([dfp, dfn])
        dfr = pd.concat([dfp, dfr])
        dfn = pd.concat([dfsciame, dfn])
    else:
        dfn = dfe
        dfp= pd.concat([dfp, dfe])
        dfr = pd.concat([dfp, dfr])   
        dfn = pd.concat([dfsciame, dfn])
    dfq = pd.concat([dfn, dfq])
    dfu = dfp
dfq.to_csv('/home/mdeluca/dataset/RUN3/PID_ric_RUN3.csv')
dfu.to_csv('/home/mdeluca/dataset/RUN3/Inizio_sciame_RUN3.csv')    
    #dfq = pd.concat()


'''
    for n in range(0, platenumber+1):
          dfsciame = dfshower.query('PID=={}'.format(n))
          pid = dfsciame['PID']
          #print(pid)
          dfsciamenew = dfsciame.copy()
          dfsciamenew['PID_ric'] = platenumber-pid
          #print(dfsciame)
          #print(n)
          #ax1.scatter(dfsciame['z'], dfsciame['x'], marker='o', color='navy')
          PID = dfsciame['PID'].values
          PID1.append(PID)
          dfnew = pd.concat([dfnew, dfsciamenew])
    dfc = pd.concat([dfc, dfsciamenew])
dfs = dfc

MC = np.unique(dfs['MCEvent'])
for shower in MC:
    dfm = dfs.query('MCEvent=={}'.format(shower))
    ID =np.min(dfm['ID'])
    d = len(dfm)
    if d>1:
       dfg = dfm.query('ID=={}'.format(ID))
    dfp = pd.concat([dfp, dfg])

       
'''
#dfc.to_csv('Inizio_sciame.csv')
#dfnew.to_csv('PID_ric')        
#print(dfc)
#print(dfnew)
#del df


#dfnew.to_csv('/home/chiara/Scrivania/Noise_Signal/Dataset/Inizio_sciame_nuovo.csv')
#ax2.hist(dfnew.query('PID_ric==0'))
#plt.show()
#P = dfs['PID']


#dfPID['Lunghezza'] = Lung
'''
df = pd.read_csv('PID_ric_RUN3.csv')
dft = pd.DataFrame()
dfc = pd.DataFrame()
del df['Unnamed: 0']
MC = np.unique(df['MCEvent'].values)
#MC= [n for n  in range(0,2)]
for shower in MC:
    print(shower)
    dfshower = df.query('MCEvent== {}'.format(shower))
    dft = dfshower.replace({'MCEvent':{shower:shower+1080}})
    dfc = pd.concat([dfc, dft])


'''
df = pd.read_csv('/home/mdeluca/dataset/RUN3/Inizio_sciame_RUN3.csv')
f1 = figure(figsize=(13.5, 7.5))
ax1 = f1.gca()

PID = (df['PID'].values) 
plate = (28-PID)
ax1.hist(plate, 19, color='purple', histtype='step', label='Entries {}'.format(len(df)))
ax1.set_xlabel('28-PID')
ax1.set_ylabel('Counts')
ax1.set_title('Start of the shower')
ax1.legend()

