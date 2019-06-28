import csv
## 우리회사 연봉 평균은?

with open('c:/images/csv/emp.csv')as rfp :
    reader = csv.reader(rfp)
    headerList = next(reader)
    sum = 0
    count = 0
    for cList in reader :
        sum += int(cList[3])
        count += 1
    avg = sum // count
    print(avg)

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


