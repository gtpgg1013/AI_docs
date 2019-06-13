from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path

################################
#######   함수 선언부   ########
################################

# 메모리를 할당해서 리스트(참조)를 반환하는 함수
# 메모리 할당 과정 똑바로 기억할 것 : 2차원 배열이기 때문에 templist이용해서 2중포문 써야함
# initValue라는 변수에 초깃값을 줘서 활용 가능
def malloc(h, w, initValue=0) :
    retMemory = []
    for _ in range(h):
        templist = []
        for _ in range(w):
            templist.append(initValue)
        retMemory.append(templist)
    return retMemory

# 파일을 메모리로 로딩하는 함수
def loadImage(fname):
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    fsize = os.path.getsize(fname) # 파일의 크기(바이트)
    inH = inW = int(math.sqrt(fsize)) # 핵심 코드 : 파일의 메모리로부터 H,W 크기 구해냄

    # 입력영상 메모리 확보
    # inImage 이차원배열 초기화
    inImage = [] # 요거 초기화 안시키면 계속 쌓여서 안됨!
    inImage = malloc(inH, inW)

    # 파일에서 메모리로 가져오기
    with open(filename, 'rb') as rFp:
        for i in range(inH):
            for k in range(inW):
                inImage[i][k] = int(ord(rFp.read(1))) # 이렇게 하면 1바이트씩 읽어서 int, 정수로 바꿔줌

    # print(inH,outW)
    # print(ord(inImage[100][100])) # ord는 이진문자 - 읽을 수 있는 문자로!

# 파일 선택해서 메모리로 로딩하는 함수
def openImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    filename = askopenfilename(parent=window, filetypes=(("RAW파일", "*.raw"), ("모든 파일", "*.*")))
    if filename == '' or filename == None:
        return
    loadImage(filename)
    equalImage()

import struct
def saveImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    saveFp = asksaveasfile(parent=window, mode="wb",defaultextension='*.raw',filetypes=(("RAW파일", "*.raw"), ("모든 파일", "*.*")))
    if saveFp == '' or saveFp == None:
        return
    for i in range(outH):
        for k in range(outW):
            saveFp.write(struct.pack('B',outImage[i][k])) # B는 바이너리
    saveFp.close()

def displayImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    if canvas != None: # 예전에 실행된 적잉 있다
        canvas.destroy()

    # 화면 크기 조절
    window.geometry(str(outH)+'x'+str(outW)) # 벽
    canvas = Canvas(window, height=outH, width=outW) # 보드
    paper = PhotoImage(height=outH, width=outW) # 빈 종이
    canvas.create_image((outH//2, outW//2), image=paper, state='normal')

    # 출력 영상을 화면에 한점씩 찍기
    # # 요게 느려서 화면이 늦게 뜸
    # for i in range(outH):
    #     for k in range(outW):
    #         r = g = b = outImage[i][k]
    #         paper.put("#%02x%02x%02x" % (r,g,b), (k,i)) # 16진수 문자열 포맷팅, i,k로 위치 지정해주기
    ## 성능 개선
    # string 통째로 넣어서 받으면 더 빠르다
    rgbStr = '' # 전체 픽셀의 문자열을 저장
    for i in range(outH):
        tmpStr = ''
        for k in range(outW):
            r = g = b = outImage[i][k]
            tmpStr += ' #%02x%02x%02x' % (r,g,b) # 문자열 구분하려면 한칸 떼줘야 함
        rgbStr += '{' + tmpStr + '} ' # 문자열 구분하려면 한칸 떼줘야 함
    paper.put(rgbStr) # 성능 개선을 위해


    # 캔버스에 바인드 걸자
    canvas.bind('<Button-1>', mouseClick)
    canvas.bind('<ButtonRelease-1>', mouseDrop)
    canvas.pack(expand=1, anchor=CENTER)

########################################################
#####   컴퓨터비전(영상처리) 알고리즘 함수 모음   ######
########################################################

# 동일영상 알고리즘
def equalImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH; outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][k]

    displayImage()

# 밝게/어둡게 하기 알고리즘
def plusminusImage(event):
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH; outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘
    if event == 1:
        value = askinteger("밝게하기", "밝게할 값", minvalue=1, maxvalue=255)
        for i in range(inH):
            for k in range(inW):
                outImage[i][k] = inImage[i][k] + value
                if outImage[i][k] > 255:
                    outImage[i][k] = 255
    else:
        value = askinteger("어둡게하기", "어둡게할 값", minvalue=1, maxvalue=255)
        for i in range(inH):
            for k in range(inW):
                outImage[i][k] = inImage[i][k] - value
                if outImage[i][k] < 0:
                    outImage[i][k] = 0
    displayImage()

# 곱셈나눗셈 알고리즘
def mulDivImage(event):
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH; outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘
    if event == 1:
        value = askinteger("곱하기", "곱할 값", minvalue=1, maxvalue=255)
        for i in range(inH):
            for k in range(inW):
                outImage[i][k] = inImage[i][k] * value
                if outImage[i][k] > 255:
                    outImage[i][k] = 255
    else:
        value = askinteger("나누기", "나눌 값", minvalue=1, maxvalue=255)
        for i in range(inH):
            for k in range(inW):
                outImage[i][k] = inImage[i][k] // value
                if outImage[i][k] < 0:
                    outImage[i][k] = 0
    displayImage()

# 화소값 반전 알고리즘
def reverseImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH; outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘

    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = 255 - inImage[i][k]

    displayImage()

# 이진화 알고리즘
def biImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH; outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘

    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] < 127:
                outImage[i][k] = 0
            else:
                outImage[i][k] = 255

    displayImage()

# 축소(통계) 알고리즘
def shrinkStatImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    ## 중요코드 : 출력영상 크기 결정 ##
    value = askinteger("안내", "축소 배율을 입력해주세요")
    outH = inH // value
    outW = inW // value
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘

    tl1 = [_ for _ in range(value)]
    tl2 = [_ for _ in range(value)]

    for i in range(outH):
        for k in range(outW):
            tempavg = 0
            for m in tl1:
                for n in tl2:
                    tempavg += inImage[i*value+m][k*value+n]
            tempavg = tempavg // (value*value)
            outImage[i][k] = tempavg

    # 더 쉽게 할 수 있는 방법도 있다? : inH / inW 만큼 포문돌려서 전부 더해주고 마지막에 나눠줌

    displayImage()

# 영상 확대 알고리즘(양선형 보간)
def zoomImage2(): # 빈 부분은 어떻게 할지 결정해야 할 것임
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    value = askinteger("안내", "확대 배율을 입력해주세요")
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH * value
    outW = inW * value
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘
    rH, rW, iH, iW = [0] * 4 # 실수 위치 및 정수 위치
    x, y = 0, 0 # 실수와 정수의 차이값
    C1, C2, C3, C4 = [0] * 4 # 결정할 위치(N)의 상하좌우 픽셀
    for i in range(outH):
        for k in range(outW):
            rH = i / value ; rW = k / value
            iH = int(rH) ; iW = int(rW)
            x = rW - iW ; y = rH - iH
            if 0 <= iH < inH-1 and 0 <= iW < inW-1:
                C1 = inImage[iH][iW]
                C2 = inImage[iH][iW+1]
                C3 = inImage[iH+1][iW]
                C4 = inImage[iH+1][iW+1]
                newValue = C1*(1-y)*(1-x) + C2*(1-y)*x + C3*y*x + C4*y*(1-x)
                outImage[i][k] = int(newValue)

    displayImage()

# 히스토그램
# 영상의 분포를 확인하는게 더 중요함! : 실제로 더 중요함
# 히스토그램의 부정확함을 보고 영상 처리에 문제가 있을 수 있음을 확인할 수 있다 : 무슨 값이 누락됬다던가
# 변화 후의 히스토그램과 비교해보는게 좋지!
import matplotlib.pyplot as plt
def histoImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    incountlist = [0] * 256
    outcountlist = [0] * 256

    for i in range(inH):
        for k in range(inW):
            incountlist[inImage[i][k]] += 1

    for i in range(outH):
        for k in range(outW):
            outcountlist[outImage[i][k]] += 1

    # 좀만 있다가 해보자
    fig = plt.figure()
    hist1 = fig.add_subplot(2,1,1)
    hist2 = fig.add_subplot(2,1,2)
    hist1.plot(incountlist)
    hist2.plot(outcountlist)
    plt.show()

# 평균 표시 대화상자
def showAverage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    inAvg = outAvg = 0

    for i in range(inH):
        for k in range(inW):
            inAvg += inImage[i][k]

    for i in range(outH):
        for k in range(outW):
            outAvg += outImage[i][k]

    inAvg = inAvg / (inH*inW)
    outAvg = outAvg / (outH*outH)
    messagebox.showinfo("입/출력 영상의 평균값", "입력 영상의 평균값 : {}, 출력 영상의 평균값: {}".format(inAvg,outAvg))

# 포스터라이징 알고리즘 : 경계값으로 뭉치게 하기
def posterizingImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH; outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘

    number = askinteger("안내", "경계값 개수를 입력해주세요, 2 이상")
    limlist = []
    firstlim = int(255 / number)
    lim = 0

    # 경계선 리스트 작성
    while True:
        lim += firstlim
        if lim > 255:
            break
        limlist.append(lim)

    for i in range(inH):
        for k in range(inW):
            for lim in limlist:
                if inImage[i][k] < lim:
                    outImage[i][k] = lim
                    break

    displayImage()

# 감마 보정 알고리즘 : 감마함수 활용
def gammaCorrectionImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH; outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘

    gamma = askfloat("안내","감마값을 입력해 주세요")
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = int(math.pow(inImage[i][k], 1/gamma))

    displayImage()

# 명암 대비 스트레칭
def strectchImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH; outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘

    # 원래 -1, 256 해도 되나, 보통 이런식으로 많이씀(버그 x)
    maxpixel = inImage[0][0]
    minpixel = inImage[0][0]

    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] > maxpixel:
                maxpixel = inImage[i][k]
            if inImage[i][k] < minpixel:
                minpixel = inImage[i][k]

    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = int(((inImage[i][k] - minpixel) / (maxpixel - minpixel)) * 255)

    displayImage()

# End-In 알고리즘 # 양쪽 날리고픈 부분 날리기
def endInImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH; outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘

    # 원래 -1, 256 해도 되나, 보통 이런식으로 많이씀(버그 x)
    maxpixel = inImage[0][0]
    minpixel = inImage[0][0]

    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] > maxpixel:
                maxpixel = inImage[i][k]
            if inImage[i][k] < minpixel:
                minpixel = inImage[i][k]

    minAdd = askinteger("최소", "최소추가",minvalue=0,maxvalue=255)
    maxAdd = askinteger("최대", "최대추가", minvalue=0,maxvalue=255)

    minpixel += minAdd
    maxpixel -= maxAdd

    for i in range(inH):
        for k in range(inW):
            value = int(((inImage[i][k] - minpixel) / (maxpixel - minpixel)) * 255)
            if value < 0:
                value = 0
            elif value > 255:
                value = 255
            outImage[i][k] = value

    displayImage()

# 히스토그램 평활화 알고리즘
def histFlatImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH; outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘

    histlist = [ 0 for _ in range(0,256) ]
    sumlist = []
    normlist = []

    # 각 색깔(0~255) 별 빈도 리스트 만들기
    for i in range(inH): # 값을 넣는 것이 아니라 빈도수를 넣는 것임
        for k in range(inW):
            histlist[inImage[i][k]] += 1

    # print(histlist)
    # print(len(histlist))

    # 각 색깔별 누적빈도 리스트 만들기
    sum = 0
    for hist in histlist:
        sum += hist
        sumlist.append(sum)

    # 각 색깔별 정규화된 빈도 리스트 만들기
    for sum in sumlist:
        norm = int(( sum / (inH * inW) ) * 255)
        normlist.append(norm)

    # print(histlist)
    # print(sum)
    # print(normlist)

    # 만들어진 정규값 리스트를 이용해서 값 변환시키기 : 쭉- 늘림!
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = normlist[inImage[i][k]]

    displayImage()

# 파라볼라 알고리즘
def parabolaImage(param):
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH; outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘
    # LookUpTable 기법 활용
    LUT = [0 for _ in range(256)]
    if param == 1:
        for input in range(256):
            LUT[input] = int(255 - 255 * math.pow(input / 128 - 1, 2))  # 복잡한 계산 256*256 하기 힘드므로 답지를 미리 가지고 값만 넣어주기!
        for i in range(inH):
            for k in range(inW):
                v = LUT[inImage[i][k]]
                outImage[i][k] = int(v)
    else:
        for input in range(256):
            LUT[input] = int(255 * math.pow(input / 128 - 1, 2))  # 복잡한 계산 256*256 하기 힘드므로 답지를 미리 가지고 값만 넣어주기!
        for i in range(inH):
            for k in range(inW):
                v = LUT[inImage[i][k]]
                outImage[i][k] = int(v)

    displayImage()

# 동일영상 알고리즘
def updownImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH; outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘
    for i in range(inH):
        for k in range(inW):
            outImage[inH-i-1][k] = inImage[i][k]

    displayImage()

# 화면이동 알고리즘
def moveImage(param):
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH; outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘
    value = askinteger("안내", "이동할 값을 입력해 주세요")
    if param == 1: # 아래로
        for i in range(inH):
            for k in range(inW):
                # print(i," ",k)
                if i+value<outW:
                    # print(i," ",k)
                    outImage[i+value][k] = inImage[i][k]
    elif param == 2: # 위로
        for i in range(inH):
            for k in range(inW):
                if i-value>=0:
                    outImage[i-value][k] = inImage[i][k]
    elif param == 3: # 오른쪽으로
        for i in range(inH):
            for k in range(inW):
                if k+value<outH:
                    outImage[i][k+value] = inImage[i][k]
    else: # 왼쪽으로
        for i in range(inH):
            for k in range(inW):
                if k-value>=0:
                    outImage[i][k-value] = inImage[i][k]

    displayImage()

# 마우스 클릭 / 드랍으로
def moveClickImage():
    global panYN
    panYN = True
    canvas.configure(cursor='Mouse')

    displayImage()

def mouseClick(event):
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global sx,sy,ex,ey,panYN
    if panYN == False:
        return
    sx = event.x; sy = event.y

def mouseDrop(event):
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global sx,sy,ex,ey,panYN
    if panYN == False:
        return
    ex = event.x; ey = event.y
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH; outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘
    # x, y 이동량 구하기
    mx = sx - ex ; my = sy - ey
    for i in range(inH):
        for k in range(inW):
            if 0 <= i-my < outH and 0 <= k-mx < outW:
                outImage[i-my][k-mx] = inImage[i][k]
    panYN = False

    displayImage()

# 회전변환 알고리즘
def rotateImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH
    outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘
    value = math.radians(askinteger("안내", "회전할 각도를 입력해 주세요"))
    centerh = inH//2
    centerw = inW//2
    centerw = inW//2
    for i in range(inH):
        for k in range(inW):
            ys = i ; xs = k
            xd = int((xs-centerw)*math.cos(value) - (ys-centerh)*math.sin(value)) + centerw
            yd = int((xs-centerw)*math.sin(value) + (ys-centerh)*math.cos(value)) + centerh
            if yd >= 0 and yd < outH and xd >= 0 and xd < outW:
                outImage[yd][xd] = inImage[i][k]

    displayImage()

# 회전 + 확대 알고리즘
def rotateZoomImage1():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    ## 중요코드 : 출력영상 크기 결정 ##
    rotvalue = math.radians(askinteger("안내", "회전할 각도를 입력해 주세요"))
    zoomvalue = askinteger("안내", "확대할 값을 입력해주세요")
    outH = inH * zoomvalue
    outW = inW * zoomvalue
    # 메모리 할당 (틀만들기)
    tmpInImage = malloc(inH,inW)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘
    centerh = inH//2
    centerw = inW//2
    centerw = inW//2

    # 회전
    for i in range(inH):
        for k in range(inW):
            ys = i ; xs = k
            xd = int((xs-centerw)*math.cos(rotvalue) - (ys-centerh)*math.sin(rotvalue)) + centerw
            yd = int((xs-centerw)*math.sin(rotvalue) + (ys-centerh)*math.cos(rotvalue)) + centerh
            if yd >= 0 and yd < inH and xd >= 0 and xd < inW:
                tmpInImage[yd][xd] = inImage[i][k]

    # 확대
    for i in range(outH):
        for k in range(outW):
            outImage[i][k] = tmpInImage[i//zoomvalue][k//zoomvalue]

    displayImage()

# 회전 + 확대 (양선형 보간) 알고리즘
def rotateZoomImage2():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    ## 중요코드 : 출력영상 크기 결정 ##
    rotvalue = math.radians(askinteger("안내", "회전할 각도를 입력해 주세요"))
    zoomvalue = askinteger("안내", "확대할 값을 입력해주세요")
    outH = inH * zoomvalue
    outW = inW * zoomvalue
    # 메모리 할당 (틀만들기)
    tmpInImage = malloc(inH,inW) # 중간 징검다리
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘
    centerh = inH//2
    centerw = inW//2

    # 회전
    for i in range(inH):
        for k in range(inW):
            ys = i ; xs = k
            xd = int((xs-centerw)*math.cos(rotvalue) - (ys-centerh)*math.sin(rotvalue)) + centerw
            yd = int((xs-centerw)*math.sin(rotvalue) + (ys-centerh)*math.cos(rotvalue)) + centerh
            if yd >= 0 and yd < inH and xd >= 0 and xd < inW:
                tmpInImage[yd][xd] = inImage[i][k]

    # 확대
    rH, rW, iH, iW = [0] * 4  # 실수 위치 및 정수 위치
    x, y = 0, 0  # 실수와 정수의 차이값
    C1, C2, C3, C4 = [0] * 4  # 결정할 위치(N)의 상하좌우 픽셀
    for i in range(outH):
        for k in range(outW):
            rH = i / zoomvalue
            rW = k / zoomvalue
            iH = int(rH)
            iW = int(rW)
            x = rW - iW
            y = rH - iH
            if 0 <= iH < inH - 1 and 0 <= iW < inW - 1:
                C1 = tmpInImage[iH][iW]
                C2 = tmpInImage[iH][iW + 1]
                C3 = tmpInImage[iH + 1][iW]
                C4 = tmpInImage[iH + 1][iW + 1]
                newValue = C1 * (1 - y) * (1 - x) + C2 * (1 - y) * x + C3 * y * x + C4 * y * (1 - x)
                outImage[i][k] = int(newValue)

    displayImage()

def shrinkImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    ## 중요코드 : 출력영상 크기 결정 ##
    value = askinteger("안내", "축소 배율을 입력해주세요")
    outH = inH // value
    outW = inW // value
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘

    for i in range(outH):
        for k in range(outW):
            # forwarding 방식
            # newi = int(i/value)
            # newk = int(k/value)
            # outImage[newi][newk] = inImage[i][k]
            # backwarding 방식
            outImage[i][k] = inImage[i*value][k*value]

    displayImage()

def zoomImage(): # 빈 부분은 어떻게 할지 결정해야 할 것임
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    value = askinteger("안내", "확대 배율을 입력해주세요")
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH * value
    outW = inW * value
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘

    # 포워딩으로하면 일케 어렵게 해야해...
    tl1 = [_ for _ in range(value)]
    tl2 = [_ for _ in range(value)]

    for i in range(inH):
        for k in range(inW):
            newi = int(i * value)
            newk = int(k * value)
            # for i in range(value):
            for m in tl1:
                for n in tl2:
                    outImage[newi-m][newk-n] = inImage[i][k]

    # 더 쉽게할 수 있다... # 백워딩!
    # for i in range(outH):
    #     for k in range(outW):
    #         outImage[i][k] = inImage[i//value][k//value]

    # 프린트 20page 양선형보간법

    displayImage()

# 엠보싱 & 블러링 & 가우시안 필터링 & 샤프닝 효과 이미지
def embossBlurGausSharpingImage(param):
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH
    outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘

    MSIZE = 3
    if param == 1: # 엠보싱
        mask = [ [-1,0,0],
                 [ 0,0,0],
                 [ 0,0,1] ]
    elif param == 2: # 블러링
        mask = [[1/9, 1/9, 1/9],
                [1/9, 1/9, 1/9],
                [1/9, 1/9, 1/9]]
    elif param == 3: # 가우시안 필터링
        mask = [[1/16, 1/8, 1/16],
                [1/8, 1/4, 1/8],
                [1/16, 1/8, 1/16]]
    elif param == 4: # 샤프닝1
        mask = [[-1,-1,-1],
                [-1, 9,-1],
                [-1,-1,-1]]
    else: # 샤프닝2
        mask = [[0,-1, 0],
                [-1,5,-1],
                [0,-1, 0]]

    # 임시 입력영상 메모리 확보 : 0으로 사방에 패딩 넣어줘야하는데 inImage는 건드리면 안됨! 원본훼손하면 안됨
    tmpInImage = malloc(inH+MSIZE-1, inW+MSIZE-1) # 위아래 좌우 : 마스크사이즈-1 만큼 늘려줘야 함
    tmpOutImage = malloc(outH,outW) # 나가는 사이즈는 똑같이

    # 원 입력 --> 임시 입력
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i+MSIZE//2][k+MSIZE//2] = inImage[i][k] # MSIZE//2 해주면 가변적으로 됨

    # 회선연산 : 마스크 윈도우 슬라이딩하기
    # MSIZE를 사용한 범위 지정에 신경쓰자
    for i in range(MSIZE//2, inH+MSIZE//2):
        for k in range(MSIZE//2, inW+MSIZE//2):
            # 각 점을 처리
            S = 0.0
            for m in range(0,MSIZE):
                for n in range(0,MSIZE):
                    S += mask[m][n]*tmpInImage[i+m-MSIZE//2][k+n-MSIZE//2]
            tmpOutImage[i-MSIZE//2][k-MSIZE//2] = S

    # 127 더하기 : 좀더 밝게해주면 잘 보임
    for i in range(outH):
        for k in range(outW):
            tmpOutImage[i][k] += 127

    # 임시 출력 --> 원 출력
    for i in range(outH):
        for k in range(outW):
            value = tmpOutImage[i][k]
            if value > 255:
                value = 255
            elif value < 0:
                value = 0
            outImage[i][k] = int(value)

    displayImage()

def boundaryFreqencyImage(param):
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH
    outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘

    if param == 1: # prewitt 수평경계선
        MSIZE = 3
        mask = [ [-1,-1,-1],
                 [ 0,0,0],
                 [ 1,1,1] ]
    elif param == 2: # prewitt 수직경계선
        MSIZE = 3
        mask = [[1, 0, -1],
                [1, 0, -1],
                [1, 0, -1]]
    elif param == 3: # Sobel 수평경계선
        MSIZE = 3
        mask = [[-1, -2, -1],
                [0, 0, 0],
                [1, 2, 1]]
    elif param == 4: # Sobel 수직경계선
        MSIZE = 3
        mask = [[1, 0, -1],
                [2, 0, -2],
                [1, 0, -1]]
    elif param == 5: # Roberts 수직경계선
        MSIZE = 2
        mask = [[0,-1],
                [1,0]]
    elif param == 6: # Roberts 수평경계선
        MSIZE = 2
        mask = [[-1,0],
                [0,1]]
    elif param == 7: # High Frequency
        MSIZE = 3
        mask = [[-1/9, -1/9, -1/9],
                [-1/9, 8/9, -1/9],
                [-1/9, -1/9, -1/9]]
    elif param == 8: # Low Frequency
        MSIZE = 3
        mask = [[1/9, 1/9, 1/9],
                [1/9, 1/9, 1/9],
                [1/9, 1/9, 1/9]]


    # 임시 입력영상 메모리 확보 : 0으로 사방에 패딩 넣어줘야하는데 inImage는 건드리면 안됨! 원본훼손하면 안됨
    tmpInImage = malloc(inH+MSIZE-1, inW+MSIZE-1) # 위아래 좌우 : 마스크사이즈-1 만큼 늘려줘야 함
    tmpOutImage = malloc(outH,outW) # 나가는 사이즈는 똑같이

    # 원 입력 --> 임시 입력
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i+MSIZE//2][k+MSIZE//2] = inImage[i][k] # MSIZE//2 해주면 가변적으로 됨

    # 회선연산 : 마스크 윈도우 슬라이딩하기
    # MSIZE를 사용한 범위 지정에 신경쓰자
    for i in range(MSIZE//2, inH+MSIZE//2):
        for k in range(MSIZE//2, inW+MSIZE//2):
            # 각 점을 처리
            S = 0.0
            for m in range(0,MSIZE):
                for n in range(0,MSIZE):
                    S += mask[m][n]*tmpInImage[i+m-MSIZE//2][k+n-MSIZE//2]
            tmpOutImage[i-MSIZE//2][k-MSIZE//2] = S

    # 127 더하기 : 좀더 밝게해주면 잘 보임
    for i in range(outH):
        for k in range(outW):
            tmpOutImage[i][k] += 127

    # 임시 출력 --> 원 출력
    for i in range(outH):
        for k in range(outW):
            value = tmpOutImage[i][k]
            if value > 255:
                value = 255
            elif value < 0:
                value = 0
            outImage[i][k] = int(value)

    displayImage()

def edgeImage():
    pass

def edgeLoGDoGImage(param):
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH
    outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘

    MSIZE = 3
    if param == 1:  # LoG1
        mask = [[0, -1, 0],
                [-1, 4, -1],
                [0, -1, 0]]
    elif param == 2:  # LoG2
        mask = [[1, 1, 1],
                [1, -8, 1],
                [1, 1, 1]]
    elif param == 3:  # DoG1
        mask = [[0, -1, 0],
                [-1, 4, -1],
                [0, -1, 0]]
    elif param == 4:  # DoG2
        mask = [[1 / 9, 1 / 9, 1 / 9],
                [1 / 9, 1 / 9, 1 / 9],
                [1 / 9, 1 / 9, 1 / 9]]


    # 임시 입력영상 메모리 확보 : 0으로 사방에 패딩 넣어줘야하는데 inImage는 건드리면 안됨! 원본훼손하면 안됨
    tmpInImage = malloc(inH + MSIZE - 1, inW + MSIZE - 1)  # 위아래 좌우 : 마스크사이즈-1 만큼 늘려줘야 함
    tmpOutImage = malloc(outH, outW)  # 나가는 사이즈는 똑같이

    # 원 입력 --> 임시 입력
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + MSIZE // 2][k + MSIZE // 2] = inImage[i][k]  # MSIZE//2 해주면 가변적으로 됨

    # 회선연산 : 마스크 윈도우 슬라이딩하기
    # MSIZE를 사용한 범위 지정에 신경쓰자
    for i in range(MSIZE // 2, inH + MSIZE // 2):
        for k in range(MSIZE // 2, inW + MSIZE // 2):
            # 각 점을 처리
            S = 0.0
            for m in range(0, MSIZE):
                for n in range(0, MSIZE):
                    S += mask[m][n] * tmpInImage[i + m - MSIZE // 2][k + n - MSIZE // 2]
            tmpOutImage[i - MSIZE // 2][k - MSIZE // 2] = S

    # 127 더하기 : 좀더 밝게해주면 잘 보임
    for i in range(outH):
        for k in range(outW):
            tmpOutImage[i][k] += 127

    # 임시 출력 --> 원 출력
    for i in range(outH):
        for k in range(outW):
            value = tmpOutImage[i][k]
            if value > 255:
                value = 255
            elif value < 0:
                value = 0
            outImage[i][k] = int(value)

    displayImage()

def edgeDoGImage():
    pass

def multiBlurringImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH
    outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘

    MSIZE = askinteger("안내", "블러링 마스크의 크기를 입력하세요 : 3,5,7,9...")
    mask = [[ 1/(MSIZE*MSIZE) for _ in range(MSIZE)] for _ in range(MSIZE)]

    # 임시 입력영상 메모리 확보 : 0으로 사방에 패딩 넣어줘야하는데 inImage는 건드리면 안됨! 원본훼손하면 안됨
    tmpInImage = malloc(inH + MSIZE - 1, inW + MSIZE - 1)  # 위아래 좌우 : 마스크사이즈-1 만큼 늘려줘야 함
    tmpOutImage = malloc(outH, outW)  # 나가는 사이즈는 똑같이

    # 원 입력 --> 임시 입력
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + MSIZE // 2][k + MSIZE // 2] = inImage[i][k]  # MSIZE//2 해주면 가변적으로 됨

    # 회선연산 : 마스크 윈도우 슬라이딩하기
    # MSIZE를 사용한 범위 지정에 신경쓰자
    for i in range(MSIZE // 2, inH + MSIZE // 2):
        for k in range(MSIZE // 2, inW + MSIZE // 2):
            # 각 점을 처리
            S = 0.0
            for m in range(0, MSIZE):
                for n in range(0, MSIZE):
                    S += mask[m][n] * tmpInImage[i + m - MSIZE // 2][k + n - MSIZE // 2]
            tmpOutImage[i - MSIZE // 2][k - MSIZE // 2] = S

    # 127 더하기 : 좀더 밝게해주면 잘 보임
    for i in range(outH):
        for k in range(outW):
            tmpOutImage[i][k] += 127

    # 임시 출력 --> 원 출력
    for i in range(outH):
        for k in range(outW):
            value = tmpOutImage[i][k]
            if value > 255:
                value = 255
            elif value < 0:
                value = 0
            outImage[i][k] = int(value)

    displayImage()

################################
#####   전역변수 선언부   ######
################################

inImage, outImage = [], [] ; inH, inW, outH, outW = [0] * 4
window, canvas, paper = None, None, None
filename = ""
# 마우스 사용할꺼니 안할꺼니 확인하는 전역변수
panYN = False
# 마우스 좌표 저장할 변수
sx,sy,ex,ey = [0] * 4

################################
#######   메인 코드부   ########
################################

window = Tk()
window.geometry("400x400")
window.resizable(True, True)

# 마우스 이벤트


mainMenu = Menu(window)
window.config(menu=mainMenu)
window.title("컴퓨터 비전(딥러닝 기법) ver 0.03")

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일",menu=fileMenu)
fileMenu.add_command(label="파일 열기",command=openImage)
fileMenu.add_command(label="파일 저장",command=saveImage)

comVisionMenu1 = Menu(mainMenu)
mainMenu.add_cascade(label="화소점처리",menu=comVisionMenu1)
comVisionMenu1.add_command(label="밝게하기",command=lambda: plusminusImage(1))
comVisionMenu1.add_command(label="어둡게하기",command=lambda: plusminusImage(2))
comVisionMenu1.add_command(label="영상 곱셈",command=lambda:mulDivImage(1))
comVisionMenu1.add_command(label="영상 나눗셈",command=lambda:mulDivImage(2))
comVisionMenu1.add_command(label="화소값 반전",command=reverseImage)
comVisionMenu1.add_command(label="입력/출력 영상의 평균값 구하기",command=showAverage) # 출력은 메시지박스
comVisionMenu1.add_command(label="Posterizing",command=posterizingImage)
comVisionMenu1.add_command(label="Gamma 보정",command=gammaCorrectionImage)
comVisionMenu1.add_command(label="명암 대비 스트레칭",command=strectchImage)
comVisionMenu1.add_command(label="End-In 탐색",command=endInImage)
comVisionMenu1.add_command(label="히스토그램 평활화",command=histFlatImage)
comVisionMenu1.add_command(label="파라볼라 변환(캡)",command=lambda : parabolaImage(1))
comVisionMenu1.add_command(label="파라볼라 변환(컵)",command=lambda : parabolaImage(2))

comVisionMenu2 = Menu(mainMenu)
mainMenu.add_cascade(label="화소(통계)",menu=comVisionMenu2)
comVisionMenu2.add_command(label="이진화",command=biImage)
comVisionMenu2.add_command(label="축소(평균)",command=shrinkStatImage)
comVisionMenu2.add_command(label="확대(양선형보간)",command=zoomImage2)
comVisionMenu2.add_separator()
comVisionMenu2.add_command(label="히스토그램",command=histoImage)

comVisionMenu3 = Menu(mainMenu)
mainMenu.add_cascade(label="기하학 처리",menu=comVisionMenu3)
comVisionMenu3.add_command(label="상하반전",command=updownImage)
moveMenu = Menu(comVisionMenu3)
comVisionMenu3.add_cascade(label="이동",menu=moveMenu)
moveMenu.add_command(label="아래로",command=lambda :moveImage(1))
moveMenu.add_command(label="위로",command=lambda :moveImage(2))
moveMenu.add_command(label="오른쪽",command=lambda :moveImage(3))
moveMenu.add_command(label="왼쪽",command=lambda :moveImage(4))
moveMenu.add_command(label="마우스로 이동",command=moveClickImage)
comVisionMenu3.add_command(label="회전",command=rotateImage)
comVisionMenu3.add_command(label="회전후 확대",command=rotateZoomImage1)
comVisionMenu3.add_command(label="회전후 확대(양선형 보간)",command=rotateZoomImage2)
comVisionMenu3.add_command(label="축소",command=shrinkImage)
comVisionMenu3.add_command(label="확대",command=zoomImage)

comVisionMenu4 = Menu(mainMenu)
mainMenu.add_cascade(label="화소 영역 처리", menu=comVisionMenu4)
comVisionMenu4.add_command(label="엠보싱처리",command=lambda:embossBlurGausSharpingImage(1))
comVisionMenu4.add_command(label="블러링",command=lambda:embossBlurGausSharpingImage(2))
sharpingMenu = Menu(comVisionMenu4)
comVisionMenu4.add_cascade(label="샤프닝",menu=sharpingMenu)
sharpingMenu.add_command(label="회선마스크1",command=lambda :embossBlurGausSharpingImage(4))
sharpingMenu.add_command(label="회선마스크2",command=lambda :embossBlurGausSharpingImage(5))
boundaryMenu = Menu(comVisionMenu4)
comVisionMenu4.add_cascade(label="경계선 검출",menu=boundaryMenu)
boundaryMenu.add_command(label="Prewitt 수평 경계선",command=lambda :boundaryFreqencyImage(1))
boundaryMenu.add_command(label="Prewitt 수직 경계선",command=lambda :boundaryFreqencyImage(2))
boundaryMenu.add_command(label="Sobel 수평 경계선",command=lambda :boundaryFreqencyImage(3))
boundaryMenu.add_command(label="Sobel 수직 경계선",command=lambda :boundaryFreqencyImage(4))
boundaryMenu.add_command(label="Roberts 수평 경계선",command=lambda :boundaryFreqencyImage(5))
boundaryMenu.add_command(label="Roberts 수직 경계선",command=lambda :boundaryFreqencyImage(6))
comVisionMenu4.add_command(label="가우시안 필터링",command=embossBlurGausSharpingImage(3))
comVisionMenu4.add_command(label="고주파",command=lambda :boundaryFreqencyImage(7))
comVisionMenu4.add_command(label="저주파",command=lambda :boundaryFreqencyImage(8))
comVisionMenu4.add_command(label="에지 검출",command=edgeImage)
comVisionMenu4.add_command(label="LoG 에지 검출",command=lambda :edgeLoGDoGImage(1))
comVisionMenu4.add_command(label="LoG 에지 검출",command=lambda :edgeLoGDoGImage(2))
comVisionMenu4.add_command(label="DoG 에지 검출",command=edgeDoGImage)
comVisionMenu4.add_command(label="다중 블러링",command=multiBlurringImage)


window.mainloop()