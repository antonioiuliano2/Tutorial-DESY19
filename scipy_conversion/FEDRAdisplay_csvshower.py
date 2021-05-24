import pandas as pd
import numpy as np
import ROOT as r
import fedrarootlogon

EDAdisplay = True
data = True
prepath = "/home/utente/Lavoro/DE19_R3/RandomForest/"
#prepath = "/home/utente/Simulations/dataset_Maria/"

#importing csv file in a dataframe, taking segments classified as true


datadf = pd.read_csv(prepath+"Dati_nuovo.csv")
#datadf = pd.read_csv(prepath+"Final_dataset_RUN3_3.csv")
datadf = datadf[datadf["DeltaT"].isna()==False] 
signaldf = datadf

if data:
 signaldf = datadf.query("Y_pred_forest_data==1")
else:
 signaldf = datadf.query("Signal==1")

#requirement of minimum number of segments to acccept a shower
minsegments = 50
sizedataset = signaldf.groupby("Ishower").count()
size = sizedataset["ID"].to_numpy()
#size = size + 1 #we need to include the injectors (not in this dataset)
goodshowers = sizedataset.query("ID>={}".format(minsegments)).index.to_numpy() #Ishower for showers with at least 50 segments
print("{} showers out of {} have at least {} segments".format(len(goodshowers),len(sizedataset),minsegments))
signaldf = signaldf[signaldf["Ishower"].isin(goodshowers)]

gAli = r.EdbPVRec()
#getting columns
IDarr = signaldf["ID"].to_numpy(dtype=np.intc)
PIDarr = signaldf["PID"].to_numpy(dtype=np.intc)
xarr = signaldf["x"].to_numpy(dtype=np.float32)
yarr = signaldf["y"].to_numpy(dtype=np.float32)
zarr = signaldf["z"].to_numpy(dtype=np.float32)
TXarr = signaldf["TX"].to_numpy(dtype=np.float32)
TYarr = signaldf["TY"].to_numpy(dtype=np.float32)
MCEventarr = signaldf["MCEvent"].to_numpy(dtype=np.intc)
MCTrackarr = signaldf["MCTrack"].to_numpy(dtype=np.intc)
Parr = signaldf["P"].to_numpy(dtype=np.float32)
IShowerarr = signaldf["Ishower"].to_numpy(dtype=np.intc)

#start loop
for (ID,PID,x,y,z,TX,TY,MCEvent,MCTrack,P, IShower) in zip(IDarr,PIDarr,xarr,yarr,zarr,TXarr,TYarr,MCEventarr,MCTrackarr,Parr,IShowerarr):
  seg = r.EdbSegP(int(ID),x,y,TX,TY)
  seg.SetZ(z)
  seg.SetDZ(300)
  seg.SetPID(int(PID))
  seg.SetPlate(29-int(PID))
  if data:
     MCEvent = IShower #in real data, MCEvent has no information, but I can use it to identify showers
  seg.SetMC(int(MCEvent),int(MCTrack))
  seg.SetP(P)
  seg.SetFlag(int(IShower))
  # //EDA draws "tracks", even if they are actually segments in my cas
  # for more info see ;EdbEDAUtil::FillTracksFromPatterns(EdbPVRec *)
  track = r.EdbTrackP(seg)
  track.SetDZ(300)
  track.SetMC(int(MCEvent),int(MCTrack))
  track.AddSegment(seg)
  gAli.AddSegment(seg)
  gAli.AddTrack(track)
      
#drawing display

if (EDAdisplay):
   eda = r.EdbEDA(gAli)
   eda.SetColorMode(r.kCOLOR_BY_PARTICLE)
   eda.Run()
    
else:
   #DISPLAY OF SEGMENTS
   dsname = "Test shower reconstruction"
   ds = r.EdbDisplay(dsname,-100000.,100000.,-100000.,100000.,-40000., 0.)
   #ds.SetDrawTracks(4)
   ds.SetArrSegP(gAli.eTracks )
   ds.Draw()

def DrawIshower(ishower):
 if (not EDAdisplay):
   print("Only valid in EDA")
 else:
   segments = r.TObjArray()
   ali = eda.GetTrackSet("TS").GetPVRec()
   for ip in range(ali.Npatterns()):
    pat = ali.GetPattern(ip)
    for iseg in range(pat.N()):
     s = pat.GetSegment(iseg)
     if(s.Flag()==ishower): 
      segments.Add(s)
			
		
	
   set = eda.GetTrackSet("BT")
   set.Clear()
   set.AddSegments(segments)
	
   eda.GetTrackSet("TS").SetDraw(False)
   eda.GetTrackSet("SB").SetDraw(False)
   eda.GetTrackSet("SF").SetDraw(False)
   eda.GetTrackSet("MN").SetDraw(False)
	
   eda.Redraw()
