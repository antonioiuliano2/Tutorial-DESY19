from __future__ import division
from sklearn.cross_validation import train_test_split
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/runs_360events/data_noise_firsttenplates_DESY19.csv")
print("read dataframe")
df["theta"] = np.arctan(np.sqrt(np.power(df["TX"],2)+np.power(df["TY"],2)))
df["phi"] = np.arctan2(df["TY"],df["TX"])

dfsignal = df.query("Signal==1")
dfbackground = df.query("Signal==0")

#splitting in train and test both signal and test dataframes (separately)
dfsignaltrain, dfsignaltest = train_test_split(dfsignal,train_size=0.7)
dfbackgroundtrain, dfbackgroundtest = train_test_split(dfbackground,train_size=0.7)

print("Total number of segments: ",len(df))

nplates = np.max(df["PID"])+1

def triangularselection(npoints, kmin, kmax):
 '''entries under triangles'''
 eff = np.zeros(41)
 rej = np.zeros(41)
 karray = np.linspace(kmin, kmax, npoints)

 for index,k in enumerate(karray):
  dfsignal_ok = dfsignaltrain.query("theta < ({} - PID)*{}".format(nplates,k))
  dfbackground_ok = dfbackgroundtrain.query("theta < ({} - PID)*{}".format(nplates,k))
  
  eff[index] = len(dfsignal_ok)/len(dfsignaltrain)
  rej[index] = 1-len(dfbackground_ok)/len(dfbackgroundtrain)
 indecesabove = np.where(eff>0.98)
 cutvalue = karray[indecesabove[0][0]]
 print("first with eff above 98%", cutvalue)
 return cutvalue, karray, eff,rej

print("Start triangulation")
npoints = 41
kmin = 0.04
kmax = 0.08
cutvalue, karray,foundeff,foundrej = triangularselection(npoints,kmin,kmax) #what do we get from the train set?

nsegplate_sig = []
nsegplate_bkg = [] 
nsegplate_sigcut = []
nsegplate_bkgcut = [] 
dfplate = []

#how many segments per plate?
for iplate in range(nplates):

 dfplate.append(df.query("PID=={}".format(iplate)))

 nsegplate_sig.append(len(dfplate[iplate].query("Signal==1")))
 nsegplate_sigcut.append(len(dfplate[iplate].query("Signal==1 and theta < ({} - PID)*{}".format(nplates,cutvalue))))
 nsegplate_bkg.append(len(dfplate[iplate].query("Signal==0")))
 nsegplate_bkgcut.append(len(dfplate[iplate].query("Signal==0 and theta < ({} - PID)*{}".format(nplates,cutvalue))))

print ("Test Sample (30% total)")
dfsignaltest_ok = dfsignaltest.query("theta < ({} - PID)*{}".format(nplates,cutvalue))
dfbackgroundtest_ok = dfbackgroundtest.query("theta < ({} - PID)*{}".format(nplates,cutvalue))
print ("Acceptance:{}, Background rej:{}".format(len(dfsignaltest_ok)/len(dfsignaltest), 1 - len(dfbackgroundtest_ok)/len(dfbackgroundtest)))

print ("Overall")
print ("Signal dimension: before selection, {} segments, after selection, {} segments".format(np.sum(nsegplate_sig),np.sum(nsegplate_sigcut)))
print ("Background dimension: before selection, {} segments, after selection, {} segments".format(np.sum(nsegplate_bkg),np.sum(nsegplate_bkgcut)))

figeff,axeff = plt.subplots()
axeff.plot(karray,foundeff,"bo",label="efficiency")
axeff.plot(karray,foundrej,"ro", label="backgroundrej")

#we need cmin=1 to hide empty bins like ROOT hists
figtest_2d, (axtest_2d_s,axtest_2d_b) = plt.subplots(1,2)

signalpid= nplates - 1 * dfsignal["PID"]
backgroundpid =nplates - 1 * dfbackground["PID"]

histest_2d_s = axtest_2d_s.hist2d(nplates - 1 * dfsignaltest["PID"], dfsignaltest["theta"], label = "Signal",bins=[nplates,100],range=[[0,nplates],[0,1.]],cmin=1)
histest_2d_b = axtest_2d_b.hist2d(nplates - 1 * dfbackgroundtest["PID"], dfbackgroundtest["theta"], label = "Background",bins=[nplates,100],range=[[0,nplates],[0,1.]],cmin=1)
axtest_2d_s.set_xlabel("PID")
axtest_2d_s.set_ylabel("theta angle [rad]")
axtest_2d_b.set_xlabel("PID")
axtest_2d_b.set_ylabel("theta angle [rad]")

#adding lines
figtest_2d_s.colorbar(histtest_2d_s[3],ax = ax0_2d_s)
axtest_2d_s.plot([0,nplates],[0,kmin * nplates],"k--",label="k = {}".format(kmin))
axtest_2d_s.plot([0,nplates],[0,kmax * nplates],"r--",label="k = {}".format(kmax))
axtest_2d_s.plot([0,nplates],[0,cutvalue * nplates],"b",label="k = {}".format(cutvalue))
figtest_2d_b.colorbar(histtest_2d_b[3],ax = ax0_2d_b)
axtest_2d_b.plot([0,nplates],[0,kmin * nplates],"k--",label="k = {}".format(kmin))
axtest_2d_b.plot([0,nplates],[0,kmax * nplates],"r--",label="k = {}".format(kmax))
axtest_2d_b.plot([0,nplates],[0,cutvalue * nplates],"b",label="k = {}".format(cutvalue))

axtest_2d_s.legend()
#we need cmin=1 to hide empty bins like ROOT hists
fig0_2d, (ax0_2d_s,ax0_2d_b) = plt.subplots(1,2)

hist0_2d_s = ax0_2d_s.hist2d(signalpid, df.query("Signal==1")["theta"], label = "Signal",bins=[nplates,100],range=[[0,nplates],[0,1.]],cmin=1)
hist0_2d_b = ax0_2d_b.hist2d(backgroundpid, df.query("Signal==0")["theta"], label = "Background",bins=[nplates,100],range=[[0,nplates],[0,1.]],cmin=1)

ax0_2d_s.set_xlabel("PID")
ax0_2d_s.set_ylabel("theta angle [rad]")
ax0_2d_b.set_xlabel("PID")
ax0_2d_b.set_ylabel("theta angle [rad]")

#adding lines
fig0_2d_s.colorbar(hist0_2d_s[3],ax = ax0_2d_s)
ax0_2d_s.plot([0,nplates],[0,kmin * nplates],"k--",label="k = {}".format(kmin))
ax0_2d_s.plot([0,nplates],[0,kmax * nplates],"r--",label="k = {}".format(kmax))
ax0_2d_s.plot([0,nplates],[0,cutvalue * nplates],"b",label="k = {}".format(cutvalue))
fig0_2d_b.colorbar(hist0_2d_b[3],ax = ax0_2d_b)
ax0_2d_b.plot([0,nplates],[0,kmin * nplates],"k--",label="k = {}".format(kmin))
ax0_2d_b.plot([0,nplates],[0,kmax * nplates],"r--",label="k = {}".format(kmax))
ax0_2d_b.plot([0,nplates],[0,cutvalue * nplates],"b",label="k = {}".format(cutvalue))

ax0_2d_s.legend()
ax0_2d_b.legend()

#we need cmin=1 to hide empty bins like ROOT hists
fig2d, (ax2d_s,ax2d_b) = plt.subplots(1,2)
ax2d_s.hist2d(df.query("Signal==1")["theta"], df.query("Signal==1")["phi"], label = "Signal",bins=[100,300],range=[[0,1.],[-1.5,1.5]],cmin=1)
ax2d_b.hist2d(df.query("Signal==0")["theta"], df.query("Signal==0")["phi"], label = "Background",bins=[100,300],range=[[0,1.],[-1.5,1.5]],cmin=1)
ax2d_s.set_xlabel("$\theta$ angle [rad]")
ax2d_s.set_ylabel("$\phi$ angle [rad]")
ax2d_b.set_xlabel("$\theta$ angle [rad]")
ax2d_b.set_ylabel("$\phi$ angle [rad]")

fig0, (ax0,ax01) = plt.subplots(1,2)
ax0.hist(df.query("Signal==1")["theta"], density = True, alpha = 0.5, label = "Signal",bins=100,range=[0,1])
ax0.hist(df.query("Signal==0")["theta"], density = True, alpha = 0.5, label = "Background",bins=100,range=[0,1])
ax0.set_xlabel("$\theta$ angle [rad]")
ax01.hist(df.query("Signal==1")["phi"], density = True, alpha = 0.5, label = "Signal",bins=100,range=[-3,3])
ax01.hist(df.query("Signal==0")["phi"], density = True, alpha = 0.5, label = "Background",bins=100,range=[-3,3])
ax01.set_xlabel("$\phi$ angle [rad]")

ax0.legend()
ax01.legend()

fig1,ax1 = plt.subplots()

ax1.plot(nsegplate_sig,"b*",label="Number of signal segments")
ax1.plot(nsegplate_sigcut,"bo",label="Number of signal segments with angle selection")
ax1.plot(nsegplate_bkg,"r*",label="Number of background segments")
ax1.plot(nsegplate_bkgcut,"ro",label="Number of background segments with angle selection")
ax1.set_xlabel("PID")
ax1.set_ylabel("nsegments")
ax1.set_yscale('log')

ax1.legend()


'''
#showing plots of changed variables
fig2,(ax21,ax22) = plt.subplots(1,2)
ax21.hist(dfplate[21]["TY"],bins=300,range=(-1.5,1.5))
ax22.hist(dfplate[19]["TY"],bins=300,range=(-1.5,1.5))
ax21.set_label("Original")
ax21.set_xlabel("$TY$")
ax22.set_label("Transformed")
ax22.set_xlabel("$TY$")

fig3,(ax31,ax32) = plt.subplots(1,2)
ax31.hist(dfplate[21]["TX"],bins=300,range=(-1.5,1.5))
ax32.hist(dfplate[18]["TX"],bins=300,range=(-1.5,1.5))
ax31.set_label("Original")
ax31.set_xlabel("$TX$")
ax32.set_label("Transformed")
ax32.set_xlabel("$TX$")

fig4,(ax41,ax42) = plt.subplots(1,2)
ax41.hist(dfplate[21]["x"],bins=125,range=(0,125000))
ax42.hist(dfplate[20]["x"],bins=125,range=(0,125000))
ax41.set_label("Original")
ax41.set_xlabel("X[$\mu m$]")
ax42.set_xlabel("X[$\mu m$]")
ax42.set_label("Transformed")

fig5,(ax51,ax52) = plt.subplots(1,2)
ax51.hist(dfplate[21]["y"],bins=100,range=(0,100000))
ax52.hist(dfplate[20]["y"],bins=100,range=(0,100000))
ax51.set_label("Original")
ax51.set_xlabel("Y[$\mu m$]")
ax52.set_xlabel("Y[$\mu m$]")
ax52.set_label("Transformed")
'''
plt.show()


 
