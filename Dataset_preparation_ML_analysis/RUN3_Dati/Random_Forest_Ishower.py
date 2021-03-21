import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import collections
from collections import OrderedDict
from argparse import ArgumentParser
import pickle

'''
   Random forest application
   It will not save algorithm (Pickle lines to be added)

   Before launching it, please make a empty directory Random_Forest
   it will fill this folder with a file for each shower
   python Random_Forest_Ishower.py -id Final_dataset_training.csv -id2 Final_dataset_test.csv -id3 Final_dataset_application.csv -of Random_Forest
'''

parser = ArgumentParser()
parser.add_argument("-id","--inputdataset",dest="inputcsvdatasettraining",help="input dataset for training",required=True)
parser.add_argument("-id2","--inputdatasettest",dest="inputcsvdatasettest",help="input dataset for test",required=True)
parser.add_argument("-id3","--inputdatasetapplication",dest="inputcsvdatasetapplication",help="input dataset for application over real data",required=True)
parser.add_argument("-of","--outputfolder",dest="outputfolder",help="folder to store output datasets",required=True)
options = parser.parse_args()

#data1 = pd.read_csv('/home/mdeluca/dataset/RUN3/RUN3_1/Dataset_Parametro_Impatto/Final_dataset1.csv')
#data2 = pd.read_csv('/home/mdeluca/dataset/RUN3/RUN3_3/SN_Knear/Final_dataset_RUN3_3.csv') #Final_dataset_RUN3_3_new.csv
#data3 = pd.read_csv('/home/mdeluca/dataset/RUN3/RUN3_data/SN_Knear/Final_dataset_data.csv')
#data3 = pd.read_csv('SN_Knear19_new.csv')
#data3 = pd.read_csv('/home/mdeluca/dataset/RUN3/RUN3_data/New/Theta_btdata19.csv')
#data3 =pd.read_csv('SN_Knear19_new.csv')
#data3 = pd.read_csv('/home/mdeluca/dataset/RUN3/RUN3_data/New/Theta_btdata19.csv')

#data1 = pd.read_csv('/home/mdeluca/dataset/RUN3/RUN3_2/Theta/Theta_RUN3_2.csv')
#data2 = pd.read_csv('/home/mdeluca/dataset/RUN3/RUN3_3/Theta/Theta_RUN3_3.csv')
#data3 = pd.read_csv('/home/mdeluca/dataset/RUN3/RUN3_data/Theta/Theta_data_RUN3.csv')

data11 = pd.read_csv(options.inputcsvdatasettraining)
data21 = pd.read_csv(options.inputcsvdatasettest)

#data3 = pd.DataFrame()

data1 = pd.DataFrame()
data1 = data11.dropna()

data2 = pd.DataFrame()
data2 = data21.dropna()

#data3 = pd.read_csv('/home/mdeluca/dataset/RUN3/RUN3_data/SN_PID/Finale_prova19.csv')
#data31 = pd.read_csv('/home/mdeluca/dataset/RUN3/RUN3_data/Test1/Event_tot.csv')
#del data31['Unnamed: 0']
#data32 = pd.read_csv('/home/mdeluca/dataset/RUN3/RUN3_data/Test/Event_123_19.csv')
#del data32['Unnamed: 0']

#data3 = pd.concat([data31, data32])
data3 = pd.read_csv(options.inputcsvdatasetapplication)
#data3 = pd.DataFrame()

#data3 = data33.dropna()

del data1['Unnamed: 0']
del data2['Unnamed: 0']
del data3['Unnamed: 0']


y = data1.loc[:, 'Signal']
X = data1.loc[:,['ID','x','y','z','TX','TY','PID','X_Next','Y_Next','P','Flag','MCTrack','dx','dy','dTX','dTY','dR','dT','DeltaT','Par_impact_nor','Angolo_cono','MCEvent','Ishower']]

X1 = data2.loc[:,['ID','x','y','z','TX','TY','PID','X_Next','Y_Next','P','Flag','MCTrack','dx','dy','dTX','dTY','dR','dT','DeltaT','Par_impact_nor','Angolo_cono', 'MCEvent','Ishower']]
y1 = data2.loc[:,'Signal']

#X2 = data3.loc[:, ['ID','x','y','z','TX','TY','PID','X_Next','Y_Next','dx','dy','dTX','dTY','dR','dT','DeltaT','Par_impact_nor','Angolo_cono','TrackID', 'MCevent','Ishower']]

X_train = X.loc[:,['dx','dy','dTX','dTY','DeltaT', 'Par_impact_nor','Angolo_cono']]
y_train = y

X_test = X1.loc[:,['dx','dy','dTX','dTY','DeltaT', 'Par_impact_nor','Angolo_cono']] #dx,dy,dTX,dTY
y_test = y1

X_pred1 = data3.loc[:,['dx','dy','dTX','dTY','DeltaT','Par_impact_nor','Angolo_cono']]
X_pred = X_pred1.fillna(0)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
sc.fit(X_train)
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)
X_pred_std = sc.transform(X_pred)

print('---------------------------------------------')
print('dataset_training', len(X_train))
print('dataset_test',len(X_test))
print('dataset dati',len(X_pred))
print('---------------------------------------------')
print('Inizio Random Forest')

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score


#filename = '/home/mdeluca/dataset/RUN3/RUN3_2/Random_Forest/Finalized_model_RF.sav'

#forest = pickle.load(open(filename, 'rb'))
#result = loaded_model.score(X_test, Y_test)
#print(result)


#forest = xgboost.XGBClassifier(n_estimators = 60, random_state=1, n_jobs=-1)
forest = RandomForestClassifier(criterion='entropy', n_estimators=500, max_depth=200, class_weight = {0:1, 1:100}, random_state=1, n_jobs=-1)
forest.fit(X_train_std, y_train)
y_pred_forest = forest.predict(X_test_std)
y_pred_forest_proba = forest.predict_proba(X_test_std)
print('RANDOM FOREST: Misclassified samples: %d' % (y_test != y_pred_forest).sum())
print('RANDOM FOREST:  Accuracy: %.3f' % accuracy_score(y_test, y_pred_forest))
print('RANDOM FOREST: Precision micro:%.3f' % precision_score(y_test, y_pred_forest, average='micro'))
print('RANDOM FOREST: F-SCORE:%.3f' % f1_score(y_test, y_pred_forest, average='micro'))
print('----------------------------------------------')
print('Confusion Matrix')
crf = classification_report(y_test, y_pred_forest)
cmf = confusion_matrix(y_test, y_pred_forest)
dforest = pd.DataFrame(cmf)
print(dforest)
dforest.to_csv(options.outputfolder+'/Confusion_matrix1.csv')
ff = open(options.outputfolder+'/Report_Forest1.txt', 'w')
ff.write('Title\n\nClassification Report\n\n{}'.format(crf))
ff.close()
dfnew = pd.DataFrame(classification_report(y_test, y_pred_forest, output_dict=True)).transpose()

print('-----------------------------------------------')
print('Classification Report')
print(dfnew)
dfnew.to_csv(options.outputfolder+'/Classification_Report1.csv', index=True)
#dfnew.to_csv('/home/mdeluca/dataset/RUN3/RUN3_data/Random_Forest/Classification_Report_testRUN3_2.csv',index=True)

labels = ['Y_test','Y_pred_forest']
dfforest = pd.DataFrame({'Y_test':y_test, 'Y_pred_forest':y_pred_forest}, columns = labels)

dfresult = pd.DataFrame(X1.join(dfforest))


y_pred_data = forest.predict(X_pred_std)
dfpred = pd.DataFrame({'Y_pred_forest_data':y_pred_data})
dfresult_data = pd.DataFrame(data3.join(dfpred))

dfresult.to_csv(options.outputfolder+'/Prediction.csv')

#dfresult.to_csv('/home/mdeluca/dataset/RUN3/RUN3_data/Random_Forest/Resut_testRUN3_2.csv')
#print('Inizio pickle')
#filename = '/home/mdeluca/dataset/RUN3/RUN3_2/Random_Forest/Finalized_model_RF_10mila.sav'
#pickle.dump(forest, open(filename, 'wb'))

#print('Fine pickle')

from sklearn.metrics import roc_curve, auc
from sklearn import metrics
from sklearn.metrics import roc_auc_score
dfresult_data.to_csv(options.outputfolder+'/Result_data.csv')


#forest.fit(X_train_std, y_train)
#forest_auc = roc_auc_score(y_test, y_pred_forest_proba)
#y_pred_proba = forest.predict_proba(X_test_std)

#print('RANDOM FOREST: AUC_SCORE:%.3f' % forest_auc)


print(dfresult_data)

