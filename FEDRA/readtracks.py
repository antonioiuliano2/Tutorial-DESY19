'''Script to loop over tracks and segments: launch with python readtracks.py tracksfile.root'''
from ROOT import TFile, TH1D, TH2D, TCanvas
import fedrarootlogon
import sys
import numpy as np

#getting input file and tree

trkfile = TFile.Open(sys.argv[1])
trktree = trkfile.Get("tracks")

#applying our selection

seltree = trktree.CopyTree("s[0].Plate()==3 && s[0].Theta()<0.05")
#seltree1 = trktree.CopyTree("s[0].Plate()<=3 && s[0].Theta()<0.05")
print ("Over selection: ",seltree.GetEntries(), " tracks")

seltree.SetAlias("t", "t.")

#defining histograms

htheta = TH1D("htheta","Angle of track; \Theta[rad]", 50, 0, 0.05)
hPlate = TH1D("hPlate","Plate segments;# Plate",30,0,30)
hn0 = TH1D("hn0", "Holes per track; # n0", 10, 0, 10)
hnpl = TH1D("hnpl","Segments expected per track; # npl",20, 0, 20)
hnseg = TH1D("hnseg", "Segments per track; # segments", 20, 0, 20)
hX = TH1D("hX", "X Seg-Distribution; x[\mu m]", 100, 0, 125000)
hY = TH1D("hY", "Y Seg-Disribution; y[\mu m]", 100, 0, 110000)
hxy = TH2D("hxy", " xy Seg-Distribution; x[\mu m]; y[\mu m] ",50, 0, 125000, 50, 0, 110000)
htXY = TH2D("hXY","XY Tracks-Distribution; x[\mu m]; y[\mu m]", 50, 0, 125000, 50, 0 ,110000)
hT = TH1D("hT", "Angle of segments; \Theta[rad]", 50, 0, 0.05)
hplate = TH1D("hp", "Plate tracks; # Plate ", 30, 0, 30)
hXP = TH2D('hXP', "X-Plate Track-Distribution; # plate; x[\mu m]", 100, 0, 30, 1000, 0, 125000)
hXP1 = TH2D('hXP1', "X-Plate Seg-Distribution; # plate; x[\mu m]", 100, 0, 30, 1000, 0, 125000)
hXP2 = TH2D('hXP2', "X-Plate Seg-Distribution; # plate; x[\mu m]", 30, 0, 30, 100, 0, 125000)
hXPT = TH2D('hXPT', "X-Plate Seg-Distribution; # plate; x[\mu m]", 30, 0, 30, 100, 0, 125000)
#starting loop on tracks

for entry in seltree:
    track = entry.t

    nseg = entry.nseg
    n0 = entry.n0
    npl = entry.npl
 
    segments = entry.s #array of nseg elements


    htheta.Fill(track.Theta())
    htXY.Fill(track.eX, track.eY)
    if n0!=0:
       hn0.Fill(n0)
    
    hnpl.Fill(npl)
    hnseg.Fill(nseg)
    hplate.Fill(29-track.PID())
    for i in range(1,4):
        if 29-track.PID()==i:
           hXP.Fill(29-track.PID(), track.eX)
           
           #hXP.SetMarkerColor(colors[i])
           hXP.SetMarkerStyle(3)
           #hXPT.Add(hXP)
           c11 = TCanvas()
           hXP.Draw()
          
    #starting loop over segments
    for seg in segments:
        hPlate.Fill(29-seg.PID())
        hX.Fill(seg.eX)
        hY.Fill(seg.eY)
        hxy.Fill(seg.eX, seg.eY)
        Tx = seg.eTX
        Ty = seg.eTY
        ArTheta = np.sqrt(pow(Tx,2)+pow(Ty,2))
        Theta = np.arctan(ArTheta)
        hT.Fill(Theta)
        hXP1.Fill(seg.Plate(),seg.eX)
c = TCanvas()
htheta.Draw()

c1 = TCanvas()
hn0.Draw()

c2 = TCanvas()
hnpl.Draw()

c3 = TCanvas()
hnseg.Draw()

c4 = TCanvas()
hPlate.Draw()

c5 = TCanvas()
hX.Draw()

c6 = TCanvas()
hY.Draw()

c7 = TCanvas()
hxy.Draw()
hxy.SetMarkerStyle(3)

c8 = TCanvas()
htXY.Draw()
htXY.SetMarkerStyle(3)

c9 = TCanvas()
hT.Draw()

c10 = TCanvas()
hplate.Draw()

c12 = TCanvas()
hXP1.SetMarkerStyle(3)
hXP1.SetMarkerColor(9)
hXP1.Draw()

