from sklearn import svm, metrics
import pandas as pd
from sklearn.model_selection import train_test_split
'''
# 붓꽃 데이터 분류기(머신러닝)
- 개요 : 150개 붓꽃 정보(꽆받침 길이, 꽃받침 폭, 꽃잎 길이, 꽃잎 폭)\
- 종류 : 3개 (Iris-setosa / Iris-vesicolor / Iris-virginica)
- CSV파일 구하장 : iris.csv
'''
## 훈련데이터, 테스트데이터 준비
csv = pd.read_csv("C:\\Users\\user\\Desktop\\lecture_dir\\part3-python\\Bigdata\\iris.csv")
# csv = csv.sample(frac=1).reset_index(drop=True)
data = csv.iloc[:, 0:-1] # 전체 row, 맨끝 label은 빼고 다 읽어오기
label = csv.iloc[:, [-1]]

# train / test 분류 메서드 사용
train_data, test_data, train_label, test_label = train_test_split(data,label,train_size=0.1)

# 1. Classifier 생성(선택) --> 머신러닝 알고리즘 선택
clf = svm.SVC(gamma='auto')

# 2. 데이터로 학습시키기
# clf.fit( [훈련데이터], [정답])
# XOR 문제를 fit 해보기
clf.fit(train_data,train_label)

# 3. 정답률 확인(신뢰도)
result = clf.predict(test_data)
score = metrics.accuracy_score(result,test_label)

# 4. 예측하기
# clf.predict([예측할 데이터])
# result = clf.predict([[1,0]])

print("정답률: ", "{0:.2f}".format(score*100),"%")
print(result)