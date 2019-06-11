
# 1. 파일 열기
inFp = open('C:/windows/win.ini', 'rt')
outFp = open('C:/images/new_win.ini','w')

# 2. 파일 읽기/쓰기
while True:
    inStr = inFp.readline()
    if not inStr: # 아무것도 없으면 FALSE
        break
    print(inStr)
    outFp.writelines(inStr)
# inStrList = inFp.readlines()
# print(inStrList)
# for line in inStrList :
#     print(line, end='')

# 3. 파일 닫기
inFp.close()
outFp.close()