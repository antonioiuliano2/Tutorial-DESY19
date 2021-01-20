'''using RDataFrames to write a TTree from numpy arrays, without having to manually define branches'''
import ROOT as r
import numpy as np

def writetree(data, outputtreename, outputfilename):
 rdataframe = r.RDF.MakeNumpyDataFrame(data) #prepare a RDataFrame
 rdataframe.Snapshot(outputtreename, outputfilename)
 
#testing it

arrx = np.linspace(0,100,1000)
arry = 2 * arrx + arrx * arrx
arrz = np.sqrt(arrx)

dataset = {"x":arrx,"y":arry,"z":arrz}

writetree(dataset, "exampletree","testwriter.root")
