from sklearn import svm, metrics
import pandas as pd
import math

def changeValue(lst):
    return [ math.ceil(float(v) / 255) for v in lst]
'''
# 붓꽃 데이터 분류기(머신러닝)
- 개요 : 150개 붓꽃 정보(꽆받침 길이, 꽃받침 폭, 꽃잎 길이, 꽃잎 폭)\
- 종류 : 3개 (Iris-setosa / Iris-vesicolor / Iris-virginica)
- CSV파일 구하장 : iris.csv
'''
## 훈련데이터, 테스트데이터 준비
csv = pd.read_csv("C:/mnist/train_10K.csv")
# csv = csv.sample(frac=1).reset_index(drop=True)
train_data = csv.iloc[:, 1:].values # 이렇게 해야 값이 들어오나(value 안붙이면 return이 DF)
train_data = list(map(changeValue, train_data)) # 값이 0~1 범위를 0~255로 : map객체를 list화 시키기
train_label = csv.iloc[:,0].values

# csv = pd.read_csv("C:/mnist/t10k_05K.csv")
# # csv = csv.sample(frac=1).reset_index(drop=True)
# test_data = csv.iloc[:, 1:].values
# test_data = list(map(changeValue, test_data)) # 값이 0~1 범위를 0~255로 : map객체를 list화 시키기
# test_label = csv.iloc[:,0].values

# 1. Classifier 생성(선택) --> 머신러닝 알고리즘 선택
clf = svm.SVC(gamma='auto')
# clf = svm.NuSVC(gamma='auto')

# 2. 데이터로 학습시키기
# clf.fit( [훈련데이터], [정답])
# XOR 문제를 fit 해보기
clf.fit(train_data,train_label)

# 학습된 모델 저장하기
# 파일 그자체 저장하기! (python에서만 사용 가능)
import joblib
joblib.dump(clf, 'mnist_model_10k.dmp')

print("저장 OK")
# 이 파이썬 파일 돌린곳에 저장

# # 3. 정답률 확인(신뢰도)
# result = clf.predict(test_data)
# score = metrics.accuracy_score(result,test_label)
#
# print("정답률: ", "{0:.2f}".format(score*100),"%")

## 그림사진 보기
# import matplotlib.pyplot as plt
# import numpy as np
# img = np.array(test_data[0]).reshape(28,28)
# plt.imshow(img, cmap='gray')
# plt.show()

# 4. 예측하기
# clf.predict([예측할 데이터])
# result = clf.predict([[1,0]])