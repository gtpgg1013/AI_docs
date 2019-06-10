# def outFunc(v1,v2): #헷갈리지 말고 내부에서만 쓰는 함수다~ 알림
#     def inFunc(n1,n2):
#         return n1 + n2
#     return inFunc(v1,v2)
#
# print(outFunc(100,200))

def hap(v1, v2):
    res = v1 + v2
    return res

hap2 = lambda v1, v2 : v1+v2 # lambda 인자들 : 리턴값

print(hap(100,200))
print(hap2(100,200))


myList = [1,2,3,4,5]
# def add10 (num):
#     return num + 10
# add10 = lambda num : num + 10

# for i in range(len(myList)):
#     myList[i] = add10((myList[i]))
# 요것들을 한방에 처리해보자 ; map함수 : 리스트에 각자 적용하는 함수!
# myList = list(map(add10, myList))
#싹다 한줄에 때려박으면 이렇게 됨
myList = list(map(lambda  num : num + 10, myList))


print(myList)

