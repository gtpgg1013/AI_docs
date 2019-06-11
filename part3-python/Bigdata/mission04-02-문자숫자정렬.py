import random

# list = [hex(random.randint(0,100000)) for _ in range(0,10)]
#
# # print(list)
#
# numlist = []
#
# for word in list:
#     word = word[2:]
#     tempword = ""
#     for i in range(len(word)):
#         if word[i].isnumeric():
#             tempword += word[i]
#     numlist.append(int(tempword))
#
# print("정렬 전: ",numlist)
#
# # selection sorting
# for i in range(0,10):
#     for k in range(i,10):
#         if numlist[i]>numlist[k]:
#             tempNum = numlist[i]
#             numlist[i] = numlist[k]
#             numlist[k] = tempNum
#
# print("선택정렬 후 :",numlist)
#
# list = [hex(random.randint(0,100000)) for _ in range(0,10)]
#
# # print(list)
#
# numlist = []
#
# for word in list:
#     word = word[2:]
#     tempword = ""
#     for i in range(len(word)):
#         if word[i].isnumeric():
#             tempword += word[i]
#     numlist.append(int(tempword))
#
# print("정렬 전: ",numlist)
#
# # bubble sorting
# for i in range(0,10):
#     for k in range(0,9-i):
#         if numlist[k]>numlist[k+1]:
#             tempNum = numlist[k]
#             numlist[k] = numlist[k+1]
#             numlist[k+1] = tempNum
#
# print("버블정렬 후 :",numlist)

# list = [hex(random.randint(0,100000)) for _ in range(0,10)]

# print(list)

# numlist = []
#
# for word in list:
#     word = word[2:]
#     tempword = ""
#     for i in range(len(word)):
#         if word[i].isnumeric():
#             tempword += word[i]
#     numlist.append(int(tempword))

numlist = [random.randint(1,100) for _ in range(0,10)]
# numlist = [59, 79, 36, 11, 85, 86, 66, 22, 69, 50]
# numlist = [52, 42, 45, 25, 98, 15, 31, 12, 5, 26]

print("정렬 전: ",numlist)

# quick sorting

def partition(arr, l, r):
    pivot = arr[r]
    i = l - 1
    for j in range(l,r):
        if arr[j] <= arr[r]:
            i += 1
            swap(arr, i, j)
    swap(arr, i+1, r)
    return i+1

def quicksort(arr, l, r):
    if l < r:
        p = partition(arr, l, r)
        quicksort(arr, l, p-1)
        quicksort(arr, p+1, r)

def swap(arr, i, j):
    tempNum = arr[i]
    arr[i] = arr[j]
    arr[j] = tempNum

quicksort(numlist,0,9)

print("퀵 정렬 후: ",numlist)

# size 1이면 하면 안됨
# def quicksort(arr,start,end):
#     pivot = arr[start]
#     i = start
#     j = end
#
#     # print(pivot)
#     # print(arr[i])
#     print(i)
#
#     while i<j:
#         while arr[i] <= pivot:
#             i += 1
#             print(i)
#             # print(arr[i])
#         while i<j and arr[j] > pivot:
#             j -= 1
#
#         print(i," ",j)
#
#         tempNum1 = arr[i]
#         arr[i] = arr[j]
#         arr[j] = tempNum1
#         # i += 1
#         j -= 1
#
#         print(arr)
#
#     print("--rotation1 end--")
#     if i == len(arr)-1 or end-start == 1:
#         tempNum2 = arr[i]
#         arr[i] = arr[start]
#         arr[start] = tempNum2
#         print(arr)
#         print("--rotation2 end--")
#         if i-1-start > 0:
#             quicksort(arr,start,i-1)
#         if end-i-1 > 0:
#             quicksort(arr,i+1,end)
#     else:
#         tempNum2 = arr[i-1]
#         arr[i-1] = arr[start]
#         arr[start] = tempNum2
#         print(arr)
#         print("--rotation2 end--")
#         if i-2-start > 0:
#             quicksort(arr,start,i-2)
#         if end-i > 0:
#             quicksort(arr,i,end)
#
#     # print(arr)
#     # print("--rotation2 end--")
#
#     # if i-2-start > 1:
#     #     quicksort(arr,start,i-2)
#     # if end-i > 1:
#     #     quicksort(arr,i,end)
#
#     return arr