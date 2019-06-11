list = [52, 42, 45, 25, 98, 15, 31, 12, 5, 26]
print(list)

def partition(arr, left, right):
    pivot = arr[right]
    i = left - 1
    for j in range(left, right):
        if(arr[j] <= pivot):
            i += 1
            tempNum = arr[i]
            arr[i] = arr[j]
            arr[j] = tempNum
    tempNum_ = arr[right]
    arr[right] = arr[i+1]
    arr[i+1] = tempNum_
    return i+1


def quicksort(arr, left, right):
    if left < right:
        p = partition(arr, left, right)

        quicksort(arr, left, p-1)
        quicksort(arr, p+1, right)

quicksort(list,0,9)

print(list)

