'''load treebranch data into a pandas dataframe'''
from __future__ import division #if you use the old python2 you want the correct division

import uproot #utility to quickly convert a ROOT into a dataframe, https://github.com/scikit-hep/uproot
import numpy as np #for arrays and math operations over them
import pandas as pd #for DataFrames 
import matplotlib.pyplot as plt #for plots

myfile = uproot.open('Shower.root')

inputtree = myfile['treebranch']

def getdfwithpurity(mytree):
 '''not all the showers have segments from the same event: counting how many segments belong to sameevent'''
 #convert branches into numpy arrays
 nsegments = mytree.array('sizeb')
 segmentevent = mytree.array('ntrace1simub')

 sameevent = segmentevent[segmentevent[:,:] == segmentevent[:,0]] 
 NSegmentsSameEvent = np.zeros(len(nsegments),dtype = int)
 #purity = NSegmentsSameEvent/nsegments
 for i, event in enumerate(sameevent):
    NSegmentsSameEvent[i] = len(event)
 purity = NSegmentsSameEvent/nsegments
 firstsegmentevent = segmentevent[:,0] #I take the first segment from each shower

 labels = ['MCEvent','NSegments','NSegmentsSameEvent']
 #I build a dataframe, sorting it by MCEvent
 dfshower = pd.DataFrame({'NSegments':nsegments,'NSegmentsSameEvent':NSegmentsSameEvent,'MCEvent':firstsegmentevent},columns = labels)
 dfshower = dfshower.sort_values(['MCEvent','NSegments'],ascending = [True,False]) #increasing by MCEvent, decreasing by NSegments
 dfshower = dfshower.drop_duplicates('MCEvent') #only one for MCEvent

 return dfshower

dfshower = getdfwithpurity(inputtree)

dfshower['Purity'] = dfshower['NSegmentsSameEvent'] /dfshower['NSegments']
#now i load the csv file with the predictions
dfpredicted = pd.read_csv("Segment.csv",names=['MCEvent','NPredSegments'],header=0)

#merging the two dataframes
dfmerged = pd.merge(dfshower,dfpredicted)
#doing the ratio
dfmerged['efficiency'] = dfmerged['NSegmentsSameEvent']/dfmerged['NPredSegments']
dfmerged['efficiencyerror'] = np.sqrt(dfmerged['efficiency'] * (1 - dfmerged['efficiency'])/dfmerged['NPredSegments']) #sqrt(e*(1-e)/N)

#setting histogram 
myhist = plt.hist(dfmerged['efficiency']*100,10,[0,100])

print("We have reconstructed {} showers".format(len(dfshower)))
print("Mean efficiency:{:.3}, std efficiency:{:.3}".format(dfmerged.mean()['efficiency'], dfmerged.std()['efficiency']))

plt.title("Efficiency (NSegFound over NSegExpected)")
plt.xlabel("eff[%]")

plt.figure()
purityhist = plt.hist(dfmerged['Purity']*100,10,[0,100])
plt.title("Purity (Same MCEvent of first segment)")
plt.xlabel("purity[%]")
plt.show()