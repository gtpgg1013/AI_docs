# i, k =0, 0
#
# for i in range(2,10,1):
#     for k in range(1,10,1):
#         print(i,"*",k,'=',i*k)

import random as rd
from random import randrange, randint #random. 안붙이고 하겠다
from random import * #걍 다 쓰겠다

count = 0
for _ in range(10): # i, k 안쓰는데 왜 있지? : 안쓸때는 지향하는게 낫다 : _로 바꾸기
    for _ in range(10):
        num = rd.randrange(0,100) # random.randint(0,99)
        print("%2d " % (num) ,end='')
        #count += 1
    print()

