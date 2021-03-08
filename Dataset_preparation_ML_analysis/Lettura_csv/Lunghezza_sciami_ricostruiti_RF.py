from __future__ import division 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, scatter, draw, figure, show
from scipy.optimize import curve_fit
from matplotlib import colors


p=1
df = pd.read_csv('/home/mdeluca/dataset/RUN3/RUN3_3/Random_Forest/Prediction.csv')
dfelectron = pd.read_csv('/home/mdeluca/dataset/RUN3/Inizio_sciame_RUN3.csv') 
del df['Unnamed: 0']
del dfelectron['Unnamed: 0']                                                                                

MCEvent = np.unique(df['Ishower'].values)

S = []
SB = []
BS = []
B = []
M = []
Pid = []
Pr = []
Zeta = []
for shower in MCEvent:
   print(shower)
   dfe = dfelectron.query('MCEvent=={}'.format(shower)) 
   dfshower =  df.query('Ishower=={}'.format(shower))
   dfsignal = dfshower.query('Y_test==1. and Y_pred_forest==1')
   dfsignal2 = dfshower.query('Y_test==1. and Y_pred_forest==0')
   dfsignal3 = dfshower.query('Y_test==0. and Y_pred_forest==1')
   dfsignal4 = dfshower.query('Y_test==0. and Y_pred_forest==0')
   
   PID_max = dfe['PID'].values
   zmin = dfe['z'].values
   PID_ric = 28-PID_max
   if len(dfshower)>=0:
    signal = len(dfsignal)
    sigback = len(dfsignal2)
    backsig = len(dfsignal3)
    back = len(dfsignal4)
    
    
    S.append(signal)
    SB.append(sigback)
    BS.append(backsig)
    B.append(back)
    Pid.append(PID_max)
    Pr.append(PID_ric)
    Zeta.append(zmin)

    s = np.hstack(S)
    sb = np.hstack(SB)
    bs = np.hstack(BS)
    b = np.hstack(B)
    Ev = np.unique(dfshower['Ishower'].values)
    M.append(Ev)
    Mh = np.hstack(M)
    PiD = np.hstack(Pid)
    Pid_ric = np.hstack(Pr)
    zeta = np.hstack(Zeta)

labels = ['MCEvent', 'Signal', 'SigBack', 'BackSig', 'Background', 'PID_max', 'PID_ric', 'zmin']
dffinale = pd.DataFrame({'MCEvent':Mh, 'Signal':s, 'SigBack':sb, 'BackSig':bs, 'Background':b, 'PID_max':PiD, 'PID_ric':Pid_ric, 'zmin':zeta}, columns = labels)
dffinale.to_csv('/home/mdeluca/dataset/RUN3/Random_Forest/Lunghezza_sciami_ric.csv')


for i in range(0,360):
    if dffinale.query('MCEvent=={}'.format(i)).empty:
       print(i)


