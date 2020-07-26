import pandas as pd
import ROOT as r
import fedrarootlogon

#defining functions for transformation

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
#Get EdbScanSet for z positions from simulation
scansetfile = r.TFile.Open("/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/runs_360events/RUN3_sim_09_07_20_movingtarget/b000003/b000003.0.0.0.set.root","READ")
scanset = scansetfile.Get("set")
brick = scanset.eB

simdf = pd.read_csv("/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/runs_360events/RUN3_uniform_26_July_2020/b000003/RUN3.csv")

simdf["Signal"] = 1

plates = []

plates.append(pd.read_csv("/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/RUN5_data_p001/b000005/first_plate.csv")) #plate[0] is run 4 first plate

for i in range(14):
 plates.append(plates[0].copy())

plates.append(pd.read_csv("/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/RUN1_data_p001/b000001/first_plate.csv")) #plate[15] is run5 first plate

for i in range(13):
 plates.append(plates[15].copy())


#prepared copies of dataframe, starting transforming them from runs 4 and 5
diffplate = 15
#every time, we set the PID and apply the transformations, they are the same for both runs so I do a loop
for i in range(2):
 #plate 2
 plates[1+i*diffplate] = reflectX(plates[0+i*diffplate],plates[1+i*diffplate])
 #plate 3
 plates[2+i*diffplate] = reflectY(plates[0+i*diffplate],plates[2+i*diffplate])
 #plate 4
 plates[3+i*diffplate] = reflectTX(plates[0+i*diffplate],plates[3+i*diffplate])
 #plate 5
 plates[4+i*diffplate] = reflectTY(plates[0+i*diffplate],plates[4+i*diffplate])
 #plate 6
 plates[5+i*diffplate] = reflectX(plates[0+i*diffplate],plates[5+i*diffplate])
 plates[5+i*diffplate] = reflectY(plates[0+i*diffplate],plates[5+i*diffplate])
 #plate 7
 plates[6+i*diffplate] = reflectX(plates[0+i*diffplate],plates[6+i*diffplate])
 plates[6+i*diffplate] = reflectTX(plates[0+i*diffplate],plates[6+i*diffplate])
 #plate 8
 plates[7+i*diffplate] = reflectX(plates[0+i*diffplate],plates[7+i*diffplate])
 plates[7+i*diffplate] = reflectTY(plates[0+i*diffplate],plates[7+i*diffplate])
 #plate 9
 plates[8+i*diffplate] = reflectY(plates[0+i*diffplate],plates[8+i*diffplate])
 plates[8+i*diffplate] = reflectTX(plates[0+i*diffplate],plates[8+i*diffplate])
 #plate 10
 plates[9+i*diffplate] = reflectY(plates[0+i*diffplate],plates[9+i*diffplate])
 plates[9+i*diffplate] = reflectTY(plates[0+i*diffplate],plates[9+i*diffplate])
 #plate 11
 plates[10+i*diffplate] = reflectTX(plates[0+i*diffplate],plates[10+i*diffplate])
 plates[10+i*diffplate] = reflectTY(plates[0+i*diffplate],plates[10+i*diffplate])
 #plate 12
 plates[11+i*diffplate] = reflectX(plates[0+i*diffplate],plates[11+i*diffplate])
 plates[11+i*diffplate] = reflectY(plates[0+i*diffplate],plates[11+i*diffplate])
 plates[11+i*diffplate] = reflectTX(plates[0+i*diffplate],plates[11+i*diffplate])
 #plate 13
 plates[12+i*diffplate] = reflectX(plates[0+i*diffplate],plates[12+i*diffplate])
 plates[12+i*diffplate] = reflectY(plates[0+i*diffplate],plates[12+i*diffplate])
 plates[12+i*diffplate] = reflectTY(plates[0+i*diffplate],plates[12+i*diffplate])
 #plate 14
 plates[13+i*diffplate] = reflectX(plates[0+i*diffplate],plates[13+i*diffplate])
 plates[13+i*diffplate] = reflectTX(plates[0+i*diffplate],plates[13+i*diffplate])
 plates[13+i*diffplate] = reflectTY(plates[0+i*diffplate],plates[13+i*diffplate])

#plate 15 (only from run4
plates[14] = reflectY(plates[0],plates[14])
plates[14] = reflectTX(plates[0],plates[14])
plates[14] = reflectTY(plates[0],plates[14])

allplates = pd.DataFrame()
#set PID and Z for all plates, then merge them into the final dataframe

for iplate in range(29):
 plates[iplate] = setPID(plates[iplate], 28-iplate)
 plates[iplate] = setZ(plates[iplate], brick.GetPlate(iplate).Z())
 allplates = pd.concat([allplates,plates[iplate]])

allplates["Signal"] = 0

#merging with simulation
allplates = pd.concat([simdf, allplates])

allplates.to_csv("/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/data_noise_DESY19.csv",index=False)

