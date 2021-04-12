import pandas as pd
import ROOT as r
import fedrarootlogon

#defining functions for transformation

def extractnoise(nrun,major = 0, minor = 0, segcut="eCHI2P<2.5&&s.eW>13&&eN1==1&&eN2==1&&s1.eFlag>=0&&s2.eFlag>=0"):
 '''extract couples from first 2 plates according to selection'''
 import desy19_fedrautils as desy19

 #we want to project to the z of sim, getting positions
 simzlist = []
 simsetfile = r.TFile.Open("/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/runs_360events/RUN3_uniform_26_July_2020/b000003/b000003.0.0.0.set.root") 
 simset = simsetfile.Get("set")
 for ipl in range(simset.eIDS.GetEntries()):
  simzlist.append(simset.GetPlate(simset.GetID(ipl).ePlate).Z())

 path = "/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/RUN{}_data".format(nrun)
 df = desy19.builddataframe(nrun,path,segcut, major, minor,simzlist)

 df.to_csv(path+("/b00000{}/firsttwoplates_projected.csv".format(nrun)),index = False)
 return 0

def reflectX(df0,df1):
 '''apply a reflection in X along the middle (62500)'''
 df1.drop("x",axis='columns')
 df1['x'] = 125000-df0['x']

 return df1

def reflectY(df0,df1):
 '''apply a reflection in Y along the middle (50000)'''
 df1.drop("y",axis='columns')
 df1['y'] = 100000-df0['y']

 return df1

def reflectTX(df0,df1):
 '''apply a reflection in TX along the origin'''
 df1.drop("TX",axis='columns')
 df1['TX'] = -1. * df0['TX']

 return df1

def reflectTY(df0,df1):
 '''apply a reflection in TY along the origin'''
 df1.drop("TY",axis='columns')
 df1['TY'] = -1. * df0['TY']

 return df1

def setPID(df,plateID):
 '''setplateID for dataframe df0'''
 df.drop("PID",axis='columns')
 df["PID"]=plateID 

 return df

def setZ(df,Z):
 '''setplateZ for dataframe df0'''
 df.drop("z",axis='columns')
 df["z"]=Z 

 return df

def preparedataframe_RUN3():
 '''prepare dataframe with both noise and simulation'''
 scansetfile = r.TFile.Open("/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/runs_360events/RUN3_sim_09_07_20_movingtarget/b000003/b000003.0.0.0.set.root","READ")
 scanset = scansetfile.Get("set")
 brick = scanset.eB

 print("Reading input files")

 simdf = pd.read_csv("/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/runs_360events/RUN3_uniform_26_July_2020/b000003/RUN3.csv")

 simdf["Signal"] = 1
 
 #reading dataframes from data
 ndataplates = 4 #the two first plates from two runs

 RUN1df = pd.read_csv("/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/RUN1_data_p001/b000001/firsttwoplates.csv")
 RUN3df = pd.read_csv("/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/RUN3_data_p001/b000003/firsttwoplates.csv")

 plates = []

 #duplicating dataframes for the plates of interest
 for i in range(7): # 7 copies of RUN3 first plate
  plates.append(RUN3df.query("PID==1").copy())

 for i in range(7): # 7 copies of RUN3 second plate
  plates.append(RUN3df.query("PID==0").copy())

 for i in range(7): # 7 copies of RUN1 first plate
  plates.append(RUN1df.query("PID==1").copy())

 for i in range(8): # 8 copies of RUN1 second plate
  plates.append(RUN1df.query("PID==0").copy())

 #prepared copies of dataframe, starting transforming them from runs 4 and 5
 diffplate = int(29/ndataplates) #if four dataplates, this is 7
 #every time, we set the PID and apply the transformations, they are the same for both runs so I do a loop
 print("Applying transformations to randomize datasets")
 for i in range(ndataplates):
  #plate 2
  plates[1+i*diffplate] = reflectX(plates[0+i*diffplate],plates[1+i*diffplate])
  plates[1+i*diffplate] = reflectY(plates[0+i*diffplate],plates[1+i*diffplate])
  #plate 3
  plates[2+i*diffplate] = reflectX(plates[0+i*diffplate],plates[2+i*diffplate])
  plates[2+i*diffplate] = reflectTY(plates[0+i*diffplate],plates[2+i*diffplate])
  #plate 4
  plates[3+i*diffplate] = reflectY(plates[0+i*diffplate],plates[3+i*diffplate])
  plates[3+i*diffplate] = reflectTX(plates[0+i*diffplate],plates[3+i*diffplate])
  #plate 5
  plates[4+i*diffplate] = reflectTX(plates[0+i*diffplate],plates[4+i*diffplate])
  plates[4+i*diffplate] = reflectTY(plates[0+i*diffplate],plates[4+i*diffplate])
  #plate 6
  plates[5+i*diffplate] = reflectX(plates[0+i*diffplate],plates[5+i*diffplate])
  plates[5+i*diffplate] = reflectTX(plates[0+i*diffplate],plates[5+i*diffplate])
  plates[5+i*diffplate] = reflectTY(plates[0+i*diffplate],plates[5+i*diffplate])
  #plate 7
  plates[6+i*diffplate] = reflectY(plates[0+i*diffplate],plates[6+i*diffplate])
  plates[6+i*diffplate] = reflectTX(plates[0+i*diffplate],plates[6+i*diffplate])
  plates[6+i*diffplate] = reflectTY(plates[0+i*diffplate],plates[6+i*diffplate])

 #plate 29 (only from second plate of run1)
 plates[28] = reflectX(plates[(ndataplates-1)*diffplate],plates[28])
 plates[28] = reflectY(plates[(ndataplates-1)*diffplate],plates[28])
 plates[28] = reflectTX(plates[(ndataplates-1)*diffplate],plates[28])
 plates[28] = reflectTY(plates[(ndataplates-1)*diffplate],plates[28])

 allplates = pd.DataFrame()

 print("End of transformations, set PID and Z for all plates, then merge them into the final dataframe")

 for iplate in range(29):
  plates[iplate] = setPID(plates[iplate], 28-iplate)
  plates[iplate] = setZ(plates[iplate], brick.GetPlate(28-iplate).Z())
  allplates = pd.concat([allplates,plates[iplate]])

 allplates["Signal"] = 0

 print("final merge with simulation")
 allplates = pd.concat([simdf, allplates])

 print("Dataframe ready, saving it to CSV")

 allplates.to_csv("/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/data_noise_DESY19.csv",index=False)

 return 0

def mergedataframes():
 '''merging shower sim and data dataframes'''
 simdif = pd.read_csv("/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/runs_360events/RUN3_uniform_26_July_2020/b000003/RUN3.csv_firsttenplates.csv")
 datadf = pd.read_csv("/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/RUN6_data/b000006/firsttenplates_projected.csv")

 simdf["Signal"] = 1
 datadf["Signal"] = 0

 mergeddf = pd.concat([simdf,datadf])
 mergeddf.to_csv("/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/data_noise_firsttenplates_DESY19.csv",index=False)


def preparedataframe_RUN7():
 '''tungsten run, with 1215 dz and 19 plates. We do not merge with simulation anymore at this stage'''
 scansetfile = r.TFile.Open("RUN7_sim/b000007/b000007.0.0.0.set.root","READ")
 scanset = scansetfile.Get("set")
 brick = scanset.eB

 print("Reading input files")
#reading dataframes from data
 ndataplates = 4 #the two first plates from two runs

 RUN1df = pd.read_csv("RUN1_data_p001/b000001/firsttwoplates.csv")
 RUN3df = pd.read_csv("RUN3_data_p001/b000003/firsttwoplates.csv")

 plates = []
 nplates = 19
 diffplate = int(nplates / ndataplates) #N plates with the same source
 #duplicating dataframes for the plates of interest

 for i in range(diffplate): # 7 copies of RUN3 first plate
  plates.append(RUN3df.query("PID==1").copy())

 for i in range(diffplate): # 7 copies of RUN3 second plate
  plates.append(RUN3df.query("PID==0").copy())

 for i in range(diffplate): # 7 copies of RUN1 first plate
  plates.append(RUN1df.query("PID==1").copy())

 for i in range(nplates - (3*diffplate)): # 8 copies of RUN1 second plate
  plates.append(RUN1df.query("PID==0").copy())
  print("Applying transformations to randomize datasets")
 for i in range(ndataplates):
   #plate 2
   plates[1+i*diffplate] = reflectX(plates[0+i*diffplate],plates[1+i*diffplate])
   plates[1+i*diffplate] = reflectY(plates[0+i*diffplate],plates[1+i*diffplate])
   #plate 3
   plates[2+i*diffplate] = reflectX(plates[0+i*diffplate],plates[2+i*diffplate])
   plates[2+i*diffplate] = reflectTY(plates[0+i*diffplate],plates[2+i*diffplate])
   #plate 4
   plates[3+i*diffplate] = reflectY(plates[0+i*diffplate],plates[3+i*diffplate])
   plates[3+i*diffplate] = reflectTX(plates[0+i*diffplate],plates[3+i*diffplate])
 
 #plate 16,17 and 18 with the last kind of transformation
 plates[16] = reflectTX(plates[0],plates[16])
 plates[16] = reflectTY(plates[0],plates[16])

 plates[17] = reflectTX(plates[4],plates[17])
 plates[17] = reflectTY(plates[4],plates[17])

 plates[18] = reflectTX(plates[8],plates[18])
 plates[18] = reflectTY(plates[8],plates[18])

 allplates = pd.DataFrame()

 print("End of transformations, set PID and Z for all plates, then merge them into the final dataframe")

 for iplate in range(nplates):
    plates[iplate] = setPID(plates[iplate], nplates-1-iplate)
    plates[iplate] = setZ(plates[iplate], brick.GetPlate(nplates-1-iplate).Z())
    allplates = pd.concat([allplates,plates[iplate]])

 allplates["Signal"] = 0
 allplates.to_csv("data_noise_DESY19_RUN7.csv",index=False)


def preparedataframe_RUN6():
 '''same as RUN3, but missing 14 and 17'''
 scansetfile = r.TFile.Open("RUN6_sim/b000006/b000006.0.0.0.set.root","READ")
 scanset = scansetfile.Get("set")
 brick = scanset.eB

 print("Reading input files")
#reading dataframes from data
 ndataplates = 4 #the two first plates from two runs

 RUN1df = pd.read_csv("RUN1_data_p001/b000001/firsttwoplates.csv")
 RUN3df = pd.read_csv("RUN3_data_p001/b000003/firsttwoplates.csv")

 plates = []

 #duplicating dataframes for the plates of interest
 for i in range(7): # 7 copies of RUN3 first plate
  plates.append(RUN3df.query("PID==1").copy())

 for i in range(7): # 7 copies of RUN3 second plate
  plates.append(RUN3df.query("PID==0").copy())

 for i in range(7): # 7 copies of RUN1 first plate
  plates.append(RUN1df.query("PID==1").copy())

 for i in range(8): # 8 copies of RUN1 second plate
  plates.append(RUN1df.query("PID==0").copy())

 #prepared copies of dataframe, starting transforming them from runs 4 and 5
 diffplate = int(29/ndataplates) #if four dataplates, this is 7
 #every time, we set the PID and apply the transformations, they are the same for both runs so I do a loop
 print("Applying transformations to randomize datasets")
 for i in range(ndataplates):
  #plate 2
  plates[1+i*diffplate] = reflectX(plates[0+i*diffplate],plates[1+i*diffplate])
  plates[1+i*diffplate] = reflectY(plates[0+i*diffplate],plates[1+i*diffplate])
  #plate 3
  plates[2+i*diffplate] = reflectX(plates[0+i*diffplate],plates[2+i*diffplate])
  plates[2+i*diffplate] = reflectTY(plates[0+i*diffplate],plates[2+i*diffplate])
  #plate 4
  plates[3+i*diffplate] = reflectY(plates[0+i*diffplate],plates[3+i*diffplate])
  plates[3+i*diffplate] = reflectTX(plates[0+i*diffplate],plates[3+i*diffplate])
  #plate 5
  plates[4+i*diffplate] = reflectTX(plates[0+i*diffplate],plates[4+i*diffplate])
  plates[4+i*diffplate] = reflectTY(plates[0+i*diffplate],plates[4+i*diffplate])
  #plate 6
  plates[5+i*diffplate] = reflectX(plates[0+i*diffplate],plates[5+i*diffplate])
  plates[5+i*diffplate] = reflectTX(plates[0+i*diffplate],plates[5+i*diffplate])
  plates[5+i*diffplate] = reflectTY(plates[0+i*diffplate],plates[5+i*diffplate])
  #plate 7
  plates[6+i*diffplate] = reflectY(plates[0+i*diffplate],plates[6+i*diffplate])
  plates[6+i*diffplate] = reflectTX(plates[0+i*diffplate],plates[6+i*diffplate])
  plates[6+i*diffplate] = reflectTY(plates[0+i*diffplate],plates[6+i*diffplate])

 #plate 29 (only from second plate of run1)
 plates[28] = reflectX(plates[(ndataplates-1)*diffplate],plates[28])
 plates[28] = reflectY(plates[(ndataplates-1)*diffplate],plates[28])
 plates[28] = reflectTX(plates[(ndataplates-1)*diffplate],plates[28])
 plates[28] = reflectTY(plates[(ndataplates-1)*diffplate],plates[28])

 allplates = pd.DataFrame()

 print("End of transformations, set PID and Z for all plates, then merge them into the final dataframe")
 nactualplates = 27 #we miss plates 14 and 17
 #PID go from 0 to 26
 for iplate in range(nactualplates):
  plates[iplate] = setPID(plates[iplate], nactualplates-1-iplate)
  plates[iplate] = setZ(plates[iplate], brick.GetPlate(nactualplates-1-iplate).Z())
  allplates = pd.concat([allplates,plates[iplate]])

 allplates["Signal"] = 0

 print("Dataframe ready, saving it to CSV")
 allplates.to_csv("data_noise_DESY19_RUN6.csv",index=False)

