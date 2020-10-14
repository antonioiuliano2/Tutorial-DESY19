'''Script to loop over tracks and segments: launch with python readtracks.py tracksfile.root'''
from ROOT import TFile, TH1D, TH2D, TCanvas
import fedrarootlogon
import sys

#getting input file and tree

trkfile = TFile.Open(sys.argv[1])
trktree = trkfile.Get("tracks")

#applying our selection

seltree = trktree.CopyTree("s[0].Plate()<4 && s[0].Theta()<0.05")

print ("Over selection: ",seltree.GetEntries(), " tracks")

seltree.SetAlias("t", "t.")

#defining histograms

htheta = TH1D("htheta","Angle of track", 50, 0, 0.05)
hPlate = TH1D("hPlate","Plate number;# Plate",29,1,30)
##hxy = TH2D("hxy", " x y ",)


#starting loop on tracks

for entry in seltree:
    track = entry.t

    nseg = entry.nseg

    segments = entry.s #array of nseg elements


    htheta.Fill(track.Theta())
    #starting loop over segments
    for seg in segments:
        hPlate.Fill(29-seg.PID())

c = TCanvas()
htheta.Draw()

c1 = TCanvas()
hPlate.Draw()