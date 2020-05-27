import numpy as np
import pandas as pd
import fedrarootlogon
import ROOT as r

def builddataframe(brick, cutstring = "1"):
 """build pandas dataframe starting from couples and scanset """
 nplate =0;
 major = 0;
 minor = 0;

 #reading scanset
 sproc = r.EdbScanProc();
 sproc.eProcDirClient="..";
 id = r.EdbID(brick,nplate,major,minor);
 ss = sproc.ReadScanSet(id);
 ss.Brick().SetID(brick);
 
 #preparing patterns
 npl = ss.eIDS.GetEntries();

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

 for i in range(npl):
  idplate = ss.GetID(i);
      
  nplate = idplate.ePlate
  plate = ss.GetPlate(idplate.ePlate);
  #read pattern information
  p = r.EdbPattern();

  ect = r.EdbCouplesTree();
  if (nplate) <10:
   ect.InitCouplesTree("couples","p00{}/{}.{}.0.0.cp.root".format(nplate,brick,nplate),"READ")
  else:
   ect.InitCouplesTree("couples","p0{}/{}.{}.0.0.cp.root".format(nplate,brick,nplate),"READ")
  
  nseg = ect.eTree.GetEntries();

  IDarray_plate = np.zeros(nseg,dtype=int)
  PIDarray_plate = np.zeros(nseg,dtype=int)

  xarray_plate = np.zeros(nseg,dtype=np.float32)
  yarray_plate = np.zeros(nseg,dtype=np.float32)
  zarray_plate = np.zeros(nseg,dtype=np.float32)
  TXarray_plate = np.zeros(nseg,dtype=np.float32)
  TYarray_plate = np.zeros(nseg,dtype=np.float32)
   
  MCEvtarray_plate = np.zeros(nseg,dtype=int)
  MCTrackarray_plate = np.zeros(nseg,dtype=int)
  Parray_plate = np.zeros(nseg,dtype=np.float32)
  Flagarray_plate = np.zeros(nseg,dtype=int)

  print ("loop over {} segments for plate {}".format(nseg,nplate))
  for iseg in range(nseg):
   #igoodsegment = goodcouples.GetEntry(iseg);
   ect.GetEntry(iseg);
 
   seg=ect.eS
   #//setting z and affine transformation
   seg.SetZ(plate.Z());
   seg.SetPID(i)
   seg.Transform(plate.GetAffineXY());

   #sproc.ReadPatCPnopar(p,idplate,cut);
   #p.SetZ(plate.Z());
   #p.SetSegmentsZ();
   #p.SetID(i);
   #p.SetPID(i);
   #p.SetSegmentsPID();
   #plate->Print();
   #p.Transform(    plate.GetAffineXY()   );
   #p.TransformShr( plate.Shr() );
   #p.TransformA(   plate.GetAffineTXTY() );
   #p.SetSegmentsPlate(idplate.ePlate);


   IDarray_plate[iseg] = seg.ID();
   PIDarray_plate[iseg] = seg.PID();
   
   xarray_plate[iseg] = seg.X();
   yarray_plate[iseg] = seg.Y();
   zarray_plate[iseg] = seg.Z();
   TXarray_plate[iseg] = seg.TX();
   TYarray_plate[iseg] = seg.TY();

   MCEvtarray_plate[iseg] = seg.MCEvt();
   MCTrackarray_plate[iseg] = seg.MCTrack();
   Parray_plate[iseg] = seg.P();          
   Flagarray_plate[iseg] = seg.Flag();   

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


def addtrueMCinfo(df,simfile):
 '''getting additional true MC info from source file'''
 import pandas as pd
 import numpy as np
 import ROOT as r
 
 simtree = simfile.Get("cbmsim")

 zoffset = 0.
 #computing zoffset: in our couples, most downstream plate has always z=0
 simtree.GetEntry(0)
 emulsionhits = simtree.BoxPoint
 ihit = 0
 while (zoffset >= 0.):
  hit = emulsionhits[ihit]  
  if (hit.GetDetectorID()==29):
   zoffset = 0. - (hit.GetZ() *1e+4) #we need also to convert from cm to micron
  ihit = ihit + 1

 print("ZOffset between FairShip and FEDRA",zoffset) 

 df = df.sort_values(["MCEvent","MCTrack"]) #sorting by MCEventID allows to access each event only once
 df.reset_index()

 currentevent=-1

 nsegments = len(df)
 isegment = 0
 print("dataframe prepared, starting loop over {} segments".format(nsegments))

 #preparing arrays with new columns
 arr_MotherID = np.zeros(nsegments, dtype=int)

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

  #adding values
  mytrack = eventtracks[MCTrack]
  arr_MotherID[isegment] = mytrack.GetMotherId()

  arr_startZ[isegment] = mytrack.GetStartZ()*1e+4 + zoffset
  
  arr_startPx[isegment] = mytrack.GetPx()
  arr_startPy[isegment] = mytrack.GetPy()
  arr_startPz[isegment] = mytrack.GetPz()
  
  isegment = isegment + 1
 
 #adding the new columns to the dataframe
 df["MotherID"] = arr_MotherID 

 df["StartZ"] = arr_startZ

 df["startPx"] = arr_startPx
 df["startPy"] = arr_startPy
 df["startPz"] = arr_startPz
 
 return df

def addtrackindex(df, trackfilename):
 trackfile = r.TFile.Open(trackfilename)
 tracktree = trackfile.Get("tracks")
 df["TrackID"]=-1
 df["nseg"]=-1
 df=df.groupby(["PID","ID"]).first()
 print("start loop on {} tracks".format(tracktree.GetEntries()))
 for track in tracktree:
  segments = track.s
  nseg = track.nseg
  trid = track.trid
  #start loop on segments
  for seg in segments:
   df.loc[(seg.PID(),seg.ID()),"TrackID"] = trid  
   df.loc[(seg.PID(),seg.ID()),"nseg"] = nseg 
   x = 0
 print("Speed test done")
 return df
