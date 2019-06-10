# 3x4 크기의 리스트 조작하기
# 1. 2차원 빈 리스트 생성
# image = \
# [   [0,0,0,0],
#     [0,0,0,0],
#     [0,0,0,0]   ]

# 10x10 만들긔
ROW, COL = 10,10
image = []
temp = []

for i in range(ROW):
    temp = []
    for k in range(COL):
        temp.append(0)
    image.append(temp)

# 2. 대입 --> 파일에서 로딩
import random
for i in range(0,ROW):
    for k in range(0,COL):
        image[i][k] = random.randint(0,255)

# 3. 데이터 처리 / 변환 / 분석 --> 영상 밝게 하기
for i in range(0,ROW):
    for k in range(0,COL):
        image[i][k] += 100
        if(image[i][k]>255):
            image[i][k] = 255

# 4. 데이터 출력
for i in range(0,ROW):
    for k in range(0,COL):
        print("%3d" % (image[i][k]), end=' ')
    print()