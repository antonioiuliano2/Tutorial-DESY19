'''The other codes in Lettura CSV require true MC info, I am writing this one to produce histograms from data csv'''

import pandas as pd
import ROOT as r
import root_numpy as rp

minsegments = 50

prepath = "/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/RUN6_dataML/RandomForest/"

histofile = r.TFile(prepath+"RandomForest_histos.root","RECREATE")
#importing csv file in a dataframe, taking segments classified as true

datadf = pd.read_csv(prepath+"Result_data.csv")
datadf = datadf[datadf["DeltaT"].isna()==False] 
signaldf = datadf.query("Y_pred_forest_data==1")

#number of segments witin the same Ishower
sizedataset = signaldf.groupby("Ishower").count()
size = sizedataset["ID"].to_numpy()
#size = size + 1 #we need to include the injectors (not in this dataset)
goodshowers = sizedataset.query("ID>={}".format(minsegments)).index.to_numpy() #Ishower for showers with at least 50 segments

print("{} showers have at least {} segments".format(len(goodshowers),minsegments))

gooddf = signaldf[signaldf["Ishower"].isin(goodshowers)]

#make histograms
hsizeML = r.TH1D("hsizeML","Size of showers reconstructed by Random Forest;Nsegments", 20,0,200)
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

