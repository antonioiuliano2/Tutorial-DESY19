import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xgboost
import collections
from collections import OrderedDict
import seaborn as sns

'''
   Random forest training and test components.
   It will not save algorithm (Pickle lines to be added)

   Before launching it, please make a empty directory Random_Forest
   it will fill this folder with a file for each shower
'''

data1 = pd.read_csv('/home/mdeluca/dataset/RUN3/RUN3_2/Event/Final_dataset_RUN3_2.csv')  # RUN3_2 --> 2 dataset del RUN3
data2 = pd.read_csv('/home/mdeluca/dataset/RUN3/RUN3_3/Event/Final_dataset_RUN3_3.csv')  # RUN3_3 --> 3 dataset del RUN3

del data1['Unnamed: 0']
del data2['Unnamed: 0']

y = data1.loc[:, 'Signal']
X = data1.loc[:,['x','y','z','TX','TY','PID','X_Next','Y_Next','dx','P','Flag','MCTrack','dy','dTX','dTY','dR','dT','DeltaT','Par_impact_nor','Angolo_cono','MCEvent','Ishower']]

X1 = data2.loc[:,['x','y','z','TX','TY','PID','X_Next','Y_Next','dx','P','Flag','MCTrack','dy','dTX','dTY','dR','dT','DeltaT','Par_impact_nor','Angolo_cono', 'MCEvent','Ishower']]
y1 = data2.loc[:,'Signal']

#from sklearn.model_selection import train_test_split
#X_trainMC, X_testMC, y_train, y_testMC = train_test_split(X,y, test_size=0.3, random_state=0, stratify=y)

#X_tot = X_testMC.append(X1)

#X_test = X_tot.loc[:,['x','y','z','TX','TY','X_Next','Y_Next','dx','dy','dTX','dTY']]
#y_test = y_testMC.append(y1)
#X_train = X_trainMC.loc[:,['x','y','z','TX','TY','X_Next','Y_Next','dx','dy','dTX','dTY']]

X_train = X.loc[:,['dx','dy','dTX','dTY','DeltaT', 'Par_impact_nor','Angolo_cono']]
y_train = y

X_test = X1.loc[:,['dx','dy','dTX','dTY', 'DeltaT', 'Par_impact_nor','Angolo_cono']]
y_test = y1


from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
sc.fit(X_train)
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)

print('---------------------------------------------')
print('dataset_training', len(X_train))
print('dataset_test',len(X_test))
print('---------------------------------------------')
print('Inizio Random Forest')

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score

#forest = xgboost.XGBClassifier(n_estimators = 60, random_state=1, n_jobs=-1)
forest = RandomForestClassifier(criterion='entropy', n_estimators=500, max_depth=200, class_weight ='balanced_subsample' , random_state=1, n_jobs=-1)
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
dforest.to_csv('/home/mdeluca/dataset/RUN3/RUN3_3/Random_Forest/Confusion_matrix1.csv')
ff = open('/home/mdeluca/dataset/RUN3/RUN3_3/Random_Forest/Report_Forest1.txt', 'w')
ff.write('Title\n\nClassification Report\n\n{}'.format(crf))
ff.close()
dfnew = pd.DataFrame(classification_report(y_test, y_pred_forest, output_dict=True)).transpose()

print('-----------------------------------------------')
print('Classification Report')
print(dfnew)
dfnew.to_csv('/home/mdeluca/dataset/RUN3/RUN3_3/Random_Forest/Classification_Report1.csv', index=True)


labels = ['Y_test','Y_pred_forest']
dfforest = pd.DataFrame({'Y_test':y_test, 'Y_pred_forest':y_pred_forest}, columns = labels)

dfresult = pd.DataFrame(X1.join(dfforest))
print(dfresult)
dfresult.to_csv('/home/mdeluca/dataset/RUN3/RUN3_3/Random_Forest/Prediction.csv')



from sklearn.metrics import roc_curve, auc
from sklearn import metrics
from sklearn.metrics import roc_auc_score

#forest.fit(X_train_std, y_train)
#forest_auc = roc_auc_score(y_test, y_pred_forest_proba)
#y_pred_proba = forest.predict_proba(X_test_std)

#print('RANDOM FOREST: AUC_SCORE:%.3f' % forest_auc)


'''
estimator = forest.estimators_[5]

from sklearn.tree import export_graphviz
# Export as dot file
export_graphviz(estimator, out_file='/home/mdeluca/dataset/RUN3/RUN3_3/Event/tree.dot', 
                rounded = True, proportion = False, 
                precision = 2, filled = True)

# Convert to png using system command (requires Graphviz)
from subprocess import call
call(['dot', '-Tpng', 'tree.dot', '-o', 'tree.png', '-Gdpi=600'])
'''
'''
# Display in jupyter notebook
from IPython.display import Image
Image(filename = 'tree.png')
'''
