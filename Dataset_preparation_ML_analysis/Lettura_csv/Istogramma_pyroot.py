import ROOT as R
import numpy as np
import root_numpy as rp
import pandas as pd

p=7
#df = pd.read_csv('/home/chiara/Scrivania/RUN3_energie/RUN3_{}GeV/Random_Forest/Prediction.csv'.format(p))
dffinale = pd.read_csv('/home/chiara/Scrivania/RUN3_energie/RUN3_{}GeV/Random_Forest/Lunghezza_sciami_ric_{}GeV.csv'.format(p,p))

del dffinale['Unnamed: 0']

c1 = R.TCanvas( 'c1', 'Histogram Drawing Options')
x = dffinale['Signal'].to_numpy()
bins = (np.max(x)-np.min(x))/(len(dffinale))
hx = R.TH1D('hs', 'Signal segments (RUN3 {} GeV); #signal segments; Entries'.format(p), 17, np.min(x), np.max(x)+5)
rp.fill_hist(hx,x)
hx.Draw()

c2 = R.TCanvas( 'c2', 'Histogram Drawing Options2')
y = dffinale['SigBack'].to_numpy()
bins = (np.max(x)-np.min(x))/(len(dffinale))
hy = R.TH1D('hsb', 'Signal segments mis-classified (RUN3 {} GeV); #signal segments mis-classified; Entries'.format(p), 17, np.min(y), np.max(y)+5)
rp.fill_hist(hy,y)
hy.Draw()


c3 = R.TCanvas( 'c3', 'Histogram Drawing Options3')
z = dffinale['BackSig'].to_numpy()
#bins = (np.max(x)-np.min(x))/(len(dffinale))
hz = R.TH1D('hbs', 'Background segments mis-classified (RUN3 {} GeV); #background segments mis-classified; Entries'.format(p), 17, np.min(z), np.max(z)+5)
rp.fill_hist(hz,z)
hz.Draw()

c4 = R.TCanvas( 'c4', 'Histogram Drawing Options4')
w = dffinale['Background'].to_numpy()
#bins = (np.max(x)-np.min(x))/(len(dffinale))
hw = R.TH1D('hb', 'Background segments (RUN3 {} GeV); #background segments (RUN3 1 GeV); Entries'.format(p), 17, np.min(w), np.max(w)+500)
rp.fill_hist(hw,w)
hw.Draw()


