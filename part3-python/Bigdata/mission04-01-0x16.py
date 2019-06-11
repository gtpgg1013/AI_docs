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

# bubble sorting
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

# quick sorting

list = []
for i in range(0,10):
    temp = hex(random.randrange(0,100000))
    list.append(temp)

print("정렬 전:",list)

def partition(arr, l, r):
    pivot = arr[r]
    i = l - 1
    for j in range(l,r):
        if arr[j] <= arr[r]:
            arr[j], arr[r] = arr[r], arr[j]
    arr[i+1], arr[r] = arr[r], arr[i+1]
    return i + 1

def quicksort(arr, l, r):
    if l < r:
        p = partition(arr, l, r)
        quicksort(arr, l, p-1)
        quicksort(arr, p+1, r)

quicksort(list,0,9)
print("퀵 정렬 후:",list)