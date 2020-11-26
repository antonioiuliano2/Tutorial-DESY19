'''Script to loop over tracks and segments: launch with python readtracks.py tracksfile.root Shower.root'''
from ROOT import TFile, TH1D, TH2D, TCanvas, kRed
import fedrarootlogon
import sys
import numpy as np

#getting input shower file
showerfile = TFile.Open(sys.argv[2])
showertree = showerfile.Get("treebranch")

showertree.BuildIndex("plateb","idb")

#getting input file and tree

trkfile = TFile.Open(sys.argv[1])
trktree = trkfile.Get("tracks")
#trktree.BuildIndex("s[0].PID()", "s[0].ID()") #building index according to parameters

#applying our selection

#seltree = trktree.CopyTree("s[0].Plate()==3 && s[0].Theta()<0.05")
seltree = trktree.CopyTree("s[0].Plate()<=3 && s[0].Theta()<0.05")
#print ("Over selection: ",seltree.GetEntries(), " tracks")

seltree.SetAlias("t", "t.")

#defining histograms

hthetagood = TH1D("hthetagood","Angle of track; \Theta[rad]", 50, 0, 0.05)
hthetabad = TH1D("hthetabad","Angle of track; \Theta[rad]", 50, 0, 0.05)

hPlategood = TH1D("hPlategood","Plate segments;# Plate",30,0,30)
hPlatebad = TH1D("hPlatebad","Plate segments;# Plate",30,0,30)

hn0good = TH1D("hn0good", "Holes per track; # n0", 10, 0, 10)
hn0bad = TH1D("hn0bad", "Holes per track; # n0", 10, 0, 10)

hnplgood = TH1D("hnplgood","Segments expected per track; # npl",20, 0, 20)
hnplbad = TH1D("hnplbad","Segments expected per track; # npl",20, 0, 20)

hnseggood = TH1D("hnseggood", "Segments per track; # segments", 20, 0, 20)
hnsegbad = TH1D("hnsegbad", "Segments per track; # segments", 20, 0, 20)

hXgood = TH1D("hXgood", "X Seg-Distribution; x[\mu m]", 100, 0, 125000)
hXbad = TH1D("hXbad", "X Seg-Distribution; x[\mu m]", 100, 0, 125000)

hYgood = TH1D("hYgood", "Y Seg-Disribution; y[\mu m]", 100, 0, 110000)
hYbad = TH1D("hYbad", "Y Seg-Disribution; y[\mu m]", 100, 0, 110000)

hTgood = TH1D("hTgood", "Angle of segments; \Theta[rad]", 50, 0, 0.05)
hTbad = TH1D("hTbad", "Angle of segments; \Theta[rad]", 50, 0, 0.05)

hxy = TH2D("hxy", " xy Seg-Distribution; x[\mu m]; y[\mu m] ",50, 0, 125000, 50, 0, 110000)
htXY = TH2D("hXY","XY Tracks-Distribution; x[\mu m]; y[\mu m]", 50, 0, 125000, 50, 0 ,110000)

hplategood = TH1D("hpgood", "Plate tracks; # Plate ", 30, 0, 30)
hplatebad = TH1D("hpbad", "Plate tracks; # Plate ", 30, 0, 30)

hXP = TH2D('hXP', "X-Plate Track-Distribution; # plate; x[\mu m]", 100, 0, 30, 1000, 0, 125000)
hXP1 = TH2D('hXP1', "X-Plate Seg-Distribution; # plate; x[\mu m]", 100, 0, 30, 1000, 0, 125000)
hXP2 = TH2D('hXP2', "X-Plate Seg-Distribution; # plate; x[\mu m]", 30, 0, 30, 100, 0, 125000)
hXPT = TH2D('hXPT', "X-Plate Seg-Distribution; # plate; x[\mu m]", 30, 0, 30, 100, 0, 125000)

hsizeb = TH1D('sizeb',' size of reconstructed shower;sizeb',20,0,200)
#starting loop on showers

def filltrackhisto(sizeb, htrackgood, htrackbad,variable):
    minsizeb = 82
    if (sizeb >= minsizeb):
        htrackgood.Fill(variable)
    else:
        htrackbad.Fill(variable)


for trackentry in seltree:

 track = trackentry.t

 nseg = trackentry.nseg
 n0 = trackentry.n0
 npl = trackentry.npl
  
 segments = trackentry.s #array of nseg elements
 
 #selecting shower corresponding to track
 showerentry = showertree.GetEntryNumberWithIndex(segments[0].PID(),segments[0].ID())
 if (showerentry > -1):
  showertree.GetEntry(showerentry)
  sizeb = showertree.sizeb
 else:
  print ("not found shower for track ", trackentry.trid)
  sizeb = -100

 hsizeb.Fill(sizeb)

 #fill track histograms

 filltrackhisto(sizeb,hthetagood,hthetabad,track.Theta())
 #htheta.Fill(track.Theta())
 htXY.Fill(track.eX, track.eY)
 if n0!=0:
       filltrackhisto(sizeb, hn0good, hn0bad, n0)
       #hn0.Fill(n0)

 filltrackhisto(sizeb,hnplgood,hnplbad,npl)   
 #hnpl.Fill(npl)
 filltrackhisto(sizeb,hnseggood,hnsegbad,nseg)
# hnseg.Fill(nseg)
 filltrackhisto(sizeb,hplategood, hplatebad, 29 - track.PID())
 #hplate.Fill(29-track.PID())
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
        filltrackhisto(sizeb, hPlategood, hPlatebad, 29 - seg.PID())
        filltrackhisto(sizeb, hXgood, hXbad, seg.eX)
        filltrackhisto(sizeb, hYgood, hYbad, seg.eX)
        #hPlate.Fill(29-seg.PID())
        #hX.Fill(seg.eX)
        #hY.Fill(seg.eY)
        hxy.Fill(seg.eX, seg.eY)
        Tx = seg.eTX
        Ty = seg.eTY
        ArTheta = np.sqrt(pow(Tx,2)+pow(Ty,2))
        Theta = np.arctan(ArTheta)

        filltrackhisto(sizeb, hTgood, hTbad, Theta)
        #hT.Fill(Theta)
        hXP1.Fill(seg.Plate(),seg.eX)

def drawsizehisto(htrackgood, htrackbad, canvas):
    htrackbad.SetLineColor(kRed)
    htrackbad.Draw()
    htrackgood.Draw("SAMES")

c = TCanvas()
drawsizehisto(hthetagood, hthetabad, c)

c1 = TCanvas()
drawsizehisto(hn0good, hn0bad, c1)

c2 = TCanvas()
drawsizehisto(hnplgood,hnplbad, c2)

c3 = TCanvas()
drawsizehisto(hnseggood,hnsegbad,c3)

c4 = TCanvas()
drawsizehisto(hPlategood,hPlatebad, c4)

c5 = TCanvas()
drawsizehisto(hXgood,hXbad, c5)

c6 = TCanvas()
drawsizehisto(hYgood,hYbad, c6)

c7 = TCanvas()
hxy.Draw()
hxy.SetMarkerStyle(3)

c8 = TCanvas()
htXY.Draw()
htXY.SetMarkerStyle(3)

c9 = TCanvas()
drawsizehisto(hTgood, hTbad, c9)

c10 = TCanvas()
drawsizehisto(hplategood,hplatebad, c10)

c12 = TCanvas()
hXP1.SetMarkerStyle(3)
hXP1.SetMarkerColor(9)
hXP1.Draw()

c13 = TCanvas()
hsizeb.Draw()