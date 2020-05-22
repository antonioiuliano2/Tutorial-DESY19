'''producing MC input file as required by ShowRec interface'''

import ROOT as r
import fedrarootlogon
import sys

simfile = r.TFile.Open(sys.argv[1])
simtree = simfile.Get("cbmsim")

nevents = simtree.GetEntries()

scansetfile = r.TFile.Open(sys.argv[2])
scanset = scansetfile.Get("set")

txtfilename = "BRICK.TreePGunInfo.txt"
outputfile = open(txtfilename,"w")

#get positions of a plate in FairSHIP an FEDRA references to set z offset
simtree.GetEntry(0)
emupoints = simtree.EmuDESYPoint
referencepoint = emupoints[0]

nplate = referencepoint.GetDetectorID()
zplate = referencepoint.GetZ()

zplateFEDRA = scanset.GetPlate(nplate).Z()
zoffset = zplateFEDRA - zplate*1E+4
print("offset between FEDRA and FairShip (micron)",zoffset)

def tofedracoordinates(x,y,z,zoffset):
    '''same transformations used in fromFairShip2FEDRA.C code'''
    xem = x* 1E+4 + 62500
    yem = y* 1E+4 + 49500
    zem = z* 1E+4 + zoffset #z must be the same of the scanset reference system
    return xem, yem, zem   


for ievent, event in enumerate(simtree):
    tracks = event.MCTrack
    primaryelectron = tracks[0]

    px = primaryelectron.GetPx()
    py = primaryelectron.GetPy()
    pz = primaryelectron.GetPz()
    x = primaryelectron.GetStartX()
    y = primaryelectron.GetStartY()
    z = primaryelectron.GetStartZ()


    #I need to find the vertex
    zmin = 10000
    xvertex = 0.
    yvertex = 0.

    for itrk, track in enumerate(tracks):
        if (itrk == 0):
             continue
        processID = track.GetProcID()
        pdgcode = track.GetPdgCode()
        if (processID==5 and r.TMath.Abs(pdgcode) ==11): #electron/pion from pair production
          if (track.GetStartZ() < zmin):
              zmin = track.GetStartZ()
              xvertex = track.GetStartX()
              yvertex = track.GetStartY()

    #variables to be written in TXT file
    (xvertex,yvertex,zvertex) = tofedracoordinates(xvertex,yvertex,zmin,zoffset)
 #   print("vertex for event ",MCEvent, "coordinates: ", xvertex, yvertex, zvertex)
    MCEvent = ievent
    PDGId = primaryelectron.GetPdgCode()
    dirx = 0.
    diry = 0.
    dirz = 0.
    tx = px/pz
    ty = py/pz
    (xem,yem,zem) = tofedracoordinates(x,y,z,zoffset)
    energy = primaryelectron.GetEnergy()
    tantheta = r.TMath.Sqrt(pow(tx,2) + pow(ty,2))

    outputfile.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\t{12}\t{13}\t{14}\n" \
        .format(MCEvent,energy,tantheta,dirx,diry,dirz,xvertex,yvertex,zvertex,tx,ty,xem,yem,zem,PDGId))

outputfile.close()

print ("Produced tree")
#print ("Producing tree, start testing if it is readable")
#testtree = r.TTree("mysim","Test reading tree as ShowRec will do")
#testtree.ReadFile(textfilename,"MCEvt/I:energy/F:tantheta/F:dirx/F:diry/F:dirz/F:vtxposx/F:vtxposy/F:vtxposz/F:TX/F:TY/F:X/F:Y/F:Z/F:PDGId/I")
#testtree.Print()
