import operator

ttL = [ ('토마스', 5), ('헨리', 8), ('에드워드', 9), ('토마스', 12), ('에드워드',1)]

tD = {}
tL = []
tR, cR = 1,1

for tmpTup in ttL:
    tName = tmpTup[0]
    tWeight = tmpTup[1]
    if tName in tD:
        tD[tName] += tWeight
    else:
        tD[tName] = tWeight

print(list(tD.items()))

tL = sorted(tD.items(), key=operator.itemgetter(1), reverse=True) # sorted 함수에서 key=operator.itemgetter(1) 해주면 1번째 놈을 기준으로 sort하겠다는 뜻

rank = 1
print(tL)
print("-----------------")
print("기차","\t","총수송량","\t","순위")
print("-----------------")
for train in tL:
    print(train[0],"\t",train[1],"\t",rank)
    rank += 1