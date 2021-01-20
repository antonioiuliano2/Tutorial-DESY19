'''we need to add track IDS to the MC CSV'''

import pandas as pd
import desy19_fedrautils as desy19

#setting paths and reading csv input

path="/eos/user/a/aiuliano/public/sims_fedra/CH1_pot_03_02_20/b000001/"

dfMC = pd.read_csv(path+"b000001.csv")

print("Loaded csv, adding tracks")

#start a loop in all quarters
quarterfolders = ["firstquarter","secondquarter","thirdquarter","fourthquarter"] #names of quarter folders

dftracks = pd.DataFrame()

whichquarter = 1

for quarterfolder in quarterfolders:

 dftracksquarter = desy19.addtrackindex(dfMC, path+"reconstruction_output/"+quarterfolder+"/linked_tracks.root")
 dftracksquarter["quarter"] = whichquarter #due to more separate track files, I need to a variable to tell me which file to look for

 dftracks = pd.concat([dftracks,dftracksquarter])
 
 print("added quarter ",whichquarter)

 whichquarter = whichquarter + 1


dfwithtracks = dfMC.merge(dftracks,how = 'left', on=["PID","ID"])

dfwithtracks.to_csv(path+'b000001_withtracks_v2.csv',index=False,na_rep="NULL") 
  
