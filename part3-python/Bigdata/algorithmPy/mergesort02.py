import random

# list = [random.randint(0,99) for _ in range(10)]
# print(list)

def mergesort(arr,l,r):
    if l<r:
        m = (l+r)//2
        mergesort(arr,l,m)
        mergesort(arr,m+1,r)
        # print(list)
        merge(arr,l,r,m)

def merge(arr,l,r,m):
    temparr = []
    i = l
    j = m+1
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

    index = 0
    for num in range(l,r+1):
        arr[num] = temparr[index]
        index += 1

# print(list)

if __name__ == '__main__':
    n = input()
    # print(n)
    list = []
    for _ in range(int(n)):
        list.append(int(input()))
    mergesort(list, 0, len(list)-1)

    for number in list:
        print(number)