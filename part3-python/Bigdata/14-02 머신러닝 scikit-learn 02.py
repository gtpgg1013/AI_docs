from sklearn import svm, metrics

## 훈련데이터, 테스트데이터 준비
train_data = [[0,0], [0,1], [1,0], [1,1]]
train_label = [0,1,1,0]
test_data = [[1,0],[0,0]]
test_label = [1,0]

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