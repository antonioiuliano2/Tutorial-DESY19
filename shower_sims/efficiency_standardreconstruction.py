from __future__ import division
import pandas as pd
import numpy as np
import ROOT as r
import uproot

def getdfwithpurity(mytree):
 '''not all the showers have segments from the same event: counting how many segments belong to sameevent'''
 #convert branches into numpy arrays
 nsegments = mytree.array('sizeb')
 segmentevent = mytree.array('ntrace1simub')

 sameevent = segmentevent[segmentevent[:,:] == segmentevent[:,0]] 
 NSegmentsSameEvent = np.zeros(len(nsegments),dtype = int)
 #purity = NSegmentsSameEvent/nsegments
 for i, event in enumerate(sameevent):
    NSegmentsSameEvent[i] = len(event)
 purity = NSegmentsSameEvent/nsegments
 firstsegmentevent = segmentevent[:,0] #I take the first segment from each shower

 labels = ['MCEvent','NSegments','NSegmentsSameEvent']
 #I build a dataframe, sorting it by MCEvent
 dfshower = pd.DataFrame({'NSegments':nsegments,'NSegmentsSameEvent':NSegmentsSameEvent,'MCEvent':firstsegmentevent},columns = labels)
 dfshower = dfshower.sort_values(['MCEvent','NSegments'],ascending = [True,False]) #increasing by MCEvent, decreasing by NSegments
 dfshower = dfshower.drop_duplicates('MCEvent') #only one for MCEvent

 return dfshower

def count_signaldataframe(df, nevents = 360):
  '''how many true from each event?'''
  nevents = 360
  ntruesim = np.zeros(nevents)
  events = np.linspace(1,nevents,nevents)
  for ievent in range(nevents):
    df0 = df.query("MCEvent=={}".format(ievent))
    ntruesim[ievent] = len(df0)
  return ntruesim

def eff_formula(foundevents, totalevents):
  efficiency = []; #value and error
  
  efficiency.append(float(foundevents/totalevents))

  efferr = np.sqrt(efficiency[0] * (1- efficiency[0])/totalevents)
  efficiency.append(efferr);
  
  return efficiency;


def readshower(Rpoint, alphapoint, ntruesim):
    '''getting efficiency and purity for this shower reconstruction
    Rpoint: used dR
    alphapoint: used alpha
    '''
    inputfile = uproot.open("recoshowers/radius{:.0f}alpha{:.2f}/shower1.root".format(Rpoint, alphapoint))
    recotree = inputfile["treebranch"]
    recodf = getdfwithpurity(recotree)

    Ntotrecosegments = np.sum(recodf["NSegments"])
    Ntotrecosegments_samevent = np.sum(recodf["NSegmentsSameEvent"])
    Ntottruesegments = np.sum(ntruesim)

    efficiency = eff_formula(Ntotrecosegments_samevent,Ntottruesegments)
    purity = eff_formula(Ntotrecosegments_samevent,Ntotrecosegments)
    
    return efficiency, purity

#getting total number of segments for each event
simdf = pd.read_csv("RUN3.csv")
ntruesim = count_signaldataframe(simdf)

nbinsy = 10
nbinsx = 7 

alphalist = np.linspace(0.02,0.08,nbinsx)
Rlist = np.linspace(200,2000,nbinsy) #microns

effgraph = r.TGraph2D()
puritygraph = r.TGraph2D()
point = 0
for Rpoint in Rlist:
    for alphapoint in alphalist:
     #reading shower from that folder
     efficiency, purity = readshower(Rpoint,alphapoint,ntruesim)
     effgraph.SetPoint(point, alphapoint, Rpoint, efficiency[0])
     if (Rpoint==1000 and alphapoint==0.04):
       print("For Rmax {} and alpha {} we have efficiency {} and purity {}".format(Rpoint,alphapoint,efficiency,purity))
     puritygraph.SetPoint(point, alphapoint, Rpoint, purity[0])
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
