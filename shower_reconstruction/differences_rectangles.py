import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist

dforig = pd.read_csv("data_noise_firsttenplates_DESY19.csv")
print("Built dataset from file")


dforig["xafter"] = 1315 * dforig["TX"] + dforig["x"]
dforig["yafter"] = 1315 * dforig["TY"] + dforig["y"]

dforig["xbefore"] = -1315 * dforig["TX"] + dforig["x"]
dforig["ybefore"] = -1315 * dforig["TY"] + dforig["y"]

selection = "abs(x - 50000)<5000 and abs(y - 50000)<5000"
df = dforig.query(selection)
print("Applied selection ", selection)

#find projections in plate before and after

#extracting component between plates with PID 5 and 6
df5 = df.query("PID==5")
df6 = df.query("PID==6")


print("Start computing matrix")
def compute2Ddistancematrix(df, dfnext):
    '''return distance matrix from columns
       df: dataframe containing segments from a plate
       dfnext: dataframe containing segments from a plate downstream
    '''
    #extracting x and y variables into 2d arrays
    xafter = df["xafter"].to_numpy()
    yafter = df["yafter"].to_numpy()
    xyafter = np.vstack((xafter,yafter)).T

    x = dfnext["x"].to_numpy() 
    y = dfnext["y"].to_numpy()
    xy = np.vstack((x,y)).T

    distancematrix = cdist(xy,xyafter,metric = "euclidean")

    return distancematrix

distancematrix = compute2Ddistancematrix(df6,df5)
print("computed distance matrix between PID 5 and 6")