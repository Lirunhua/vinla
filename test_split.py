#coding=utf-8
import numpy as np
from mdlp.discretization import MDLP
from sklearn.datasets import load_iris
column = np.array([1,2])
transformer = MDLP(column)
iris = load_iris()
X, y = iris.data, iris.target
print y
print type(X), type(y)
X_disc = transformer.fit_transform(X,y)

conv_X = transformer.fit_transform(X, y)
print conv_X
di = transformer.cut_points_




print  transformer.cut_points_

for each in di:
    print len(di[each])