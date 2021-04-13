from __future__ import division 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, scatter, draw, figure, show
from scipy.optimize import curve_fit
from matplotlib import colors
from copy import copy
import ROOT as R
import root_numpy as rp
from argparse import ArgumentParser

'''
Estimate energy resolution, knowing the function,
with a gaussian on Erec - Etrue / Etrue

python Erec.py -i inputfile -n minsize -e expectedenergy
'''

parser = ArgumentParser()
parser.add_argument("-i","--inputdataset",dest="inputcsvdataset",help="input dataset with Random Forest classification (e.g. Result_data.csv)",required=True)
parser.add_argument("-n","--minsize",dest="minsize",help="minimum number of segments to accept a shower (e.g. 50)")
parser.add_argument("-e","--energy",dest="energy",help="expected value of shower energy in GeV (e.g. 6)")
options = parser.parse_args()

dffinale_data = pd.read_csv(options.inputcsvdataset)
#df = dffinale_data.query('Signal+BackSig>=50')

df = dffinale_data.query("Y_pred_forest_data==1")

sizedataset = df.groupby("Ishower").count()
size = sizedataset["ID"].to_numpy()

p0 = 0.42
p1 = 0.04
Ishower = np.unique(df['Ishower'].values)
#Ishower = [n for n in range(1080, 1082)]
dfu = pd.DataFrame()

for index, shower in enumerate(Ishower):
    print(shower)
    dft = df.groupby("Ishower").first() #only one entry per shower
    dft = dft.query('Ishower=={}'.format(shower))
   
    #x0 = dft['Signal'].values
    x0 = size[index]
    if (x0 >= int(options.minsize)):
     x = x0
 
     Erec = p1*x+p0

     #Energy_ric.append(Erec)
     dfr = dft.copy()
     dfr['Erec']=Erec
    

     sigma = (Erec-float(options.energy))/float(options.energy)
     dfr['Sigma'] = sigma
     dfu = pd.concat([dfu, dfr])


c1 = R.TCanvas( 'c1', 'Histogram Drawing Options')
x = dfu['Sigma'].to_numpy()
hx = R.TH1D('hres', '#DeltaE/E distribution; #DeltaE/E;Entries', 10, -1, 1)
rp.fill_hist(hx,x)

f1 = R.TF1('f1','gaus', -0.6, 0.6)

f1.SetParameters(20, 0, 0.25)

hx.Fit(f1)

hx.Draw()

