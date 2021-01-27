import uproot
import numpy as np
import pandas as pd

inputfile = uproot.open("shower1.root")
inputtree = inputfile["treebranch"]
#defining branches to read
idb = inputtree.array("idb")
plateb = inputtree.array("plateb")
xb = inputtree.array("xb")
yb = inputtree.array("yb")
zb = inputtree.array("zb")
txb = inputtree.array("txb")
tyb = inputtree.array("tyb")
sizeb = inputtree.array("sizeb")

#total array to be stored
idbtotal = np.zeros(0,dtype = np.int32)
platebtotal = np.zeros(0,dtype = np.int32)
xbtotal = np.zeros(0,dtype = np.float32)
ybtotal = np.zeros(0,dtype = np.float32)
zbtotal = np.zeros(0,dtype = np.float32)
txbtotal = np.zeros(0,dtype = np.float32)
tybtotal = np.zeros(0,dtype = np.float32)
Ishowertotal = np.zeros(0,dtype = np.int32)

mariashowers = [10,19,25,45,77,93,95,96,115,117,118,122,126,133,148,159,168]
myshowers = [158,146,143,123,91,75,73,72,12,52,51,47,43,36,23,12,3]

Ishowerdict = dict(zip(myshowers, mariashowers))

for key in Ishowerdict:
   #getting values from tree for this entry, adding them to total
   idbtotal = np.concatenate([idbtotal,idb[key]],axis = 0)
   platebtotal = np.concatenate([platebtotal,plateb[key]],axis = 0)
   xbtotal = np.concatenate([xbtotal,xb[key]],axis = 0)
   ybtotal = np.concatenate([ybtotal,yb[key]],axis = 0)
   zbtotal = np.concatenate([zbtotal,zb[key]],axis = 0)
   txbtotal = np.concatenate([txbtotal,txb[key]],axis = 0)
   tybtotal = np.concatenate([tybtotal,tyb[key]],axis = 0)
   #adding Ishower
   Ishower = np.zeros(sizeb[key],dtype = np.int32)
   Ishower[:] = Ishowerdict[key]
   Ishowertotal = np.concatenate([Ishowertotal,Ishower],axis = 0)

#arrays ready, making dataframe and saving it as csv for Maria
data = {"ID":idbtotal,"PID":platebtotal,"x":xbtotal,"y":ybtotal,"z":zbtotal,"TX":txbtotal,"TY":tybtotal,"Ishower":Ishowertotal}
df = pd.DataFrame(data, columns = ["ID","PID","x","y","z","TX","TY","Ishower"])

df.to_csv("standard_reconstruction_showers.csv",index = False)

