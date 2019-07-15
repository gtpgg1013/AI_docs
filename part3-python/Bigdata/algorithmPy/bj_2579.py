numOfStair = int(input())
tempList = []
resList = []
res = 0
for _ in range(numOfStair):
    tempList.append(int(input()))
    resList.append(0)

resList[0] = tempList[0]

# print(resList)

def changeNext(num, depth):
    global numOfStair, tempList, resList, res
    # if num == 0:
    #     changeNext(1,0)
    if depth >= 1:
        if num+2 < numOfStair and resList[num+2] < resList[num] + tempList[num+2]:
            resList[num+2] = resList[num] + tempList[num+2]
            changeNext(num+2, 0)
    else:
        if num+1 < numOfStair and resList[num+1] < resList[num] + tempList[num+1]:
            resList[num+1] = resList[num] + tempList[num+1]
            changeNext(num+1,1)
        if num+2 < numOfStair and resList[num+2] < resList[num] + tempList[num+2]:
            resList[num+2] = resList[num] + tempList[num+2]
            changeNext(num+2,0)
    # if num == 0 and depth == 0: # 이렇게하면 첫번째게 더해진 2번째로 시작함
    #     res = resList[-1]
    #     # print(res)
    #     # print(resList)
    #     for i in range(numOfStair):
    #         resList[i] = 0
    #     resList[1] = tempList[1]
    #     # print(resList)
    #     changeNext(1,0)
    #     # print("ASAS")

if numOfStair == 1:
    res = resList[-1]

elif numOfStair ==0:
    res = 0

else:
    changeNext(0,0)
    res = resList[-1]

#     for i in range(numOfStair):
#         resList[i] = 0

#     # print(resList)
#     resList[1] = tempList[1]
#     # print(resList)
#     changeNext(1,0)

# if res < resList[-1]:
#     res = resList[-1]

# print(resList)
print(res)
