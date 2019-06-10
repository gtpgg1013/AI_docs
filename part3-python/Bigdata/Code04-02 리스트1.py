import random

aa = [0,0,0,0] # 4칸 리스트 # C사용할 때는 메모리 확보를 해놔야 함

for i in range(4):
    num = random.randint(0,99)
    aa[i] = num

print(aa)