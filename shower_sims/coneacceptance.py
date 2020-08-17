from __future__ import division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

simdf = pd.read_csv("RUN3.csv")

def doevent(mcevent,df, alphamax, Rmax):
    '''acceptance and purity for event mcevent in dataframe df'''
    firstsegment = df.query("PID==28 and  MCTrack==0 and MCEvent=={}".format(mcevent))

    if len(firstsegment) != 1:
        print(len(firstsegment))
        return (0,0)

    xfirst = firstsegment["x"].to_numpy()
    yfirst = firstsegment["y"].to_numpy()
    zfirst = firstsegment["z"].to_numpy()
    TXfirst = firstsegment["TX"].to_numpy()
    TYfirst = firstsegment["TY"].to_numpy()
    #computing dR
    df["dx"] = df["x"] - xfirst[0]
    df["dy"] = df["y"] - yfirst[0]
    df["dz"] = df["z"] - zfirst[0]
    #transverse radial difference
    df["dR"] = np.sqrt(np.power(df["dx"],2) + np.power(df["dy"],2))
    #cone angle
    df["alpha"] = np.arctan(np.sqrt(np.power(df["dx"]/df["dz"],2)+np.power(df["dy"]/df["dz"],2)))

    #how many within conditions?
    recodf = df.query("dR < {} and alpha < {}".format(Rmax,alphamax))

    Ntruesim = len(simdf.query("MCEvent=={}".format(mcevent)))
    Ntruereco = len(recodf.query("MCEvent=={}".format(mcevent)))
    Nallreco = len(recodf)

    efficiency = Ntruereco / Ntruesim
    purity = Ntruereco / Nallreco

    return (efficiency, purity)

nevents = 360

alphamax = 0.04
rmax = 800 #microns

allefficiencies = []
allpurities = []
for ievent in range(nevents):
 (efficiency, purity) = doevent(ievent,simdf,alphamax, rmax)
 allefficiencies.append(efficiency)
 allpurities.append(purity)

#plotting result histograms
fig1 = plt.figure()
plt.hist(allefficiencies, range = [0,1], bins = 10)
plt.xlabel("efficiency")

fig2 = plt.figure()
plt.hist(allpurities, range = [0,1], bins = 10)
plt.xlabel("purity")

plt.show()
