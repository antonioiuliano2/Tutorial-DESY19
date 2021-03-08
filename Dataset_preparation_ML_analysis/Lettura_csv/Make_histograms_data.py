'''The other codes in Lettura CSV require true MC info, I am writing this one to produce histograms from data csv'''

import pandas as pd
import ROOT as r
import root_numpy as rp

minsegments = 50
histofile = r.TFile("/home/utente/Lavoro/DE19_R3/RUN3_RandomForest_histos.root","RECREATE")
#importing csv file in a dataframe, taking segments classified as true

datadf = pd.read_csv("/home/utente/Lavoro/DE19_R3/Dati_nuovo.csv")
datadf = datadf[datadf["DeltaT"].isna()==False] 
signaldf = datadf.query("Y_pred_forest_data==1")

#number of segments witin the same Ishower
sizedataset = signaldf.groupby("Ishower").count()
size = sizedataset["ID"].to_numpy()
#size = size + 1 #we need to include the injectors (not in this dataset)
goodshowers = sizedataset.query("ID>=50").index.to_numpy() #Ishower for showers with at least 50 segments

gooddf = signaldf[signaldf["Ishower"].isin(goodshowers)]

#make histograms
hsizeML = r.TH1D("hsizeML","Size of showers reconstructed by Random Forest;Nsegments", 18,0,180)
rp.fill_hist(hsizeML,size)

hIPnorm = r.TH1D("hIPnorm","Impact parameter over distance along axis;IP/#DeltaZ",30,0.,0.3)
rp.fill_hist(hIPnorm, gooddf["Par_impact_nor"].to_numpy())

hthetaprime = r.TH1D("hthetaprime","Cone angle with respect to shower start;#theta'[rad]",40,0,0.04)
rp.fill_hist(hthetaprime,gooddf["Angolo_cono"].to_numpy())

c1 = r.TCanvas()
hsizeML.Draw()

c2 = r.TCanvas()
hIPnorm.Draw()

c3 = r.TCanvas()
hthetaprime.Draw()

#write histograms to file
histofile.cd()
hsizeML.Write()
hIPnorm.Write()
hthetaprime.Write()

