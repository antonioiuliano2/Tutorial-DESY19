import ROOT as r
import pandas as pd
import fedrarootlogon
import numpy as np

mariadf = pd.read_csv("Final_result_data.csv")

dfshower = mariadf.query("Ishower==19and Y_pred_forest_data == 1")

sizeb = np.zeros(1,dtype = np.intc)
idb = dfshower["ID"].to_numpy(dtype = np.intc)
plateb = dfshower["PID"].to_numpy(dtype = np.intc) 
xb = dfshower["x"].to_numpy(dtype = np.float32)
yb = dfshower["y"].to_numpy(dtype = np.float32)
zb = dfshower["z"].to_numpy(dtype = np.float32)
txb = dfshower["TX"].to_numpy(dtype = np.float32)
tyb = dfshower["TY"].to_numpy(dtype = np.float32)

showerfile = r.TFile("shower1ml.root","RECREATE")
outputtree = r.TTree("treebranch","Shower from Maria Random Forest")
outputtree.Branch("sizeb",sizeb,"sizeb/I")
outputtree.Branch("xb",xb,"xb[sizeb]/F")
outputtree.Branch("yb",yb,"yb[sizeb]/F")
outputtree.Branch("zb",zb,"zb[sizeb]/F")
outputtree.Branch("txb",txb,"txb[sizeb]/F")
outputtree.Branch("tyb",tyb,"tyb[sizeb]/F")
outputtree.Branch("idb",idb,"idb[sizeb]/I")
outputtree.Branch("plateb",plateb,"plateb[sizeb]/I")

sizeb[0] = len(dfshower)

outputtree.Fill()
outputtree.Write()
