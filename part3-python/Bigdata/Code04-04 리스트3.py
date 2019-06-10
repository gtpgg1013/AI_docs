# 이 리스트가 영상 픽셀이라 생각하고 작업하기

# 빈 메모리 확보 후에 작업하기
import random
SIZE = 4
## 1. 메모리 확보 개녕 : 타 언어 스타일
aa = [] # empty

for i in range(SIZE):
    aa.append(0)

## 2. 메모리에 확보한 값 대입 --> 파일 읽기
for i in range(SIZE):
    num = random.randint(0,99)
    aa[i] = num

## 3. 메모리 처리/조작/연산 --> 알고리즘(컴퓨터 비전, 영상처리)
sum = 0
for i in range(SIZE):
    sum += aa[i]
avg = sum / SIZE

# 4. 출력
print("영상 평균값" ,avg)
