## 특정값의 모든 위치 출력하는 프로그램

import random

myList = [random.randint(1,5) for _ in range(10)]
print(myList)

NUMBER = 5

index = 0
findList = []

# index함수는 제일 앞에서부터 1개만
for i in range(myList.count(NUMBER)): # 5의 개수 셀 것임
    index = myList.index(NUMBER,index) # arg1은 찾을숫자, arg2는 시작점
    print(index)
    index += 1