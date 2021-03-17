from __future__ import division 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, scatter, draw, figure, show
from argparse import ArgumentParser

'''
It computes theta_bt - theta_e,
            theta'_bt,
            IP/DeltaZ

DeltaT is theta_bt - theta_e
Angolo_cono is theta'_bt

It applies all the selections on these variables
theta_bt - theta_e <= 0.6
IP/DeltaZ <= 0.4

python Taglio_Theta.py -n 10 -is Inizio_sciame_RUN3.csv -if Rect_crescenti -of Theta
'''

parser = ArgumentParser()

parser.add_argument("-n","--nshower",dest="nshower",help="number of shower event",default=0)
parser.add_argument("-is","--inputstarters",dest="inputcsvstarters",help="input dataset in csv format with shower injectors", required=True)
parser.add_argument("-if","--inputfolder",dest="inputfolder",help="folder to access input datasets",required=True)
parser.add_argument("-of","--outputfolder",dest="outputfolder",help="folder to store output datasets",required=True)
options = parser.parse_args()

X=[]
Y = []
DeltaT = []
DeltaT_noise = []
dfs = pd.DataFrame()
dfu = pd.DataFrame()
dfc = pd.DataFrame()
dfb = pd.DataFrame()

dfe = pd.DataFrame()
dff = pd.DataFrame()
dfg = pd.DataFrame()

dfe = pd.read_csv(options.inputcsvstarters)
#Ishower = [n for n in range(720, 721)]
Ishower = np.unique(dfe['MCEvent'].values)
#del dfefake['Unnamed: 0']

def calcTheta(ishower):
    print(ishower)
    del X[:]
    del Y[:]
    #del DeltaT[:]
    #del DeltaT_noise[:]
    dfu = dfu[0:0] # per creare un dataset unico con il taglio in DeltaT<=0.6rad si cmmenta con #
    #dfs = dfs[0:0]
    #dfb = dfb[0:0]
    #dfc = dfc[0:0]
    #dfe = dfe[0:0]
    #dff = dff[0:0]
    #df = pd.read_csv("/home/chiara/Scrivania/Distanze/Event0/Dataset_rect{}_nuovo.csv".format(shower))
    df = pd.read_csv(options.inputfolder+('/Rect_crescenti{}.csv'.format(ishower)))
    del df['Unnamed: 0']
    dfshower = df.query('Signal==1')
    PID_max = np.max(dfshower['PID'])
    PID_min = np.min(dfshower['PID'])

    dfirst = dfshower.query('PID=={}'.format(PID_max))
    firstX = dfirst['x'].values[0]
    firstY = dfirst['y'].values[0]
    firstZ = dfirst['z'].values[0]
    firstTX = dfirst['TX'].values[0]
    firstTY = dfirst['TY'].values[0]

    firstT = dfirst['Theta'].values[0]

    dfnext = df.query('PID<{}'.format(PID_max))
    nextX  = dfnext['x'].values
    nextY  = dfnext['y'].values
    nextZ  = dfnext['z'].values
    nextTX = dfnext['TX'].values
    nextTY = dfnext['TY'].values
    nextT  = dfnext['Theta'].values

    #calcolo Theta_bt-Theta_e#
    DeltaT = nextT-firstT



    DiffX = firstX-nextX
    DiffY = firstY-nextY
    DiffZ = firstZ-nextZ
   
    DiffTX = firstTX-nextTX
    DiffTY = firstTY-nextTY
 
    #Calcolo Angolo apertura e parametro di impatto#
    tanY = DiffY/DiffZ
    tanX = DiffX/DiffZ

    DeltaX = nextX-DiffZ*nextTX
    DeltaY = nextY-DiffZ*nextTY

    tanTheta2 = pow(tanX,2)+pow(tanY,2)
    tanTheta = pow(tanTheta2,1/2)
  
    PI = np.sqrt((firstX-DeltaX)**2+(firstY-DeltaY)**2)
  
    PI_n = PI/(-(DiffZ))

    dfnext_signal = dfnext.copy()
    dfnext_signal['DeltaT'] = DeltaT
    dfnext_signal['Par_impact'] = PI
    dfnext_signal['Par_impact_nor'] = PI_n
    dfnext_signal['Angolo_cono'] = tanTheta

    dfsignal = dfnext_signal.query('DeltaT <= 0.6')
    dfsignal1 = dfsignal.query('Par_impact_nor<=0.4')
    #dfu = pd.concat([dfsignal,dfirst])

    dfu = pd.concat([dfu, dfsignal])
    #dfsignal = dfu
    dfsignal1.to_csv(options.outputfolder+('/Thetabt_{}.csv'.format(ishower)))

def calcallThetas():
 for shower in MCEvent:
    calcTheta(shower)

#python Rect.py 11 makes all rectangles, otherwise only one
if (int(options.nshower) >0):
 calcTheta(int(options.nshower))
else:
 calcallThetas()
