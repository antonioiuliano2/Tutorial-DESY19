from __future__ import division 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, scatter, draw, figure, show
from scipy.optimize import curve_fit
from matplotlib import colors

import ROOT as R
import root_numpy as rp

dffinale1 = pd.read_csv('MC/Lunghezza_sciame_nuovo.csv')#Lunghezza_sciame_pred_new.csv
df = pd.read_csv('MC/RF_application.csv')#Prediction.csv
dfelectron = pd.read_csv('MC/Inizio_sciame_new.csv')
dft = pd.DataFrame()

dffinale_data = pd.read_csv('Dati/Lunghezza_sciami.csv')
df_data = pd.read_csv('Dati/Dati_nuovo.csv')
dfelectron_data = pd.read_csv('Dati/Inizio_candidati_sciami.csv')
dft_data = pd.DataFrame()

del dffinale1['Unnamed: 0']
del dffinale_data['Unnamed: 0']
#df50 = dffinale.query('Signal>=50')

dffinale = dffinale1.query('Signal + BackSig>=50')
dffinale_d = dffinale_data.query('Signal>=50')
'''
c1 = R.TCanvas( 'c1', 'Histogram Drawing Options')
x = (dffinale_data['Signal'].to_numpy())+1
bins = (np.max(x)-np.min(x))/(len(dffinale))
hx = R.TH1D('hs', 'Showers size; signal segments; Entries', 18, 0, 180)
#hx = R.TH1D('hs', '#theta showers segments; #theta[rad]; Entries', 27, 0, 0.054)
rp.fill_hist(hx,x)
hx.Draw()
'''
MC = dffinale['MCEvent'].to_numpy()

for i in MC:
   dfr = df.query('MCEvent=={}'.format(i))
   dft = pd.concat([dft, dfr])

dfp = dft.query('Y_test==1. and Y_pred_forest==1')



Ishower = dffinale_d['Ishower'].to_numpy()

for i in Ishower:
   dfr_d = df_data.query('Ishower=={}'.format(i))
   dft_data = pd.concat([dft_data, dfr_d])

dfp_d = dft_data.query('Y_pred_forest_data==1')

#df1 MC, df2 Data

df1 = dfp.fillna(-1000000)
df2 = dfp_d.fillna(-1000000)

c2 = R.TCanvas( 'c2', 'Histogram Drawing Options2')
#variable to select not NA values
x0 = df1['DeltaT'].to_numpy() #DeltaT
y0 = df2['DeltaT'].to_numpy() #DeltaT
def retrievecolumns(variable):
 x1 = df1[variable].to_numpy()
 y1 = df2[variable].to_numpy() #Par_impact_nor
 x = x1[x0>-1000000]
 y = y1[y0>-1000000]   
 return x,y

#retrieving columns from dataset
xnormIP, ynormIP = retrievecolumns("Par_impact_nor")
xtheta_bte, ytheta_bte = retrievecolumns("DeltaT")
xthetaprime, ythetaprime = retrievecolumns("Angolo_cono")
xdTY, ydTY = retrievecolumns("dTY")

#target histograms
htheta_bte_MC = R.TH1D('htheta_bte_MC', '#theta_{bt}-#theta_{e} signal distribution ; #theta_{bt}-#theta_{e} [rad] ; Normalized entries', 50, np.min(xtheta_bte), np.max(xtheta_bte)+0.1)
htheta_bte_data = R.TH1D('htheta_bte_data', '#theta_{bt}-#theta_{e} signal distribution; #theta_{bt}-#theta_{e} [rad]; Normalized entries', 50, np.min(xtheta_bte), np.max(xtheta_bte)+0.1)
hthetaprime_MC = R.TH1D('hthetaprime_MC', " #theta'_{bt} signal distribution; #theta'_{bt} [rad]; Normalized entries", 50, np.min(xthetaprime), np.max(xthetaprime)+0.1)
hthetaprime_data = R.TH1D('hthetaprime_data', " #theta'_{bt} signal distribution; #theta'_{bt} [rad]; Normalized entries", 50, np.min(xthetaprime), np.max(xthetaprime)+0.1)
hnormIP_MC = R.TH1D('hnormIP_MC', 'IP/#DeltaZ signal distribution ; IP/#DeltaZ ; Normalized entries', 50, np.min(xnormIP), np.max(xnormIP)+0.1)
hnormIP_data = R.TH1D('hnormIP_data', 'IP/#DeltaZ signal distribution ; IP/#DeltaZ ; Normalized entries', 50, np.min(xnormIP), np.max(xnormIP)+0.1)
hdTY_MC = R.TH1D('hdTY_MC', 'dTY signal distribution ; dTY ; Normalized entries', 100, -0.22, 0.22)
hdTY_data = R.TH1D('hdTY_data', 'dTY signal distribution ; dTY; Normalized entries', 100, -0.22, 0.22)

cthetaprime = R.TCanvas()
ctheta_bte = R.TCanvas()
cnormIP = R.TCanvas()
cdTY = R.TCanvas()

def drawhistograms(hx,hy,x,y,c):
 '''hx is MC histogram, hy is data histogram'''

 rp.fill_hist(hy,y)
 rp.fill_hist(hx,x)

 hx.Scale(1. / hx.Integral())
 hy.Scale(1. / hy.Integral())

 hx.SetLineColor(R.kRed)
 c.cd()
 hx.Draw()
 hy.Draw('sames')

 hx.SetTitle("Simulation")
 hy.SetTitle("Data")
 c.BuildLegend()

#drawing histograms
drawhistograms(hnormIP_MC,hnormIP_data,xnormIP,ynormIP,cnormIP)
drawhistograms(htheta_bte_MC,htheta_bte_data,xtheta_bte,ytheta_bte,ctheta_bte)
drawhistograms(hthetaprime_MC,hthetaprime_data,xthetaprime,ythetaprime,cthetaprime)
drawhistograms(hdTY_MC,hdTY_data,xdTY,ydTY,cdTY)


