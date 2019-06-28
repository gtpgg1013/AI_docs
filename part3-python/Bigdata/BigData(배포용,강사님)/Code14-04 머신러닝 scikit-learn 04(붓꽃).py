from sklearn import svm, metrics
import pandas as pd
##0. 훈련데이터, 테스트데이터 준비
csv = pd.read_csv('c:/bigdata/iris.csv')
train_data = csv.iloc[0:120, 0:-1]
train_label = csv.iloc[0:120, [-1]]
test_data = csv.iloc[120:, 0:-1]
test_label = csv.iloc[120:, [-1]]
#1. Classifire 생성(선택) --> 머신러닝 알고리즘 선택
clf = svm.SVC(gamma='auto')
#2. 데이터로 학습 시키기
#clf.fit( [ 훈련데이터] , [정답] )
clf.fit (  train_data ,train_label)
# 3. 정답률 구하기
result = clf.predict(test_data)
score = metrics.accuracy_score(result, test_label)
print('정답률 : ', "{0:.2f}%".format(score * 100))

# 4. 내꺼 예측하기
#clf.predict( [예측할 데이터] )
result = clf.predict( [[4.1,	3.3,	1.5,	0.2] ])
print(result)
