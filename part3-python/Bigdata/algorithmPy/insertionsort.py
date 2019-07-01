import random

list = [ random.randint(0,99) for _ in range(10)]
print(list)

# 앞에꺼부터 정렬시키는 sorting

for i in range(len(list)):
    key = list[i]
    j = i - 1
    while j>=0 and list[j]>key:
        list[j+1],list[j] = list[j],list[j+1]
        j -= 1
    list[j+1] = key

print(list)