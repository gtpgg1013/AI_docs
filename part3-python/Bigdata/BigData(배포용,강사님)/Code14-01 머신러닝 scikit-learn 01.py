from sklearn import svm, metrics

#1. Classifire 생성(선택) --> 머신러닝 알고리즘 선택
clf = svm.SVC(gamma='auto')

#2. 데이터로 학습 시키기
#clf.fit( [ 훈련데이터] , [정답] )
clf.fit (  [ [0,0],
             [0,1],
             [1,0],
             [1,1]] ,
           [ 0, 1, 1, 0])
#3. 정답률을 확인 (신뢰도)
results = clf.predict([[1,0],[0,0]])

score = metrics.accuracy_score(results, [1,0])
print("정답률 :", score*100, '%')

#4. 예측하기
# # clf.predict( [예측할 데이터] )
# result = clf.predict( [ [1,0] ])
# print(result)
