def mergesort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    frontArr = mergesort(arr[:mid])
    backArr = mergesort(arr[mid:])

    l = r = 0
    merged_arr = []
    while l < mid and r <  len(arr) - mid : # len(arr) - mid까지 빼줘야 한당당
        if frontArr[l] > backArr[r]:
            merged_arr.append(backArr[r])
            r += 1
        else:
            merged_arr.append(frontArr[l])
            l += 1
    merged_arr.extend(frontArr[l:])
    merged_arr.extend(backArr[r:])

    return  merged_arr

import random
list = [random.randint(0,99) for _ in range(10)]
print(list)
print(mergesort(list))
