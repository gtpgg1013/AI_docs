import random

# list = [52, 42, 45, 25, 98, 15, 31, 12, 5, 26]
list = [random.randint(0,100) for _ in range(0,10)]
print("0: ",list)

#pivot을 첫번째 element로 만들기

def partition(arr,l,r):
    pivot = arr[l]
    i = r + 1
    for j in range(r,l-1,-1):
        if arr[l] > arr[j]:
            i -= 1
            arr[i],arr[j] = arr[j],arr[i]
            print("1: ",arr)
    arr[l],arr[i-1] = arr[i-1],arr[l]
    print("2: ",arr)
    return i-1

def quicksort(arr,l,r):
    if l<r:
        p = partition(arr,l,r)
        quicksort(arr,l,p-1)
        quicksort(arr,p+1,r)

quicksort(list,0,9)
print(list)

# for i in range(9,0,-1):
#     print(i, " ")