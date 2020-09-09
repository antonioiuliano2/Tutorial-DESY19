from __future__ import division
import pandas as pd
import numpy as np
import ROOT as r

simdf = pd.read_csv("RUN3.csv")

def doevent(mcevent,df, alphalist, Rlist, nbins):
    '''acceptance and purity for event mcevent in dataframe df'''
    firstsegment = df.query("PID==28 and  MCTrack==0 and MCEvent=={}".format(mcevent))

    if len(firstsegment) != 1:
        print(len(firstsegment))
        return (0,0)

    xfirst = firstsegment["x"].to_numpy()
    yfirst = firstsegment["y"].to_numpy()
    zfirst = firstsegment["z"].to_numpy()
    TXfirst = firstsegment["TX"].to_numpy()
    TYfirst = firstsegment["TY"].to_numpy()
    #computing dR
    df["dx"] = df["x"] - xfirst[0]
    df["dy"] = df["y"] - yfirst[0]
    df["dz"] = df["z"] - zfirst[0]
    #transverse radial difference
    df["dR"] = np.sqrt(np.power(df["dx"],2) + np.power(df["dy"],2))
    #cone angle
    df["alpha"] = np.arctan(np.sqrt(np.power(df["dx"]/df["dz"],2)+np.power(df["dy"]/df["dz"],2)))

    #how many within conditions, loop on dr and alpha? For each couple, I compute efficiency and purities.
    istep = 0
    efficiency = np.zeros(nbins * nbins)
    purity = np.zeros(nbins * nbins)
    for Rmax in Rlist:
        for alphamax in alphalist:
            recodf = df.query("dR < {} and alpha < {}".format(Rmax,alphamax))
            Ntruesim = len(simdf.query("MCEvent=={}".format(mcevent)))
            Ntruereco = len(recodf.query("MCEvent=={}".format(mcevent)))
            Nallreco = len(recodf)

            efficiency[istep] = Ntruereco / Ntruesim
            purity[istep] = Ntruereco / Nallreco

            istep = istep + 1

    return (efficiency, purity)

nevents = 360

nbins = 61
alphalist = np.linspace(0.02,0.08,nbins)
Rlist = np.linspace(200,2000,nbins) #microns

allefficiencies = np.zeros(nbins * nbins)
allpurities = np.zeros(nbins*nbins)

for ievent in range(nevents):
 print("arrived at event ", ievent)
 (efficiency, purity) = doevent(ievent,simdf,alphalist, Rlist, nbins)
 allefficiencies = allefficiencies + efficiency
 allpurities = allpurities + purity
allefficiencies = allefficiencies/nevents
allpurities = allpurities/nevents
#plotting result efficiency and purity maps
effgraph = r.TGraph2D()
puritygraph = r.TGraph2D()
point = 0
for Rpoint in range(nbins):
    for alphapoint in range(nbins):
     effgraph.SetPoint(point, alphalist[alphapoint], Rlist[Rpoint], allefficiencies[point])
     puritygraph.SetPoint(point, alphalist[alphapoint], Rlist[Rpoint], allpurities[point])
     point = point + 1
c0 = r.TCanvas()
#My2DGraph->SetMarkerStyle(21); // style 21 = "full square" My2DGraph->SetMarkerSize(1.0); // size 1.0 = 8 pixels on the screen My2DGraph->Draw("PCOL"); gPad->Modified(); gPad->Update(); /

effgraph.SetTitle("Efficiency in function of cone aperture angle and cylinder radius;maximum aperture angle [rad]; maximum radius [#mu m]")
#effgraph.SetMarkerStyle(21)
#effgraph.SetMarkerSize(1.0)
#effgraph.Draw("PCOL")
effgraph.Draw("COLZ")

c1 = r.TCanvas()
puritygraph.SetTitle("Purity in function of cone aperture angle and cylinder radius;maximum aperture angle [rad]; maximum radius [#mu m]")
#puritygraph.SetMarkerStyle(21)
#puritygraph.SetMarkerSize(1.0)
#puritygraph.Draw("PCOL")
puritygraph.Draw("COLZ")