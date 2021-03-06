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

   python Rect.py -n 10 -is Inizio_sciame_RUN3.csv -ir PID_ric_RUN3.csv -ib Noise_RUN3_Proiezioni_new.csv -of Rect

'''

parser = ArgumentParser()

parser.add_argument("-n","--nshower",dest="nshower",help="number of shower event",default=-1)
parser.add_argument("-is","--inputstarters",dest="inputcsvstarters",help="input dataset in csv format with shower injectors (e.g. Inizio_sciame_RUN5.csv)", required=True)
parser.add_argument("-ir","--inputremainder",dest="inputcsvremainder",help="input dataset in csv format with remainder of the shower (e.g. PID_ric_RUN5.csv)", required=True)
parser.add_argument("-ib","--inputbackground",dest="inputbackground",help="input dataset in csv format with background projections (e.g. Noise_RUN3_proiezioni_new.csv)", required=True)
parser.add_argument("-of","--outputfolder",dest="outputfolder",help="folder to store output datasets (e.g. Rect)",required=True)
options = parser.parse_args()

dfe = pd.read_csv(options.inputcsvstarters)
#print(dfe)

dfsignal = pd.read_csv(options.inputcsvremainder)
dfnoise = pd.read_csv(options.inputbackground)
#dftot = pd.read_csv('/home/mdeluca/dataset/RUN3_2/Data_Noise_RUN3_2.csv')
#print(dfnoise)
del dfe['Unnamed: 0']
del dfsignal['Unnamed: 0']
del dfnoise['Unnamed: 0']
#c = len(dfefake)

df = pd.DataFrame()
dfproiezioni = pd.DataFrame()
dfPID_successivo= pd.DataFrame()
dfnoise_rect = pd.DataFrame()
dfnoise_successivo = pd.DataFrame()
dfst = pd.DataFrame()
dfnt = pd.DataFrame()
#MCEvent = np.unique(dfe['MCEvent'].values)
#Ishower = [n for n in range(500, 501)]
#MCEvent = [n for n in range(360, 720)]
MCEvent = np.unique(dfe['MCEvent'].values)


def calcRect(shower):
    print(shower)
    dfelectron = dfe.query('MCEvent == {}'.format(shower))
    dfcentrale = dfelectron
    PID_max = dfcentrale['PID'].values[0]
    xc = (dfcentrale['x'].values[0])
    yc = (dfcentrale['y'].values[0])
    
    dfsciame = dfsignal.query('MCEvent=={}'.format(shower))    
    dfs = dfsciame.query('PID<={}'.format(PID_max-1))
    dfn = dfnoise.query('PID<={}'.format(PID_max-1))
    dfsc = dfs.query('{}-5000<=x<={}+5000 and {}-5000<=y<={}+5000'.format(xc,xc, yc,yc))
    dfns = dfn.query('{}-5000<=x<={}+5000 and {}-5000<=y<={}+5000'.format(xc,xc, yc, yc))
    #dft1 = dft.copy()
    #dft1['Ishower'] = shower
    dfst = pd.concat([dfsc, dfcentrale])
    dfnt = pd.concat([dfst, dfns])
    dft1 = dfnt.copy()
    dft1['Ishower'] = shower
    #print(len(dfst))
    #print(len(dfnt))
    dft1.to_csv(options.outputfolder+('/Rect{}.csv'.format(shower)))         

def calcallRects():
 for shower in MCEvent:
    calcRect(shower)

#python Rect.py 11 makes all rectangles, otherwise only one
if (int(options.nshower) >=0):
 calcRect(int(options.nshower))
else:
 calcallRects()
