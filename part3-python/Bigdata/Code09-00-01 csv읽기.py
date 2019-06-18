import csv
## 우리회사 연봉 평균은?
# head를 날리고 / (iterable이므로 한번 꺼내쓰면 끝)
# 이터러블인 놈들은 for문으로 꺼내쓰면 됨

# 파일 여는 알고리즘 : 1. open으로 객체를 만듬 as rfp
# 2. 그걸 각 파일 형식에 맞는 함수에 때려넣음 reader = csv.reader(rfp)
# 3. 그 이터러블 객체를 알아서 잘 돌려서 쓰면 됨 : headerList = next(reader)
with open('emp.csv')as rfp :
    reader = csv.reader(rfp)
    headerList = next(reader)
    sum = 0
    count = 0
    for cList in reader :
        sum += int(cList[3])
        count += 1
    avg = sum // count
    for word in headerList:
        print(word,end=' ')

    print("s' avg-->:" , avg)

    # sum = 0
    # line = rfp.readline()
    # count = 0
    # while True :
    #     line = rfp.readline()
    #     if not line :
    #         break
    #     count += 1
    #     lineList = line.split(",")
    #     sum += int(lineList[3])
    # avg = sum // count
    # print(avg)