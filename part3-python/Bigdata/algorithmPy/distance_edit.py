import numpy as np

word_s = input()
word_i = input()

# 신촌역 : 신천역

# word_s = 'delete'
# word_i = 'delegate'

len_s = len(word_s)
len_i = len(word_i)

levMat = []

for i in range(len_s+1):
    tmp = []
    for k in range(len_i+1):
        tmp.append(0)
    levMat.append(tmp)

for i in range(len_s+1):
    for k in range(len_i+1):
        if i == 0:
            levMat[i][k] = k
        if k == 0:
            levMat[i][k] = i

for i in range(1,len_s+1):
    for k in range(1,len_i+1):
        if word_s[i-1] == word_i[k-1]:
            levMat[i][k] = levMat[i-1][k-1]
        else:
            levMat[i][k] = min(levMat[i-1][k]+1, levMat[i][k-1]+1, levMat[i-1][k-1]+1)

print(np.array(levMat))
mat = np.array(levMat)
print(mat[-1,-1])