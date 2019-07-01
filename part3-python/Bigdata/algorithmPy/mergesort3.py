import random

# list = [random.randint(0,99) for _ in range(10)]
# print(list)

def merge_sorted(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]

        l = merge_sorted(left)
        r = merge_sorted(right)
        return merge(l, r)
    else:
        return arr


def merge(left, right):
    i = 0
    j = 0
    arr = []

    while (i < len(left)) & (j < len(right)):
        if left[i] < right[j]:
            arr.append(left[i])
            i += 1
        else:
            arr.append(right[j])
            j += 1
    # ㅇㅇㅇ
    while (i < len(left)):
        arr.append(left[i])
        i += 1
    #
    while (j < len(right)):
        arr.append(right[j])
        j += 1

    return arr

# print(list)
import random

if __name__ == '__main__':
    n = input()
    # list = [random.randint(0,99) for _ in range(10)]
    list = []

    for _ in range(int(n)):
        list.append(int(input()))
    # merge_sorted(list)

    for number in merge_sorted(list):
        print(number)