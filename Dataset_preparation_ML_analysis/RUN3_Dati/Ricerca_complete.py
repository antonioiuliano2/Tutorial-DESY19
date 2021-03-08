from __future__ import division 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, scatter, draw, figure, show
from scipy.optimize import curve_fit
from matplotlib import colors
#import ROOT as R
import numpy as np
#import root_numpy as rp

#MCEvent = [n for n in range(360, 720)]

MCEvent = [n for n in range(0,173)]

#dfinizio = pd.read_csv('/home/user/Desktop/RUN3_2/Inizio_sciamenuovo.csv')
#dfinizio = pd.read_csv('/home/mdeluca/dataset/RUN3/RUN3_3/Inizio_sciame_RUN3_3.csv')

dfinizio = pd.read_csv('/home/mdeluca/dataset/RUN3/RUN3_data/Inizio_candidati_sciami.csv')
#df = pd.read_csv('/home/user/Desktop/RUN3_2/Taglio_par.csv')
#df = pd.read_csv('/home/mdeluca/dataset/RUN3/RUN3_3/Theta/Final_dataset_RUN3_3_tagliopar.csv')
df = pd.read_csv('/home/mdeluca/dataset/RUN3/RUN3_data/Theta/Final_data_tagliopar.csv')
#df = pd.read_csv('Theta_btdata0.csv')
#del dfinizio['Unnamed: 0']
del df['Unnamed: 0']

h = 0

dfg = pd.DataFrame()
dfp = pd.DataFrame()
dfg = pd.concat([dfinizio, df], sort=False)
dfh = dfg.fillna(0)
dfv = pd.DataFrame()
dfs = pd.DataFrame()

dftheta1 = pd.DataFrame()
dftheta2 = pd.DataFrame()

do = pd.DataFrame()
du = pd.DataFrame()
dh = pd.DataFrame()
da = pd.DataFrame()
dfu = pd.DataFrame()
dfl = pd.DataFrame()

for shower in MCEvent:
    dh = dh[0:0]
    du = du[0:0]
    do = du[0:0]
    dfu = dfu[0:0]
    dfs = dfs[0:0]
    dfv = dfv[0:0]
    dftheta1 = dftheta1[0:0]
    dftheta2 = dftheta2[0:0]
    print(shower)
    dfshower = dfg.query('Ishower=={}'.format(shower))
    print(len(dfshower))
    PID_max = np.max(dfshower['PID'])
    PID_min = np.min(dfshower['PID'])

    for m in range(PID_min, PID_max+1):
      dft = dfshower.query('PID=={}'.format(m))
      dfc = dft.copy()
      dfc['PID_ric'] = PID_max-m
      dfv = pd.concat([dfv, dfc], sort=False)

    for pid in range(PID_min , 1):  
      #if pid==PID_min:
        #for pid in range(PID_min, 1):
         print(pid)
         dftheta1 = dfv.query('PID_ric=={}'.format(PID_min))
         dftheta2 = dfv.query('PID_ric=={}'.format(PID_min+1))
        
         if dftheta2.empty:
           dftheta2 = dftheta1
           do = dftheta2
        
         else:
           print('non vuoto')
           
         xevent = (dftheta2['x'].values)
         
         zevent = (dftheta2['z'].values)
         yevent = (dftheta2['y'].values)

         TXevent = (dftheta2['TX'].values)
         TYevent = (dftheta2['TY'].values)
         xnext = (dftheta1['X_Next'].values)
         znext = (dftheta1['Z_Next'].values)
         ynext = (dftheta1['Y_Next'].values)
         TXnext = (dftheta1['TX'].values)
         TYnext = (dftheta1['TY'].values)  
           
         for n in range(0, len(xnext)):
            # print(n)
            DiffX = xnext[n] - xevent
            DiffY = ynext[n] - yevent
            DiffTX = TXnext[n] - TXevent
            DiffTY = TYnext[n] - TYevent
            dR = np.sqrt((DiffX)**2 + (DiffY)**2)
            dTh = np.sqrt((DiffTX)**2 + (DiffTY)**2)
            dT =np.arctan(dTh)
            dfs = dfs[0:0]
            
            for i in range(0, len(dT)):
              
              if dT[i]<=0.4:
                 xevent1 = np.round(xevent,3)
                 #print(dT[i])
                 #print(i,xevent1[i])
                 ID2 = dftheta2['ID'].values
                 #print(ID2[i])
                 dft = dftheta2.query('ID=={}'.format(ID2[i]))
                 #dft = dftheta2.query('x=={}'.format(xevent[i]))
                 #print(dft)
                 dfc = dft.copy()
                 dfc['dx']=DiffX[i]
                 dfc['dy']=DiffY[i]
                 dfc['dTX']=DiffTX[i]
                 dfc['dTY']=DiffTY[i]
                 dfc['dT']=dT[i]
                 dfc['dR']=dR[i]
                 dfs = pd.concat([dfc, dfs])
         dfu = pd.concat([dfs,dfu])

         dx = pd.DataFrame()
         ID2 = np.unique(dfu['ID'].values)
         #ID2 = [n for n in range(417368, 417369)]

         for t in ID2:
            dfj = dfu.query('ID=={}'.format(t))
            dfp = dfj.copy()
         
            dfh = dfp[dfp.dT==dfp.dT.min()]
            do = pd.concat([do, dfh]) 
         dfz = do

 

    for pid in range(1, PID_max+1):
        #dh = dh[0:0]
        du = du[0:0]
        print(pid)
        dfl = dfl[0:0]
        da = da[0:0]

        dftheta1 = do
        dftheta2 = dfv.query('PID_ric=={}'.format(pid+1))

        if dftheta2.empty:
             dftheta2=dftheta1
             print('Vuoto')
        else: 
             print('Non vuoto')

        dZ = np.unique(dftheta2['z'].values)- dftheta1['z'].values
        xevent = (dftheta2['x'].values)
        zevent = (dftheta2['z'].values)
        yevent = (dftheta2['y'].values)

        TXevent = (dftheta2['TX'].values)
        TYevent = (dftheta2['TY'].values)
        
        xnext = (dftheta1['x'].values+dftheta1['TX'].values*dZ/2)
        znext = (dftheta1['z'].values+dZ/2)
        ynext = (dftheta1['y'].values+dftheta1['TY'].values*dZ/2)
        TXnext = (dftheta1['TX'].values)
        TYnext = (dftheta1['TY'].values)


        for n in range(0, len(xnext)):
            # print(n)
            DiffX = xnext[n] - xevent
            DiffY = ynext[n] - yevent
            DiffTX = TXnext[n] - TXevent
            DiffTY = TYnext[n] - TYevent
            dR = np.sqrt((DiffX)**2 + (DiffY)**2)
            dTh = np.sqrt((DiffTX)**2 + (DiffTY)**2)
            dT =np.arctan(dTh)
            #dfs = dfs[0:0]
            #da = da[0:0]
            #dx = dx[0:0]
            ID2 = dftheta2['ID'].values
            #print(ID2[i])
            '''
            for u in ID2:
             dft = dftheta2.query('ID=={}'.format(u))
             #dft = dftheta2.query('x=={}'.format(xevent[i]))
             #print(dft)
             dfc = dft.copy()
             dfc['dx']=DiffX[i]
             dfc['dy']=DiffY[i]
             dfc['dTX']=DiffTX[i]
             dfc['dTY']=DiffTY[i]
             dfc['dT']=dT[i]
             dfc['dR']=dR[i]
             da = pd.concat([dfc, da])
             dfb = da[da.dT==da.dT.min()]
        dfx = pd.concat([dfx, dfb])
        dfl = pd.concat([da,dfl])
            '''
            for i in range(0, len(dT)):
              
              if dT[i]<=0.4:
                 xevent1 = np.round(xevent,3)
                 #print(dT[i])
                 #print(i,xevent1[i])
                 ID2 = dftheta2['ID'].values
                 #print(ID2[i])
                 dft = dftheta2.query('ID=={}'.format(ID2[i]))
                 #dft = dftheta2.query('x=={}'.format(xevent[i]))
                 #print(dft)
                 dfc = dft.copy()
                 dfc['dx']=DiffX[i]
                 dfc['dy']=DiffY[i]
                 dfc['dTX']=DiffTX[i]
                 dfc['dTY']=DiffTY[i]
                 dfc['dT']=dT[i]
                 dfc['dR']=dR[i]
                 da = pd.concat([dfc, da])
        dfl = pd.concat([da,dfl])

        if dfl.empty:
           print('dfl vuoto')
           do = dftheta1
           du = do
           dh = pd.concat([dh, du])
           #do = do[0:0] 
        
        elif not dfl.empty:
   
          ID2 = np.unique(dfl['ID'].values)
          #ID2 = [n for n in range(417368, 417369)]
          du = do
          dh = pd.concat([dh, du])
          do = do[0:0]
          for t in ID2:
            dfj = dfl.query('ID=={}'.format(t))
            dfi = dfj.copy()
         
            dfb = dfi[dfi.dT==dfi.dT.min()]
         
         
            do = pd.concat([do, dfb], sort=False)
    dv = dh.drop_duplicates()
    print(dv)
    dv.to_csv('/home/mdeluca/dataset/RUN3/RUN3_data/Event/Event{}.csv'.format(shower))
    
    #print(dh)



