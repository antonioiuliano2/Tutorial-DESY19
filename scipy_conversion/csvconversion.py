import desy19_fedrautils as desy19
import pandas as pd
import ROOT as r

def applyconversion():
 '''convert couples ROOT files into a csv'''

 df = desy19.builddataframe(1)
 
 df = df.drop("P",axis = 1)
 df = df.drop("Flag",axis=1)

 return df 

#the two steps can now be done together, without an intermediate file

simfile = r.TFile.Open("../pythia8_Geant4_1000_0.1_dig.root")
#df = pd.read_csv('b000001.csv')

df = applyconversion()

df = desy19.addtrueMCinfo(df,simfile, True)
df.to_csv('b000001.csv',index=False)


