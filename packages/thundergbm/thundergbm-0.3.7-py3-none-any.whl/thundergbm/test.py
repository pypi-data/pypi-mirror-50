from thundergbm import *
from sklearn.datasets import *
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from math import sqrt
#x,y = load_svmlight_file("../dataset/test_dataset.txt")
x,y = load_svmlight_file("../../dataset/a9a")
#clf = TGBMRegressor(n_gpus=1)
clf = TGBMClassifier(objective='binary:logistic')
#clf = TGBMClassifier(objective='multi:softmax')
clf.fit(x,y)
#, objective='binary:logistic'
x2,y2=load_svmlight_file("../../dataset/a9a")
#x2,y2=load_svmlight_file("../dataset/test_dataset.txt")
y_predict=clf.predict(x2)
#print(y_predict)
acc = accuracy_score(y2, y_predict)
print(acc)
#rms = sqrt(mean_squared_error(y2, y_predict))
#print(rms)
