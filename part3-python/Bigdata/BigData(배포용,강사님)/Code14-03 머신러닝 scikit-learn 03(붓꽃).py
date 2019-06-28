from sklearn import svm, metrics
'''
# 붓꽃 데이터 분류기 (머신러닝)
- 개요 : 150개 붓꽃 정보(꽃받침 길이, 꽃받침 폭, 꽃잎 길이, 꽃잎 폭)
- 종류 : 3개 (Iris-setosa, Iris-vesicolor, Iris-virginica)
- 
'''

##0. 훈련데이터, 테스트데이터 준비

#1. Classifire 생성(선택) --> 머신러닝 알고리즘 선택
clf = svm.SVC(gamma='auto')
#2. 데이터로 학습 시키기
#clf.fit( [ 훈련데이터] , [정답] )
clf.fit (  train_data ,train_label)
#3. 정답률을 확인 (신뢰도)
results = clf.predict(test_data)
score = metrics.accuracy_score(results, test_label)
print("정답률 :", score*100, '%')

#4. 예측하기
# # clf.predict( [예측할 데이터] )
# result = clf.predict( [ [1,0] ])
# print(result)
