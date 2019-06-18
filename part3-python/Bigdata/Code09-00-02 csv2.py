import csv
from tkinter.filedialog import *

## 우리회사 연봉 평균은?

filename = askopenfilename(parent=None,
                           filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))

csvList = []

with open(filename) as rfp:
    reader = csv.reader(rfp)
    headerList = next(reader) # 헤더뽑고
    sum = 0
    count = 0
    for cList in reader:
        csvList.append(cList) # 나머지 리스트에 처박기

# 가격 10퍼 인상 / cost열의 위치 찾아내기
headerList = [ data.upper().strip() for data in headerList ]
pos = headerList.index('COST')
for i in range(len(csvList)):
    rowList = csvList[i]
    cost = rowList[pos]
    cost = float(cost[1:])
    cost *= 1.1
    costStr = "${0:.2f}".format(cost)
    csvList[i][pos] = costStr
print(csvList)

# 결과 저장
saveFp = asksaveasfile(parent=None, mode='wt',
                       defaultextension='*.csv',filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))
# asksaveasfile 할 때는 saveFp.name으로 가져와야 하는구나
# 파일을 작성할 때는 : 1. mode를 w 모드로 saveFp를 가져와서
# 그걸 csv.writer 객체화해서 writer에 넣어주고
# writerow로 헤더 / 내용 작성해주면 됨
with open(saveFp.name, mode='w', newline='') as wFp:
    writer = csv.writer(wFp)
    writer.writerow(tuple(headerList))
    for row in csvList:
        print(row)
        writer.writerow(row)