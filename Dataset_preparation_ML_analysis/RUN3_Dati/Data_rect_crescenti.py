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
   it builds rectangles of increasing dimensions (pyramid)
   
   before launching it, please make a empty directory
   it will fill this folder with a file for each shower

   python Rect_crescenti.py -n 10 -is Inizio_candidati_sciami.csv -if Rect -of Rect_crescenti
'''

parser = ArgumentParser()

parser.add_argument("-n","--nshower",dest="nshower",help="number of shower event",default=0)
parser.add_argument("-is","--inputstarters",dest="inputcsvstarters",help="input dataset in csv format with shower injectors", required=True)
parser.add_argument("-if","--inputfolder",dest="inputfolder",help="folder to access input datasets",required=True)
parser.add_argument("-of","--outputfolder",dest="outputfolder",help="folder to store output datasets",required=True)
options = parser.parse_args()

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

#dfefake = pd.read_csv('/home/maria/Scrivania/TestRF/Noisefake_Ishower.csv')
#dfefake = pd.read_csv('/home/mdeluca/dataset/Noise_New/Noisefake_Ishower.csv')
dfefake = pd.read_csv(options.inputcsvstarters)
#Ishower = [n for n in range(19, 20)]
Ishower = np.unique(dfefake['Ishower'])
#dfefake1 = dfefake.query('Ishower=={}'.format(Ishower))
#i = int(input('Quanto vale i?'))
#y = int(input('Intercetta?'))
i = 140
y = 500
#del dfefake['Unnamed: 0']

def calcRect(ishower):
    print(ishower)
    #dfshower = pd.read_csv('/home/maria/Scrivania/TestRF/Rect_Fake{}.csv'.format(ishower))
    dfshower = pd.read_csv(options.inputfolder+'/Rect_data{}.csv'.format(ishower)) 
    del dfshower['Unnamed: 0'] 

    global dfproiezioni
    global dft
    global dfPID_successivo
    global dfnoise_rect
    global dfnoise_successivo
    global dft    

    dfproiezioni = dfproiezioni[0:0]
    df = df[0:0]
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
       
           dft = pd.concat([dfPID_successivo1, dfcentrale1])
           dft.to_csv(options.outputfolder+'/Rect_crescentidata{}.csv'.format(ishower)) 
           
def calcallRects():
 for ishower in Ishower:
    calcRect(ishower)

if (int(options.nshower) >0):
 calcRect(int(options.nshower))
else:
 calcallRects()


