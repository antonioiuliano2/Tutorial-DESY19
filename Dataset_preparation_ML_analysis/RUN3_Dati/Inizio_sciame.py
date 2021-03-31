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
from argparse import ArgumentParser

'''
   definisce il punto di inizio dello sciame e gli altri segmenti associati
   python Inizio_sciame.py -i Proiezioni_RUN3data.csv -os Inizio_candidati_sciami.csv -or  RUN3data_ric.csv
'''

parser = ArgumentParser()
parser.add_argument("-i","--input",dest="inputcsv",help="input dataset in csv format with projections (e.g. Proiezioni_RUN5.csv)", required=True)
parser.add_argument("-os","--outputstarters",dest="outputcsvstarters",help="output dataset in csv format with shower injectors (e.g. Inizio_candidati_sciami.csv)", required=True)
parser.add_argument("-or","--outputremainder",dest="outputcsvremainder",help="output dataset in csv format with remainder of the shower (e.g. RUN5data_ric.csv)", required=True)
options = parser.parse_args()

dfevent = pd.read_csv(options.inputcsv)

maxtheta = 0.050 #50 mrad
maxplates = 3 #first 3 plates

maxPID = dfevent["PID"].max()
minPID = maxPID - maxplates + 1 #maxPID is included (ie.,26,27,28)
#getting shower starters and remainder base tracks
dfcandidates = dfevent.query("TrackID>=0 and PID >= {} and sqrt(TX*TX+TY*TY)<={}".format(minPID, maxtheta))
dfremainder = dfevent.query("not(TrackID>=0 and PID >= {} and sqrt(TX*TX+TY*TY)<={})".format(minPID, maxtheta))

dfcandidates = dfcandidates.sort_values("PID",ascending=False) #from most upstream plate to most downstream
dfstarters = dfcandidates.groupby("TrackID").last() #taking the last segment (accepting the selection) of tracks
#we want to know which we excluded to add them back to remainder
dfnotstarters = dfcandidates.merge(dfstarters,how = 'left', indicator = True).query("_merge=='left_only'")
del dfnotstarters["_merge"]
dfremainder = pd.concat([dfremainder,dfnotstarters])

#adding increasing counter Ishower
dfstarters["Ishower"]=np.arange(0, len(dfstarters))
dfstarters.to_csv(options.outputcsvstarters)
dfremainder.to_csv(options.outputcsvremainder)
