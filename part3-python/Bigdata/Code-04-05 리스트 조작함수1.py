## 특정값의 모든 위치 출력하는 프로그램

import random

myList = [random.randint(1,5) for _ in range(10)]
print(myList)

NUMBER = 5

index = 0
findList = []
while True :
    try :
        index = myList.index(NUMBER, index)
        findList.append(index)
        index += 1
    except :
        break

print(findList)