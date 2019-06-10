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

list = [hex(random.randint(0,100000)) for _ in range(0,10)]

# print(list)

numlist = []

for word in list:
    word = word[2:]
    tempword = ""
    for i in range(len(word)):
        if word[i].isnumeric():
            tempword += word[i]
    numlist.append(int(tempword))

print("정렬 전: ",numlist)

# quick sorting
# size 1이면 하면 안됨
def quicksort(arr,start,end):
    if len(arr) == 1:
        return
    pivot = arr[0]
    i = start
    j = end
    while i < j:
        while arr[i] < pivot:
            i += 1
        while arr[j] > pivot:
            j -= 1
        tempNum = arr[i]
        arr[i] = arr[j]
        arr[j] = tempNum
        i += 1
    tempNum = arr[i-1]
    arr[i-1] = arr[0]
    arr[0] = tempNum
    quicksort(arr,0,i-1)
    quicksort(arr,i-1,len(arr))

quicksort(numlist,0,9)

print("퀵 정렬 후: ",list)