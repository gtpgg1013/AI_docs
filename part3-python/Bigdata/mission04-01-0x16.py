import random

# selection sorting
list = []
for i in range(0,10):
    temp = hex(random.randrange(0,100000))
    list.append(temp)

print("정렬 전:",list)

for i in range(0,10):
    for k in range(i,10):
        if list[i]>list[k]:
            tempNum = list[i]
            list[i] = list[k]
            list[k] = tempNum

print("선택정렬 후:",list)

# bubble selection
list = []
for i in range(0,10):
    temp = hex(random.randrange(0,100000))
    list.append(temp)

print("정렬 전:",list)

for i in range(0,10):
    for k in range(0,10-i-1):
        if list[k]>list[k+1]:
            tempNum = list[k+1]
            list[k+1] = list[k]
            list[k] = tempNum

print("버블정렬 후 :",list)