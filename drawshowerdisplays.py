import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv(sys.argv[1])
nshowers = 360
#drawing xy distribution of beam
dfbeam = df.query("PID==28 and MCTrack==0")
print (len(dfbeam))


fig1, ax1 = plt.subplots()
ax1.plot(dfbeam["x"],dfbeam["y"],"r*")
ax1.set_title("Beam XY distribution of all surface")
ax1.set_xlabel("x[$\mu m$]")
ax1.set_ylabel("y[$\mu m$]")

#drawing xy distribution of all showers
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()
fig4, ax4 = plt.subplots()

for ishower in range(nshowers):
 dfshower = df.query("MCEvent == {}".format(ishower))
 #random color

 r = np.random.random()
 b = np.random.random()
 g = np.random.random()
 color = (r, g, b)

 ax2.plot(dfshower["x"],dfshower["y"],"*",c=color)
 ax2.set_title("XY distribution of all surface")
 ax2.set_xlabel("x[$\mu m$]")
 ax2.set_ylabel("y[$\mu m$]")
 
 ax3.plot(dfshower["z"],dfshower["y"],"*",c=color)
 ax3.set_title("ZY distribution of all surface")
 ax3.set_xlabel("z[$\mu m$]")
 ax3.set_ylabel("y[$\mu m$]")

 df1mm =dfshower.query("abs(y-50000)<500")

 ax4.plot(df1mm["z"],df1mm["y"],"*",c=color)
 ax4.set_title("zoomed ZY distribution of all surface")
 ax4.set_xlabel("z[$\mu m$]")
 ax4.set_ylabel("y[$\mu m$]")

plt.figure()
plt.hist(29-df["PID"],29,[1,30])
plt.show()