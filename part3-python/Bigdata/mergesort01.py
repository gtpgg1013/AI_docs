import random

list = [ random.randint(0,99) for _ in range(10) ]
print(list)

def mergesort(arr,l,r):
    partition(arr,l,r)

def partition(arr,l,r):
    if l < r:
        m = (l + r) // 2
        print(m)
        partition(arr, l, m)
        partition(arr, m+1,r)
        print("before merge l m r: ",l," ",m," ",r)
        merge(arr,l,r,m)
        # print(m)

def merge(arr,l,r,m):
    i = l
    j = m+1
    temparr = []

    while i<m+1 and j<r+1:
        if arr[i] > arr[j]:
            temparr.append(arr[j])
            j += 1
        else:
            temparr.append(arr[i])
            i += 1
    while i<m+1:
        temparr.append(arr[i])
        i += 1
    while j<r+1:
        temparr.append(arr[j])
        j += 1

    print("temparr: ",temparr)
    index = l
    for a in range(len(temparr)):
        arr[index] = temparr[a]
        index += 1

partition(list,0,9)

print(list)