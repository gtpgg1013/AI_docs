stair = []
resList = []

numOfStair = int(input())

for _ in range(numOfStair):
    stair.append(int(input()))
    resList.append(0)

resList[0] = stair[0]
resList[1] = stair[1]+resList[0]
for i in range(2,numOfStair):
    resList[i] = max(stair[i]+resList[i-2], resList[i-3]+stair[i-1]+stair[i])

print(resList[-1])


# print(stair)