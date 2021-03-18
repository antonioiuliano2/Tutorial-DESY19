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
from argparse import ArgumentParser

'''
   first large selection in the transverse area
   1 cm x 1 cm in the xy plane

   before launching it, please make a empty directory Rect
   it will fill this folder with a file for each shower
   python Data_rect.py -n 10 -is Inizio_candidati_sciami.csv -ir RUN3data_selected.csv -of Rect
'''

parser = ArgumentParser()

parser.add_argument("-n","--nshower",dest="nshower",help="number of shower event",default=0)
parser.add_argument("-is","--inputstarters",dest="inputcsvstarters",help="input dataset in csv format with shower injectors", required=True)
parser.add_argument("-ir","--inputremainder",dest="inputcsvremainder",help="input dataset in csv format with remainder of the shower", required=True)
parser.add_argument("-of","--outputfolder",dest="outputfolder",help="folder to store output datasets",required=True)
options = parser.parse_args()

dfefake = pd.read_csv(options.inputcsvstarters)
print(dfefake)
#dfnoise = pd.read_csv('/home/mdeluca/dataset/RUN3/RUN3_data/Proiezioni_RUN3data.csv')
dfnoise = pd.read_csv(options.inputcsvremainder)
print(dfnoise)
#del dfefake['Unnamed: 0']
#del dfnoise['Unnamed: 0']
c = len(dfefake)

df = pd.DataFrame()
dfproiezioni = pd.DataFrame()
dfPID_successivo= pd.DataFrame()
dfnoise_rect = pd.DataFrame()
dfnoise_successivo = pd.DataFrame()
Ishower = np.unique(dfefake['Ishower'])
#Ishower = [n for n in range(19, 20)]

def calcRect(ishower):
    print(ishower)
    global df

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
    df.to_csv('/home/mdeluca/dataset/RUN3/RUN3_data/Rect/Rect_data{}.csv'.format(ishower)) 
            
def calcallRects():
 for ishower in Ishower:
    calcRect(ishower)

if (int(options.nshower) >0):
 calcRect(int(options.nshower))
else:
 calcallRects()