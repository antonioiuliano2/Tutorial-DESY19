import numpy as np
import pandas as pd
import fedrarootlogon
import ROOT as r

def builddataframe(brick, path = "..", cutstring = "1", major = 0, minor = 0, newzprojection = None):
 """build pandas dataframe starting from couples and scanset 
    brick = Number of brick as in b0000*
    path = input path to the folder containing theb b0000* folder
    cutsring = eventual selection to couples
    newzprojection = list of projection to a new z reference system
 """
 nplate =0

 print("Reading ScanSet at path ",path)

 #reading scanset
 sproc = r.EdbScanProc()
 sproc.eProcDirClient=path
 id = r.EdbID(brick,nplate,major,minor)
 ss = sproc.ReadScanSet(id)
 ss.Brick().SetID(brick)
 
 #preparing patterns
 npl = ss.eIDS.GetEntries()

 cut = r.TCut(cutstring)

 #intial empty arrays
 IDall = np.zeros(0,dtype=int)
 PIDall = np.zeros(0,dtype=int)

 xall = np.zeros(0,dtype=np.float32)
 yall = np.zeros(0,dtype=np.float32)
 zall = np.zeros(0,dtype=np.float32)
 TXall = np.zeros(0,dtype=np.float32)
 TYall = np.zeros(0,dtype=np.float32)

 MCEvtall = np.zeros(0,dtype=int)
 MCTrackall = np.zeros(0,dtype=int)
 Pall = np.zeros(0,dtype=np.float32)
 Flagall = np.zeros(0,dtype=int)

 print ("Cut on couples ")
 cut.Print()

 print("Try to open folders at path ",path+"/b00000"+str(brick))
 for i in range(npl):
  idplate = ss.GetID(i)
      
  nplate = idplate.ePlate
  plate = ss.GetPlate(idplate.ePlate)
  #read pattern information
  p = r.EdbPattern()

  ect = r.EdbCouplesTree()
  if (nplate) <10:
   ect.InitCouplesTree("couples",path+"/b00000"+str(brick)+"/p00{}/{}.{}.{}.{}.cp.root".format(nplate,brick,nplate,major,minor),"READ")
  else:
   ect.InitCouplesTree("couples",path+"/b00000"+str(brick)+"/p0{}/{}.{}.{}.{}.cp.root".format(nplate,brick,nplate,major,minor),"READ")

  #addingcut
  ect.eCut = cut 
  cutlist = ect.InitCutList()
  
  nsegcut = cutlist.GetN()
  nseg = ect.eTree.GetEntries()

  IDarray_plate = np.zeros(nsegcut,dtype=int)
  PIDarray_plate = np.zeros(nsegcut,dtype=int)

  xarray_plate = np.zeros(nsegcut,dtype=np.float32)
  yarray_plate = np.zeros(nsegcut,dtype=np.float32)
  zarray_plate = np.zeros(nsegcut,dtype=np.float32)
  TXarray_plate = np.zeros(nsegcut,dtype=np.float32)
  TYarray_plate = np.zeros(nsegcut,dtype=np.float32)
   
  MCEvtarray_plate = np.zeros(nsegcut,dtype=int)
  MCTrackarray_plate = np.zeros(nsegcut,dtype=int)
  Parray_plate = np.zeros(nsegcut,dtype=np.float32)
  Flagarray_plate = np.zeros(nsegcut,dtype=int)

  print ("loop on {} segments over  {} for plate {}".format(nsegcut, nseg,nplate))
  for ientry in range(nsegcut):
   iseg = cutlist.GetEntry(ientry)
   ect.GetEntry(iseg)
 
   seg=ect.eS
   #//setting z and affine transformation
   seg.SetZ(plate.Z())
   seg.SetPID(i)
   seg.Transform(plate.GetAffineXY())

   if(newzprojection is not None):
    seg.PropagateTo(newzprojection[i])

   IDarray_plate[ientry] = seg.ID()
   PIDarray_plate[ientry] = seg.PID()
   
   xarray_plate[ientry] = seg.X()
   yarray_plate[ientry] = seg.Y()
   zarray_plate[ientry] = seg.Z()
   TXarray_plate[ientry] = seg.TX()
   TYarray_plate[ientry] = seg.TY()

   MCEvtarray_plate[ientry] = seg.MCEvt()
   MCTrackarray_plate[ientry] = seg.MCTrack()
   Parray_plate[ientry] = seg.P()     
   Flagarray_plate[ientry] = seg.Flag()   

  #end of loop, storing them in global arrays
  IDall = np.concatenate((IDall,IDarray_plate),axis=0)
  PIDall = np.concatenate((PIDall,PIDarray_plate),axis=0)

  xall = np.concatenate((xall,xarray_plate),axis=0)
  yall = np.concatenate((yall,yarray_plate),axis=0)
  zall = np.concatenate((zall,zarray_plate),axis=0)
  TXall = np.concatenate((TXall,TXarray_plate),axis=0)
  TYall = np.concatenate((TYall,TYarray_plate),axis=0)
  MCEvtall = np.concatenate((MCEvtall,MCEvtarray_plate),axis=0)
  MCTrackall = np.concatenate((MCTrackall,MCTrackarray_plate),axis=0)
  Pall = np.concatenate((Pall,Parray_plate),axis=0)
  Flagall = np.concatenate((Flagall,Flagarray_plate),axis=0)

 data = {'ID':IDall,'PID':PIDall,'x':xall,'y':yall,'z':zall,'TX':TXall,'TY':TYall,'MCEvent':MCEvtall,'MCTrack':MCTrackall,'P':Pall,'Flag':Flagall}
 df = pd.DataFrame(data, columns = ['ID','PID','x','y','z','TX','TY','MCEvent','MCTrack','P','Flag'] )

 return df


def addtrueMCinfo(df,simfile, ship_charm):
 '''getting additional true MC info from source file, If ship_charm is true, TM is taken into account to spread XY position'''
 import pandas as pd
 import numpy as np
 import ROOT as r
 
 simtree = simfile.Get("cbmsim")

 #position differences from FairShip2Fedra: initialized to 0
 xoffset = 0.
 yoffset = 0.
 zoffset = 0.
 #computing zoffset: in our couples, most downstream plate has always z=0
 simtree.GetEntry(0)
 emulsionhits = simtree.BoxPoint
 ihit = 0
 while (zoffset >= 0.):
  hit = emulsionhits[ihit]  
  if (hit.GetDetectorID()==29):
   zoffset = 0. - hit.GetZ()
  ihit = ihit + 1

 #virtual TM parameters (only ship-charm simulations)
 spilldy = 1
 targetmoverspeed = 2.6

 print("ZOffset between FairShip and FEDRA",zoffset) 

 df = df.sort_values(["MCEvent","MCTrack","PID"],ascending=[True,True,False]) #sorting by MCEventID allows to access each event only once
 df.reset_index()

 currentevent=-1

 nsegments = len(df)
 isegment = 0
 print("dataframe prepared, starting loop over {} segments".format(nsegments))

 #preparing arrays with new columns
 arr_MotherID = np.zeros(nsegments, dtype=int)

 arr_startX = np.zeros(nsegments,dtype=float)
 arr_startY = np.zeros(nsegments,dtype=float)
 arr_startZ = np.zeros(nsegments,dtype=float)
 
 arr_startPx = np.zeros(nsegments,dtype=float)
 arr_startPy = np.zeros(nsegments,dtype=float)
 arr_startPz = np.zeros(nsegments,dtype=float)

 for (MCEvent, MCTrack) in zip(df['MCEvent'], df['MCTrack']):

  if (MCEvent != currentevent):
   currentevent = MCEvent
   simtree.GetEntry(currentevent)
   eventtracks = simtree.MCTrack
   if(currentevent%10000 == 0):
    print("Arrived at event ",currentevent)
   #getting virtual timestamp and replicating Target Mover
   if (ship_charm):
    eventheader = simtree.ShipEventHeader
    virtualtimestamp = eventheader.GetEventTime()
    nspill = int(virtualtimestamp/100)
    pottime = virtualtimestamp - nspill * 100
    #computing xy offset for this event
    xoffset = -12.5/2. + pottime * targetmoverspeed
    yoffset = - 9.9/2. + 0.5 + nspill * spilldy 
    #print(virtualtimestamp, pottime, nspill, xoffset, yoffset)
   

  #adding values
  mytrack = eventtracks[MCTrack]
  arr_MotherID[isegment] = mytrack.GetMotherId()

  arr_startX[isegment] = (mytrack.GetStartX() + xoffset) * 1e+4 + 62500 #we need also to convert cm to micron
  arr_startY[isegment] = (mytrack.GetStartY() + yoffset) * 1e+4 + 49500
  arr_startZ[isegment] = (mytrack.GetStartZ() + zoffset) * 1e+4
  
  arr_startPx[isegment] = mytrack.GetPx()
  arr_startPy[isegment] = mytrack.GetPy()
  arr_startPz[isegment] = mytrack.GetPz()
  
  isegment = isegment + 1
 
 #adding the new columns to the dataframe
 df["MotherID"] = arr_MotherID 

 df["StartX"] = arr_startX
 df["StartY"] = arr_startY
 df["StartZ"] = arr_startZ

 df["startPx"] = arr_startPx
 df["startPy"] = arr_startPy
 df["startPz"] = arr_startPz
 
 return df

def addtrackindex(df, trackfilename):
 ''' adding track index to dataframe, if tracking was performed'''
 trackfile = r.TFile.Open(trackfilename)
 tracktree = trackfile.Get("tracks")
 
 ntracks = tracktree.GetEntries()
 #initial empty arrays, to be filled with segments from all tracks
 IDall = np.zeros(0,dtype=int)
 PIDall = np.zeros(0,dtype=int)
 TrackIDall = np.zeros(0,dtype=int)

 print("start loop on {} tracks".format(tracktree.GetEntries()))
 for track in tracktree:
  nseg = track.nseg
  segments = track.s

  #initial arrays, length given by number of segments of this tracks
  IDarr = np.zeros(nseg,dtype=int)
  PIDarr = np.zeros(nseg,dtype=int)
  TrackIDarr = np.zeros(nseg,dtype=int)

  #start loop on segments
  for iseg, seg in enumerate(segments):
   IDarr[iseg] = seg.ID()
   PIDarr[iseg] = seg.PID()
   TrackIDarr[iseg] = seg.Track()
  #concatenate, adding segments for this track to the global arrays
  IDall = np.concatenate((IDall,IDarr),axis=0)
  PIDall = np.concatenate((PIDall,PIDarr),axis=0)
  TrackIDall = np.concatenate((TrackIDall,TrackIDarr),axis=0)

 labels = ["ID","PID","TrackID"]
 dftracks = pd.DataFrame({"ID":IDall,"PID":PIDall,"TrackID":TrackIDall},columns = labels) 
 print("Track dataframe ready: merging it with all couples dataframe: not tracked segments will be labelled as NA") 
 #Now I need to merge them, however I want to keep all the segments, not only the ones which have been tracked. Luckily, there are many ways to do a merge (default is inner)
 dfwithtracks = df.merge(dftracks,how = 'left', on=["PID","ID"])
 return dfwithtracks
