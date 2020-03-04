#build a simplified global tree with all couples positions and angles, stored as numpy arrays
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import pandas as pd
import fedrarootlogon
import ROOT as r
import sys
import desy19_fedrautils as utils

df = utils.builddataframe(5)

withtrackinfo = False #if True, loop over tracks to find which dataframe segments are contained. Currently very slow, not Python-like

if withtrackinfo:
 print("Dataframe ready, now adding track information")
 df = utils.addtrackindex(df,"b000005.0.0.0.trk.root")

#now adding shower info 
nevent = 274 #Number of MCEvent to display at the start

#getting reconstructed shower for that event
inputfile = r.TFile(sys.argv[1])
inputtree = inputfile.Get("treebranch_0")
inputtree.BuildIndex("ntrace1simub[0]") #it has sense only if one shower per event has been defined


def computelines(reduceddf):
 '''compute lines for angles'''
 dz = 300
 #first, we need to compute start points and end points to draw lines
 reduceddf["startx"] = reduceddf["x"]-reduceddf["TX"]*dz/2.
 reduceddf["endx"] =  reduceddf["x"]+ reduceddf["TX"]*dz/2.

 reduceddf["starty"] = reduceddf["y"] - reduceddf["TY"]*dz/2.
 reduceddf["endy"] = reduceddf["y"]+ reduceddf["TY"]*dz/2.
  
 reduceddf["startz"] = reduceddf["z"]-dz/2.
 reduceddf["endz"] = reduceddf["z"]+dz/2.
 #converting from pandas to numpy arrays and building the lines
 linexz = (reduceddf[["startz","startx","endz","endx"]]).to_numpy()
 lineyz = (reduceddf[["startz","starty","endz","endy"]]).to_numpy()

 #lines = [[(0, 1), (1, 1)], [(2, 3), (3, 3)], [(1, 2), (1, 3)]]
 newlinexz = []
 newlineyz = []
 for i in range(len(reduceddf)):
  newlinexz.append([(linexz[i,0],linexz[i,1]),(linexz[i,2],linexz[i,3])])
  newlineyz.append([(lineyz[i,0],lineyz[i,1]),(lineyz[i,2],lineyz[i,3])])

 lcxz = LineCollection(newlinexz)
 lcyz = LineCollection(newlineyz)
 #returning the lines to be drawn
 return lcxz, lcyz

def getshowernr(mcevent):
 '''get number of shower for MCEvent.
    It has sense only if one shower per event has been defined
    Otherwise, we cannot know what shower will be chosen
 '''

 return inputtree.GetEntryNumberWithIndex(mcevent)

def displayshowers(nshower,nevents = 300):
 '''compare display of segments from MCEvent nevent
    with reconstructed segments from nshower
 '''
 #getting containers of found couples from tree
 inputtree.GetEntry(nshower)
 idfoundlist= inputtree.idb
 xbfoundlist = inputtree.xb
 ybfoundlist = inputtree.yb
 zbfoundlist = inputtree.zb
 platebfoundlist = inputtree.plateb
 mceventlist = inputtree.ntrace1simub

 nsegmentsxevent = {}
 #initializing to zero
 for i in range(nevents):
  nsegmentsxevent[i] = 0
 #finding most common event
 for event in mceventlist:
  nsegmentsxevent[event] = nsegmentsxevent[event] + 1

 maxsegments = 0
 mostcommnevent = -1
 for i in range(nevents):
  if nsegmentsxevent[i] > maxsegments:
   maxsegments = nsegmentsxevent[i]
   mostcommonevent = i

 dfevent = df.query("MCEvent=={}".format(mostcommonevent))
 dfevent = dfevent.reset_index() #resetting the index, allows indexing from 0

 print("Display shower for event{}".format(mostcommonevent))

 dfevent["Found"] = False
 #checking if a segment from that event was found, according to ID and PID. Again, unfortunately still done with a loop due to my inexperience
 for i in range(len(dfevent)):
  if (dfevent.loc[i,"ID"],dfevent.loc[i,"PID"]) in zip(idfoundlist,platebfoundlist):
   dfevent.loc[i,"Found"] = True
 #do the plots
 dfevent_onlyfound = dfevent.query("Found == True")
 dfevent_onlymissing = dfevent.query("Found == False")

 (lcxz,lcyz) = computelines(dfevent)
 #draw projections, for missing and found segments
 figzy,ax_yz = plt.subplots()
 ax_yz.plot(dfevent_onlymissing['z'], dfevent_onlymissing['y'],"ro",fillstyle="none",label="missing segments")
 ax_yz.plot(zbfoundlist, ybfoundlist,"bo",fillstyle="none",label="found segments")
 plt.title("zy projection")
 plt.xlabel("z[micron]")
 plt.ylabel("y[micron]")
 plt.legend()
 ax_yz.add_collection(lcyz)

 figzx,ax = plt.subplots()
 ax.plot(dfevent_onlymissing['z'], dfevent_onlymissing['x'],"ro",fillstyle="none",label="missing segments")
 ax.plot(zbfoundlist, xbfoundlist,"bo",fillstyle="none",label="found segments")
 plt.title("zx projection")
 plt.xlabel("z[micron]")
 plt.ylabel("x[micron]")
 plt.legend()
 ax.add_collection(lcxz)

 figzy.show()
 figzx.show()
 
 return dfevent

def displaytrack(ntrack):
 '''launch df=utils.addtrackindex(df,trackfilename) before 
    executing this function
 '''
 dftrack = df.query("TrackID=={}".format(ntrack))
 dftrack = dftrack.reset_index() #resetting the index, allows indexing from 0

 (lcxz,lcyz) = computelines(dftrack)
 #draw projections for segments from this track
 figzy,ax_yz = plt.subplots()
 ax_yz.plot(dftrack['z'], dftrack['y'],"ro",fillstyle="none",label="track segments")
 plt.title("zy projection")
 plt.xlabel("z[micron]")
 plt.ylabel("y[micron]")
 ax_yz.add_collection(lcyz)

 figzx,ax = plt.subplots()
 ax.plot(dftrack['z'], dftrack['x'],"ro",fillstyle="none",label="track segments")
 plt.title("zx projection")
 plt.xlabel("z[micron]")
 plt.ylabel("x[micron]")

 figzy.show()
 figzx.show()
 ax.add_collection(lcxz)

dfevent = displayshowers(50)

