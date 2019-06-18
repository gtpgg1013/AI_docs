from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path
import pymysql

# 전역 변수부

IP_ADDR = '192.168.56.101'; USER_NAME = 'root'; USER_PASS = '1234'
DB_NAME = 'BigData_DB'; CHAR_SET = 'utf8'

# 함수부

def selectFolder():
    global rawFileList
    foldername = askdirectory(parent=window)
    if foldername == '' or foldername == None:
        return
    edt1.insert(0, str(foldername))
    # 파일 목록 뽑기
    rawFileList = []
    for dirName, subDirList, fnames in os.walk(foldername): # os.walk에서 3가지로 쪼개고
        for fname in fnames: # fnames에서 하나씩 꺼내서
            filename, extname = os.path.basename(fname).split(".") # 확장자가 맞으면
            if extname.upper().strip() == "RAW": # RAW이면
                rawFileList.append(os.path.join(dirName,fname)) # 고놈의 절대주소를 리스트에 등록

def malloc(h,w, initValue=0):
    retMemory = []
    for _ in range(h):
        tmpList=[]
        for _ in range(w):
            tmpList.append(initValue)
        retMemory.append(tmpList)
    return retMemory

def findStat(fname):
    # 파일 읽고, 열기
    fsize = os.path.getsize(fname) # 파일의 크기(바이트)
    inH = inW = int(math.sqrt(fsize))

    ## 입력영상 메모리 확보 ##
    inimage = []
    inimage = malloc(inH, inW)

    # 파일 --> 메모리
    with open(fname, 'rb') as rFp:
        for i in range(inH):
            for k in range(inW):
                inimage[i][k] = int(ord(rFp.read(1)))

    sum = 0
    for i in range(inH):
        for k in range(inW):
            sum += inimage[i][k]
    avg = sum // (inW * inH)
    maxVal = minVal = inimage[0][0]

    for i in range(inH):
        for k in range(inW):
            if inimage[i][k] < minVal:
                minVal = inimage[i][k]
            elif inimage[i][k] > maxVal:
                maxVal = inimage[i][k]
    return avg, maxVal, minVal

import datetime
def uploadData():
    global rawFileList
    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS,
                          db=DB_NAME,charset=CHAR_SET)
    cur = con.cursor()

    # unsigned 쓰면 음수 안씀 (맨앞비트를 부호로 안쓰고 숫자를 더 씀)
    try:
        sql = '''
            CREATE TABLE rawImage_TBL (
            raw_id INT AUTO_INCREMENT PRIMARY KEY,
            raw_fname VARCHAR(30),
            raw_extname CHAR(3),
            raw_height SMALLINT, raw_width SMALLINT,
            raw_avg TINYINT UNSIGNED,
            raw_max TINYINT UNSIGNED,
            raw_min TINYINT UNSIGNED,
            raw_data LONGBLOB);
        '''
        cur.execute(sql)
    except:
        pass

    for fullname in rawFileList:
        with open(fullname, 'rb') as rfp: # rb형식으로 fullname에 있는 데이터를 open 객체로 가져옴
            binData = rfp.read() # 그거를 읽어서 binData에 넣어줌

        fname, extname = os.path.basename(fullname).split(".")
        fsize = os.path.getsize(fullname)
        height = width = int(math.sqrt(fsize))
        avgVal, maxVal, minValue = findStat(fullname) # avg, max, min 찾는 함수
        sql = "INSERT INTO rawImage_TBL(raw_id , raw_fname,raw_extname,"
        sql += "raw_height,raw_width,raw_avg,raw_max,raw_min,raw_data) "
        sql += " VALUES(NULL,'" + fname + "','" + extname +"',"
        sql += str(height) + "," + str(width) + ","
        sql += str(avgVal)+ "," + str(maxVal) + "," + str(minValue)
        sql += ", %s )" # 여기에 %s 주고 뒤에 tupleData로 넘겨줄 수 있는건가?
        tupleData = (binData,)
        cur.execute(sql,tupleData)
        con.commit()
        print('업로드 ok' + fullname)

    cur.close()
    con.close()
    print("전송완료")

# 메인 코드부
window = Tk()
window.geometry("500x200")
window.title("폴더째 Raw --> DB ver 0.03")

edt1 = Entry(window, width=50)
edt1.pack() # Entry : 텍스트 입력 혹은 출력을 위한 기입창
btnFile = Button(window, text="폴더선택",command=selectFolder); btnFile.pack()
btnUpload = Button(window, text="업로드",command=uploadData); btnUpload.pack()

window.mainloop()