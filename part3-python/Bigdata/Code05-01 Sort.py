#selection
import random

list = [ random.randint(1,99) for _ in range(20) ]
print(list)

for i in range(0, len(list)-1):
    for k in range(i+1, len(list)):
        if list[i] > list[k]:
            list[i], list[k] = list[k], list[i] # 오 이런게 되누

print(list)

# def swap(list,i,j):
#     tempNum = list[i]
#     list[i] = list[j]
#     list[j] = tempNum

#bubble

list = [ random.randint(1,99) for _ in range(20) ]
print(list)

for i in range(0, len(list)-1):
    change = False
    for k in range(0, len(list)-i-1):
        if list[k]>list[k+1]:
            list[k], list[k+1] = list[k+1], list[k]
            change = True
    if change == False:
        break

print(list)