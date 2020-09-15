import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
#input parameters
myevent = 4
coneangle = 0.04

#drawing segments from a shower in 3d
df = pd.read_csv("RUN3.csv_firsttenplates.csv")

df4 = df.query("MCEvent == {}".format(myevent))
#getting first segment
firstseg = df4.query("PID==9 and MCTrack==0")
firstsegT = np.sqrt(np.power(firstseg["TX"].iloc[0],2)+np.power(firstseg["TY"].iloc[0],2)+np.power(1,2))
#vettore spostamento
df4["dx"] = df4["x"] - firstseg["x"].iloc[0]
df4["dy"] = df4["y"] - firstseg["y"].iloc[0]
df4["dz"] = df4["z"] - firstseg["z"].iloc[0]
df4["dr"] = np.sqrt(np.power(df4["dx"],2)+np.power(df4["dy"],2)+np.power(df4["dz"],2))

scalardot = firstseg["TX"].iloc[0] * df4["dx"] + firstseg["TY"].iloc[0] * df4["dy"] + df4["dz"]

df4["theta"] = np.arccos(scalardot/(firstsegT * df4["dr"]))
df4 = df4.fillna(0) #theta is not defined for first segment of the shower

df4ok = df4.query("theta <= {}".format(coneangle))
df4notok = df4.query("theta > {}".format(coneangle))

fig3d = plt.figure()
#first, I simply draw the shower
ax3d = fig3d.add_subplot(111, projection='3d')

ax3d.scatter(df4notok['z'], df4notok['x'],df4notok['y'],c="r")
ax3d.scatter(df4ok['z'], df4ok['x'],df4ok['y'],c="g")
#cone draw, I need a meshgrid
# Set up the grid in polar
theta = np.linspace(0,2*np.pi,90)
z = np.linspace(firstseg["z"].iloc[0],0,50)
T, Z = np.meshgrid(theta, z)

# Then calculate X, Y, and Z
R = (Z - firstseg["z"].iloc[0]) * np.tan(coneangle)
X = R * np.cos(T) + firstseg["x"].iloc[0]
Y = R * np.sin(T) + firstseg["y"].iloc[0]
#Z = R - 1
ax3d.plot_wireframe(Z, X, Y,color = "c")

ax3d.set_title("Shower from event {}".format(myevent))
ax3d.set_xlabel("Z[$\mu$m]")
ax3d.set_ylabel("Y[$\mu$m]")
ax3d.set_zlabel("X[$\mu$m]")
plt.show()