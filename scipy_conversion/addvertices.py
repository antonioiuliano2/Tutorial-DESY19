import pandas as pd
import desy19_fedrautils as desy19

path = "/eos/user/a/aiuliano/public/sims_fedra/CH1_pot_03_02_20/b000001/"
dfMC = pd.read_csv(path+"b000001_withtracks.csv")


print("Loaded csv, adding vertices")

#start a loop in all quarters
quarterfolders = ["firstquarter","secondquarter","thirdquarter","fourthquarter"] #names of quarter folders


dfvertices = pd.DataFrame()

whichquarter = 1

for quarterfolder in quarterfolders:

 dfvertexquarter = desy19.addvertexindex(dfMC, path+"reconstruction_output/"+quarterfolder+"/vertextree.root")
 dfvertexquarter["quarter"] = whichquarter

 dfvertices = pd.concat([dfvertices,dfvertexquarter])
 
 print("added quarter ",whichquarter)

 whichquarter = whichquarter + 1


dfwithvertices = dfMC.merge(dfvertices,how = 'left', on=["FEDRATrackID","quarter"])

dfwithvertices.to_csv(path+'b000001_withvertices.csv',index=False,na_rep="NULL") 
