'''examples how to fill a ROOT TGraph with root numpy, from 2 arrays
   TH2D and TProfile work exactly in the same way, check fill_hist and fill_profile
'''
import ROOT as r
import numpy as np
import root_numpy


def combinevectors(arrx,arry):
 arrx = arrx[:, np.newaxis]
 arry = arry[:, np.newaxis]
 #concatenate along columns
 arrxy = np.concatenate([arrx,arry],axis=1)
 return arrxy
    
def fillgraph(graph, arrx,arry):
 arrxy = combinevectors(arrx,arry)
 root_numpy.fill_graph(graph, arrxy)

def fillprofile(profile, arrx,arry):
 arrxy = combinevectors(arrx,arry)
 root_numpy.fill_profile(profile, arrxy)

def fillhist(hist, arrx, arry):
 arrxy = combinevectors(arrx,arry)
 root_numpy.fill_hist(profile, arrxy)  

#a quick test

x = np.linspace(100,0,100)
y = x *x + 2 * x

graph = r.TGraph()

fillgraph(graph, x, y)

graph.Draw("AP*")
