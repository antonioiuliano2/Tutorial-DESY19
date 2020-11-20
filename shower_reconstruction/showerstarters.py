'''selection of first segments from volume tracks in the first three plates, with angles less than 0.05 rad'''
import numpy as np
import pandas as pd

def addshowerindex( df, selection = "sqrt(TX*TX+TY*TY) < 0.05 and PID > 25"):
 '''selecting shower candidates to dataset df with selection'''
 #checking which segments have been assigned to volume tracks
 dftracked = df.query("TrackID>=0")
 
 #sorting according to track index and plate, keeping only first segment

 dftracked_firstsegment = dftracked.sort_values(["TrackID","PID"],ascending = [True, False]).groupby("TrackID").first()

 #selection for starters
 dfstarters = dftracked_firstsegment.query(selection)

 #adding a new column, starterindex

 ishower = np.linspace(0,len(dfstarters)-1, len(dfstarters),dtype = int)

 dfstarters["ishower"] = ishower

 #keeping only the columns needed for merge and new one

 dfstarters_reduced = dfstarters[["ID","PID","ishower"]]

 #merging with original dataframe

 df_withstarters = df.merge(dfstarters_reduced,how = 'left', on=["PID","ID"])

 return df_withstarters
