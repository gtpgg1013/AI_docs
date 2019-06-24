from sklearn import svm, metrics

# 1. Classifier 생성(선택) --> 머신러닝 알고리즘 선택
clf = svm.SVC(gamma='auto')

# 2. 데이터로 학습시키기
# clf.fit( [훈련데이터], [정답])
# XOR 문제를 fit 해보기
clf.fit([[0,0],
         [0,1],
         [1,0],
         [1,1]],
        [0,1,1,0])

# 3. 정답률 확인(신뢰도)
result = clf.predict([[1,0],[0,0]])
score = metrics.accuracy_score(result,
                               [1,0])

# 4. 예측하기
# clf.predict([예측할 데이터])
# result = clf.predict([[1,0]])

print("정답률: ", "{0:.2f}".format(score*100),"%")
print(result)