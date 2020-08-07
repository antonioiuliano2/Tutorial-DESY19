import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/runs_360events/data_noise_firsttenplates_DESY19.csv")
print("read dataframe")
df["theta"] = np.sqrt(np.power(df["TX"],2)+np.power(df["TY"],2))
df["phi"] = np.arctan2(df["TY"],df["TX"])
print("Total number of segments: ",len(df))

nplates = 10

nsegplate_sig = []
nsegplate_bkg = [] 
nsegplate_sigcut = []
nsegplate_bkgcut = [] 
dfplate = []

#how many segments per plate?
for iplate in range(nplates):

 dfplate.append(df.query("PID=={}".format(iplate)))

 nsegplate_sig.append(len(dfplate[iplate].query("Signal==1")))
 nsegplate_sigcut.append(len(dfplate[iplate].query("Signal==1 and theta<0.4")))
 nsegplate_bkg.append(len(dfplate[iplate].query("Signal==0")))
 nsegplate_bkgcut.append(len(dfplate[iplate].query("Signal==0 and theta<0.4")))

fig0, (ax0,ax01) = plt.subplots(1,2)
ax0.hist(df.query("Signal==1")["theta"], density = True, alpha = 0.5, label = "Signal",bins=200,range=[0,1])
ax0.hist(df.query("Signal==0")["theta"], density = True, alpha = 0.5, label = "Background",bins=200,range=[0,1])
ax0.set_xlabel("$\theta$ angle [rad]")
ax01.hist(df.query("Signal==1")["phi"], density = True, alpha = 0.5, label = "Signal",bins=200,range=[-3,3])
ax01.hist(df.query("Signal==0")["phi"], density = True, alpha = 0.5, label = "Background",bins=200,range=[-3,3])
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


 
