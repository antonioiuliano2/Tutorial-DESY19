#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 10:41:21 2020

@author: maria
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, scatter, draw, figure, show

dfshower = pd.read_csv("DataFrame01.csv")

dfshower = dfshower[['x','y','z','TX','TY','MCEvent']]
print(dfshower)

y = dfshower.iloc[:,-1].values
X = dfshower.iloc[:, [2,1]].values
print(X)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
sc.fit(X_train)
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)


'''Percettrone'''
from sklearn.linear_model import Perceptron
ppn = Perceptron(max_iter=1000, eta0=0.1, random_state=0)
ppn.fit(X_train_std, y_train)
y_pred = ppn.predict(X_test_std)
X_combined_std = np.vstack((X_train_std, X_test_std))
y_combined = np.hstack((y_train, y_test))

from mlxtend.plotting import plot_decision_regions
plot_decision_regions(X_combined_std, y_combined, clf=ppn, legend=2, X_highlight=X_test_std)
plt.xlabel('z[standardized]')
plt.ylabel('y[standardized]')
plt.title('Perceptron classifier')
plt.show()
print('PERCEPTRON:   Misclassified samples: %d' % (y_test != y_pred).sum())
from sklearn.metrics import accuracy_score
print('PERCEPTRON:  Accuracy: %.2f' % accuracy_score(y_test, y_pred))



'''SVM'''
from sklearn.svm import SVC
svm = SVC(kernel='linear', C=0.1, random_state=0)
svm.fit(X_train_std, y_train)
y_pred_svm = svm.predict(X_test_std)
plot_decision_regions(X_combined_std,
			y_combined, clf=svm, X_highlight=X_test_std)
plt.xlabel('z[standardized]')
plt.ylabel('y[standardized]')
plt.title('SVM Linear')
plt.show()
print('SVM_Linear:  Misclassified samples: %d' % (y_test != y_pred_svm).sum())
from sklearn.metrics import accuracy_score
print('SVM_Linear:  Accuracy: %.2f' % accuracy_score(y_test, y_pred_svm))

from sklearn.svm import SVC
#Training
svm_gaus = SVC(kernel='rbf', C=10.0, random_state=1,gamma=10.)
svm_gaus.fit(X_train_std, y_train)
#Predizione
y_pred_svm_gaus= svm_gaus.predict(X_test_std)
plot_decision_regions(X_combined_std,
			y_combined, clf=svm_gaus, legend=2, X_highlight=X_test_std)
plt.xlabel('z[standardized]')
plt.ylabel('y[standardized]')
plt.title('SVM Gaussian')
plt.show()
print('SVM_Gaussian:   Misclassified samples: %d' % (y_test != y_pred_svm_gaus).sum())
from sklearn.metrics import accuracy_score
print('SVM_Gaussian:   Accuracy: %.2f' % accuracy_score(y_test, y_pred_svm_gaus))


'''Decision tree'''
from sklearn.tree import DecisionTreeClassifier
tree = DecisionTreeClassifier(criterion='entropy',
                            max_depth=5, random_state=1)
tree.fit(X_train_std, y_train)
y_pred_tree = tree.predict(X_test_std)
plot_decision_regions(X_combined_std, y_combined,
                      clf=tree, X_highlight=X_test_std)
plt.xlabel('z[standardized]')
plt.ylabel('y[standardized]')
plt.title('Decision_tree classifier')
plt.show()
print('DECISION TREE:  Misclassified samples: %d' % (y_test != y_pred_tree).sum())
from sklearn.metrics import accuracy_score
print('DECISION TREE: Accuracy: %.2f' % accuracy_score(y_test, y_pred_tree))



from sklearn.ensemble import RandomForestClassifier
forest = RandomForestClassifier(criterion='entropy', n_estimators=10, random_state=1, n_jobs=2)
forest.fit(X_train_std, y_train)
y_pred_forest = forest.predict(X_test_std)
plot_decision_regions(X_combined_std, y_combined,
clf=forest, X_highlight=X_test_std)
plt.xlabel('z[standardized]')
plt.ylabel('y[standardized]')
plt.title('Random_Forest classifier')
plt.show()
print('RANDOM FOREST: Misclassified samples: %d' % (y_test != y_pred_forest).sum())
from sklearn.metrics import accuracy_score
print('RANDOM FOREST:  Accuracy: %.2f' % accuracy_score(y_test, y_pred_forest))


from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
BDT= AdaBoostClassifier(base_estimator=DecisionTreeClassifier(max_depth=1),n_estimators=500, algorithm='SAMME',learning_rate=1,random_state=0)
BDT.fit(X_train_std, y_train)
#Predizione
y_pred_bdt= BDT.predict(X_test_std)
plot_decision_regions(X_combined_std, y_combined,
clf=BDT, X_highlight=X_test_std)
plt.xlabel('z[standardized]')
plt.ylabel('y[standardized]')
plt.title('BDT_classifier')
plt.show()
print('BDT: Misclassified samples: %d' % (y_test != y_pred_bdt).sum())
from sklearn.metrics import accuracy_score
print('BDT:  Accuracy: %.2f' % accuracy_score(y_test, y_pred_bdt))




from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=5, p=2,
                           metric='minkowski')
knn.fit(X_train_std, y_train)
y_pred_knn = knn.predict(X_test_std)

from sklearn.metrics import confusion_matrix
plot_decision_regions(X_combined_std, y_combined,
                      clf=knn, X_highlight=X_test_std)
plt.xlabel('z[standardized]')
plt.ylabel('y[standardized]')
plt.show()
print(confusion_matrix (y_test, y_pred_knn))
print('KNN:  Misclassified samples: %d' % (y_test != y_pred_knn).sum())
from sklearn.metrics import accuracy_score
print('KNN:  Accuracy: %.2f' % accuracy_score(y_test, y_pred_knn))

