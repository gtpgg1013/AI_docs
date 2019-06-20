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
# 이었지만 결국은 numpy가 짱짱이다
import numpy as np
def malloc(h, w, initValue=0, dataType=np.uint8):  # uint8 : 범위가 0~255이어서 컬러 나타내기 딱
    # print("맬록은?")
    retMemory = np.zeros((h, w), dtype=dataType)
    retMemory += initValue  # 아 그냥 초깃값 설정 가능 ㅎㅎ
    return retMemory


# 파일을 메모리로 로딩하는 함수
def loadImage(fname):
    # print("로드이미지는?")
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global startTime
    startTime = time.time()
    fsize = os.path.getsize(fname)  # 파일의 크기(바이트)
    inH = inW = int(math.sqrt(fsize))  # 핵심 코드 : 파일의 메모리로부터 H,W 크기 구해냄

    # 입력영상 메모리 확보
    inImage = np.fromfile(fname, dtype=np.uint8)  # 이건 한쭐로 쫙 읽은거고
    inImage = inImage.reshape(inH, inW)

    # 파일에서 메모리로 가져오기
    # with open(fname, 'rb') as rFp:
    #     for i in range(inH):
    #         for k in range(inW):
    #             inImage[i][k] = int(ord(rFp.read(1)))  # 이렇게 하면 1바이트씩 읽어서 int, 정수로 바꿔줌
    #
    # # print(inH,outW)
    # print(ord(inImage[100][100])) # ord는 이진문자 - 읽을 수 있는 문자로!


# 파일 선택해서 메모리로 로딩하는 함수
import time
def openImage():
    # print("오픈이미지는?")
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    startTime = time.time()
    filename = askopenfilename(parent=window, filetypes=(("RAW파일", "*.raw"), ("모든 파일", "*.*")))
    if filename == '' or filename == None:
        return
    loadImage(filename)
    equalImage()


import struct
def saveImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    saveFp = asksaveasfile(parent=window, mode="wb", defaultextension='*.raw',
                           filetypes=(("RAW파일", "*.raw"), ("모든 파일", "*.*")))
    if saveFp == '' or saveFp == None:
        return
    for i in range(outH):
        for k in range(outW):
            saveFp.write(struct.pack('B', outImage[i][k]))  # B는 바이너리
    saveFp.close()


def displayImage():
    # print("디스풀레이이미지")
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global VIEW_X, VIEW_Y
    if canvas != None:  # 예전에 실행된 적이 있다
        canvas.destroy()

    ## 고정된 화면 크기
    if outH <= VIEW_Y or outW <= VIEW_X:
        VIEW_X = outW
        VIEW_Y = outH
        step = 1
    else:
        VIEW_X = 512
        VIEW_Y = 512
        step = outW / VIEW_X

    window.geometry(str(int(VIEW_Y * 1.2)) + 'x' + str(int(VIEW_X * 1.2)))  # 벽
    canvas = Canvas(window, height=VIEW_Y, width=VIEW_X)
    paper = PhotoImage(height=VIEW_Y, width=VIEW_X)
    canvas.create_image((VIEW_Y // 2, VIEW_X // 2), image=paper, state='normal')

    # 화면 크기 조절
    # window.geometry(str(outH) + 'x' + str(outW))  # 벽
    # canvas = Canvas(window, height=outH, width=outW)  # 보드
    # paper = PhotoImage(height=outH, width=outW)  # 빈 종이
    # canvas.create_image((outH // 2, outW // 2), image=paper, state='normal')

    # 출력 영상을 화면에 한점씩 찍기
    # # 요게 느려서 화면이 늦게 뜸
    # for i in range(outH):
    #     for k in range(outW):
    #         r = g = b = outImage[i][k]
    #         paper.put("#%02x%02x%02x" % (r,g,b), (k,i)) # 16진수 문자열 포맷팅, i,k로 위치 지정해주기
    ## 성능 개선
    # string 통째로 넣어서 받으면 더 빠르다
    # rgbStr = ''  # 전체 픽셀의 문자열을 저장
    # for i in range(outH):
    #     tmpStr = ''
    #     for k in range(outW):
    #         r = g = b = outImage[i][k]
    #         tmpStr += ' #%02x%02x%02x' % (r, g, b)  # 문자열 구분하려면 한칸 떼줘야 함
    #     rgbStr += '{' + tmpStr + '} '  # 문자열 구분하려면 한칸 떼줘야 함
    # paper.put(rgbStr)  # 성능 개선을 위해
    #
    # # 캔버스에 바인드 걸자
    # canvas.bind('<Button-1>', mouseClick)
    # canvas.bind('<ButtonRelease-1>', mouseDrop)
    # canvas.pack(expand=1, anchor=CENTER)
    # numpy로 더욱 성능개선!
    import numpy
    rgbStr = ''  # 전체 픽셀의 문자열을 저장
    for i in numpy.arange(0, outH, step):
        tmpStr = ''
        for k in numpy.arange(0, outW, step):
            i = int(i);
            k = int(k)
            r = g = b = outImage[i][k]
            tmpStr += ' #%02x%02x%02x' % (r, g, b)  # 문자열 구분하려면 한칸 떼줘야 함
        rgbStr += '{' + tmpStr + '} '  # 문자열 구분하려면 한칸 떼줘야 함
    paper.put(rgbStr)  # 성능 개선을 위해

    # 캔버스에 바인드 걸자
    canvas.bind('<Button-1>', mouseClick)
    canvas.bind('<ButtonRelease-1>', mouseDrop)
    canvas.pack(expand=1, anchor=CENTER)
    endTime = time.time() - startTime
    status.configure(text='이미지 정보' + str(outW) + 'x' + str(outH) + "\t 시간(초)" + "{0:.2f}".format(endTime))


########################################################
#####   컴퓨터비전(영상처리) 알고리즘 함수 모음   ######
########################################################

# 동일영상 알고리즘
def equalImage():
    # print("이콜이미지?")
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global startTime
    startTime = time.time()
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH; outW = inW

    # 이젠 메모리 할당을 할 필요가 없다
    # 진짜 컴퓨터 비전 알고리즘
    outImage = inImage[:]
    displayImage()


# 밝게/어둡게 하기 알고리즘
def plusminusImage(event):
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global startTime
    startTime = time.time()
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH; outW = inW
    start = time.time()
    # 진짜 컴퓨터 비전 알고리즘
    if event == 1:
        value = askinteger("밝게하기", "밝게할 값", minvalue=1, maxvalue=255)
        inImage = inImage.astype(np.int16)  # 2차원 배열 값이 255를 초과할 수도 있으므로 미리 방지
        outImage = inImage + value
        outImage = np.where(outImage > 255, 255, outImage)  # np.where(조건식, true, false)
        # outImage = np.where(outImage < 0, 0, outImage)
        # for i in range(inH):
        #     for k in range(inW):
        #         outImage[i][k] = inImage[i][k] + value
        #         if outImage[i][k] > 255:
        #             outImage[i][k] = 255
    else:
        value = askinteger("어둡게하기", "어둡게할 값", minvalue=1, maxvalue=255)
        inImage = inImage.astype(np.int16)  # 2차원 배열 값이 255를 초과할 수도 있으므로 미리 방지
        outImage = inImage - value
        # outImage = np.where(outImage > 255, 255, outImage) # np.where(조건식, true, false)
        outImage = np.where(outImage < 0, 0, outImage)
        # for i in range(inH):
        #     for k in range(inW):
        #         outImage[i][k] = inImage[i][k] - value
        #         if outImage[i][k] < 0:
        #             outImage[i][k] = 0

    # 시간측정
    # seconds = time.time() - start
    # status.configure는 displayImage 다음에 와야 함
    # status.configure(text=status.cget("text") + "\t\t 시간(초)" + "{0:.2f}".format(seconds))
    displayImage()


# 곱셈나눗셈 알고리즘
def mulDivImage(event):
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global startTime
    startTime = time.time()
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    # 진짜 컴퓨터 비전 알고리즘
    if event == 1:
        value = askinteger("곱하기", "곱할 값", minvalue=1, maxvalue=255)
        outImage = inImage * value
        outImage = np.where(outImage > 255, 255, outImage)
        # outImage = np.where(outImage < 0, 0, outImage)
    else:
        value = askinteger("나누기", "나눌 값", minvalue=1, maxvalue=255)
        outImage = inImage // value
        outImage = np.where(outImage > 255, 255, outImage)
        # outImage = np.where(outImage < 0, 0, outImage)
    displayImage()


# 화소값 반전 알고리즘
def reverseImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global startTime
    startTime = time.time()
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    # 진짜 컴퓨터 비전 알고리즘
    outImage = 255 - inImage

    displayImage()


# 이진화 알고리즘
def biImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global startTime
    startTime = time.time()
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    # 진짜 컴퓨터 비전 알고리즘
    outImage = np.where(inImage>127, 255, 0)

    displayImage()


# 축소(통계) 알고리즘
def shrinkStatImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global startTime
    startTime = time.time()
    ## 중요코드 : 출력영상 크기 결정 ##
    value = askinteger("안내", "축소 배율을 입력해주세요")
    outH = inH // value
    outW = inW // value
    # 메모리 할당 (틀만들기)
    # np 배열로 작아진 배열 먼저 만들고
    # 진짜 컴퓨터 비전 알고리즘

    # outImage = malloc(outH, outW, dataType=np.int16)
    # for i in range(outH):
    #     for k in range(outW):
    #         startX = i;
    #         startY = k
    #         endX = i * value;
    #         endY = k * value
    #
    #         # try:
    #         outImage[i][k] = int(inImage[startY:endY][startX:endX].mean())
    #         print(outImage[i][k])
    #         # except:
    #         #     pass
    # print(inImage)

    # outImage = malloc(outH, outW, dataType=np.int16)
    # for i in range(inW):
    #     for k in range(inH):
    #         try:
    #             outImage[i//value][k//value] += inImage[i][k]
    #         except:
    #             pass

    # outImage //= (value * value)

    # 더 쉽게 할 수 있는 방법도 있다? : inH / inW 만큼 포문돌려서 전부 더해주고 마지막에 나눠줌
    # for i in range(inH):
    #     for k in range(inW):
    #         outImage[i//value][k//value] += inImage[i][k]
    #
    # for i in range(outH):
    #     for k in range(outW):
    #         outImage[i][k] //= (value * value)

    displayImage()


# 영상 확대 알고리즘(양선형 보간)
def zoomImage2():  # 빈 부분은 어떻게 할지 결정해야 할 것임
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global startTime
    startTime = time.time()
    value = askinteger("안내", "확대 배율을 입력해주세요")
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH * value
    outW = inW * value
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘
    rH, rW, iH, iW = [0] * 4  # 실수 위치 및 정수 위치
    x, y = 0, 0  # 실수와 정수의 차이값
    C1, C2, C3, C4 = [0] * 4  # 결정할 위치(N)의 상하좌우 픽셀
    for i in range(outH):
        for k in range(outW):
            rH = i / value;
            rW = k / value
            iH = int(rH);
            iW = int(rW)
            x = rW - iW;
            y = rH - iH
            if 0 <= iH < inH - 1 and 0 <= iW < inW - 1:
                C1 = inImage[iH][iW]
                C2 = inImage[iH][iW + 1]
                C3 = inImage[iH + 1][iW]
                C4 = inImage[iH + 1][iW + 1]
                newValue = C1 * (1 - y) * (1 - x) + C2 * (1 - y) * x + C3 * y * x + C4 * y * (1 - x)
                outImage[i][k] = int(newValue)

    displayImage()


# 히스토그램
# 영상의 분포를 확인하는게 더 중요함! : 실제로 더 중요함
# 히스토그램의 부정확함을 보고 영상 처리에 문제가 있을 수 있음을 확인할 수 있다 : 무슨 값이 누락됬다던가
# 변화 후의 히스토그램과 비교해보는게 좋지!
import matplotlib.pyplot as plt
def histoImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global startTime
    startTime = time.time()
    incountlist = np.bincount(inImage.flatten())
    outcountlist = np.bincount(outImage.flatten())

    # for i in range(inH):
    #     for k in range(inW):
    #         incountlist[inImage[i][k]] += 1

    # for i in range(outH):
    #     for k in range(outW):
    #         outcountlist[outImage[i][k]] += 1

    # status.configure(text='이미지 정보' + str(outW) + 'x' + str(outH) + "\t 시간(초)" + "{0:.2f}".format(endTime))
    # 좀만 있다가 해보자
    fig = plt.figure()
    hist1 = fig.add_subplot(3, 1, 1)
    hist2 = fig.add_subplot(3, 1, 2)
    hist3 = fig.add_subplot(3, 1, 3)
    hist1.plot(incountlist)
    hist2.plot(outcountlist)
    hist3.plot(incountlist)
    hist3.plot(outcountlist)
    plt.show()


# 평균 표시 대화상자
def showAverage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global startTime
    startTime = time.time()
    inAvg = inImage.sum() / (inH*inW)
    outAvg = outImage.sum() / (outH*outW)

    status.configure(text='이미지 정보' + str(outW) + 'x' + str(outH) + "\t 시간(초)" + "{0:.2f}".format(endTime))
    messagebox.showinfo("입/출력 영상의 평균값", "입력 영상의 평균값 : {}, 출력 영상의 평균값: {}".format(inAvg, outAvg))


# 포스터라이징 알고리즘 : 경계값으로 뭉치게 하기
def posterizingImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global startTime
    startTime = time.time()
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
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
    global startTime
    startTime = time.time()
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘

    gamma = askfloat("안내", "감마값을 입력해 주세요")
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = int(math.pow(inImage[i][k], 1 / gamma))

    displayImage()


# 명암 대비 스트레칭
# 2배 빨라짐
def strectchImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global startTime
    startTime = time.time()
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    # 진짜 컴퓨터 비전 알고리즘
    maxpixel = inImage.max()
    minpixel = inImage.min()
    print(maxpixel, " ", minpixel)
    print(inImage)

    outImage = ((inImage - minpixel) / (maxpixel - minpixel)) * 255
    print(outImage)
    outImage = outImage.astype(np.uint8)

    displayImage()


# End-In 알고리즘 # 양쪽 날리고픈 부분 날리기
def endInImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global startTime
    startTime = time.time()
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    # 진짜 컴퓨터 비전 알고리즘

    # 원래 -1, 256 해도 되나, 보통 이런식으로 많이씀(버그 x)
    maxpixel = float(inImage.max())
    minpixel = float(inImage.min())

    print(inImage)

    minAdd = askinteger("최소", "최소추가", minvalue=0, maxvalue=255)
    maxAdd = askinteger("최대", "최대추가", minvalue=0, maxvalue=255)

    minpixel += minAdd
    maxpixel -= maxAdd

    outImage = ((inImage - minpixel) / (maxpixel - minpixel)) * 255 # 255보다 커질 수 있네
    print(outImage)
    outImage = np.where(outImage > maxpixel, 255,
                        np.where(outImage < minpixel, 0, outImage))
    outImage = outImage.astype(np.uint8)
    print(outImage.max())


    displayImage()


# 히스토그램 평활화 알고리즘
def histFlatImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global startTime
    startTime = time.time()
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘

    histlist = [0 for _ in range(0, 256)]
    sumlist = []
    normlist = []

    # 각 색깔(0~255) 별 빈도 리스트 만들기
    for i in range(inH):  # 값을 넣는 것이 아니라 빈도수를 넣는 것임
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
        norm = int((sum / (inH * inW)) * 255)
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
#
def parabolaImage(param):
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global startTime
    startTime = time.time()
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘
    # LookUpTable 기법 활용

    LUT = np.array([i for i in range(256)]) # 색깔 LUT 만들기 : LUT[]에 인덱스로 걍 때려넣으면 되네....?
    if param == 1:
        LUT = 255 - 255 * np.power((LUT / 128) - 1, 2)
        outImage = LUT[inImage]
    else:
        LUT = 255 * np.power((LUT / 128) - 1, 2)
        outImage = LUT[inImage]
    print(LUT)
    outImage = np.where(outImage > 255, 255,
                        np.where(outImage < 0, 0, outImage))
    outImage = outImage.astype(dtype=np.uint8)
    print(outImage)

    displayImage()


# 모핑 함수
def morphImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global startTime
    startTime = time.time()
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    # 추가 영상 선택
    filename2 = askopenfilename(parent=window, \
                                filetypes=(("RAW 파일", "*.raw"), ("모든 파일", "*.*")))
    if filename2 == '' or filename2 == None:
        return

    fsize = os.path.getsize(filename2)  # 파일의 크기(바이트)
    inH2 = inW2 = int(math.sqrt(fsize))  # 핵심코드 : 겹칠 사진 크기구하기
    # 입력 영상 메모리 확보
    inImage2 = []
    inImage2 = malloc(inH2, inW2)
    # 파일 -> 메모리
    with open(filename2, 'rb') as rFp:
        for i in range(inH2):
            for k in range(inW2):
                inImage2[i][k] = int(ord(rFp.read(1)))  # 1바이트씩 읽기

    # 메모리 할당
    outImage = [];
    outImage = malloc(outH, outW)

    # 진짜 컴퓨터 알고리즘
    # w1 = askinteger("원영상 가중치", "가중치(%)->", minvalue=0, maxvalue=100)
    # w2 = 1 - (w1/100); w1 = 1 - w2

    import threading
    import time
    def morpFunc():
        w1 = 1;
        w2 = 0
        for _ in range(20):
            for i in range(inH):
                for k in range(inW):
                    newValue = int(inImage[i][k] * w1 + inImage2[i][k] * w2)
                    if newValue > 255:
                        newValue = 255
                    elif newValue < 0:
                        newValue = 0
                    outImage[i][k] = newValue
            displayImage()
            w1 -= 0.05;
            w2 += 0.05
            time.sleep(0.5)

    threading.Thread(target=morpFunc).start()


# 동일영상 알고리즘
def updownImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global startTime
    startTime = time.time()
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘
    outImage = inImage[::-1,:] # 콜론 법칙 : 시작(:) 끝(:) 스텝(-1)
    # outImage = np.filp(inImage,axis=0)

    displayImage()


# 화면이동 알고리즘
def moveImage(param):
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global startTime
    startTime = time.time()
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘
    value = askinteger("안내", "이동할 값을 입력해 주세요")
    if param == 1:  # 아래로
        for i in range(inH):
            for k in range(inW):
                # print(i," ",k)
                if i + value < outW:
                    # print(i," ",k)
                    outImage[i + value][k] = inImage[i][k]
    elif param == 2:  # 위로
        for i in range(inH):
            for k in range(inW):
                if i - value >= 0:
                    outImage[i - value][k] = inImage[i][k]
    elif param == 3:  # 오른쪽으로
        for i in range(inH):
            for k in range(inW):
                if k + value < outH:
                    outImage[i][k + value] = inImage[i][k]
    else:  # 왼쪽으로
        for i in range(inH):
            for k in range(inW):
                if k - value >= 0:
                    outImage[i][k - value] = inImage[i][k]

    displayImage()


# 마우스 클릭 / 드랍으로
def moveClickImage():
    global panYN
    panYN = True
    canvas.configure(cursor='mouse')


def mouseClick(event):
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global sx, sy, ex, ey, panYN
    if panYN == False:
        return
    sx = event.x;
    sy = event.y


def mouseDrop(event):
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global sx, sy, ex, ey, panYN
    global startTime
    startTime = time.time()
    if panYN == False:
        return
    ex = event.x;
    ey = event.y
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘
    # x, y 이동량 구하기
    mx = sx - ex; my = sy - ey
    if mx < 0 and my < 0:
        outImage[-mx:inH, -my:inW] = inImage[0:inH+mx,0:inW+my]
    elif mx >= 0 and my >= 0:
        pass
    panYN = False

    displayImage()


# 회전변환 알고리즘
def rotateImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global startTime
    startTime = time.time()
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH
    outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘
    value = math.radians(askinteger("안내", "회전할 각도를 입력해 주세요"))
    centerh = inH // 2
    centerw = inW // 2
    centerw = inW // 2
    for i in range(inH):
        for k in range(inW):
            ys = i;
            xs = k
            xd = int((xs - centerw) * math.cos(value) - (ys - centerh) * math.sin(value)) + centerw
            yd = int((xs - centerw) * math.sin(value) + (ys - centerh) * math.cos(value)) + centerh
            # print(k,"/", i,"포워딩: ", xd," / ", yd)
            if yd >= 0 and yd < outH and xd >= 0 and xd < outW:
                outImage[yd][xd] = inImage[i][k]

    displayImage()


# 영상 회전 알고리즘 - 중심, 역방향
def rotateImage2():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global startTime
    startTime = time.time()
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;
    outW = inW;
    ###### 메모리 할당 ################
    outImage = [];
    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    value = math.radians(askinteger("안내", "회전할 각도를 입력해 주세요"))
    centerh = inH // 2
    centerw = inW // 2
    centerw = inW // 2
    for i in range(outH):
        for k in range(outW):
            ys = i;
            xs = k
            xd = int((xs - centerw) * math.cos(value) - (ys - centerh) * math.sin(value)) + centerw
            yd = int((xs - centerw) * math.sin(value) + (ys - centerh) * math.cos(value)) + centerh
            # print(k,"/", i, "백워딩: ",xd," / ", yd)
            if yd >= 0 and yd < outH and xd >= 0 and xd < outW:
                outImage[ys][xs] = inImage[yd][xd]
            else:
                outImage[ys][xs] = 255

    # start를 out에 넣어주는게 역방향인건가...?
    # 역방향으로 해주면 "어찌되었건" 화면에 0이 아닌 다른 색깔의 픽셀이 들어감
    # 중복된 곳에서 들어가는 곳이 있긴 하지만(데이터 손실) : 어찌되었건 눈으로 보기엔 손실이 없어보임
    # radian = angle * math.pi / 180
    # cx = inW//2; cy = inH//2
    # for i in range(outH) :
    #     for k in range(outW) :
    #         xs = i ; ys = k;
    #         xd = int(math.cos(radian) * (xs-cx) - math.sin(radian) * (ys-cy)) + cx
    #         yd = int(math.sin(radian) * (xs-cx) + math.cos(radian) * (ys-cy)) + cy
    #         if 0<= xd < outH and 0 <= yd < outW :
    #             outImage[xs][ys] = inImage[xd][yd]
    #         else :
    #             outImage[xs][ys] = 255

    displayImage()


# 회전 + 확대 알고리즘
def rotateZoomImage1():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global startTime
    startTime = time.time()
    ## 중요코드 : 출력영상 크기 결정 ##
    rotvalue = math.radians(askinteger("안내", "회전할 각도를 입력해 주세요"))
    zoomvalue = askinteger("안내", "확대할 값을 입력해주세요")
    outH = inH * zoomvalue
    outW = inW * zoomvalue
    # 메모리 할당 (틀만들기)
    tmpInImage = malloc(inH, inW)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘
    centerh = inH // 2
    centerw = inW // 2
    centerw = inW // 2

    # 회전
    for i in range(inH):
        for k in range(inW):
            ys = i;
            xs = k
            xd = int((xs - centerw) * math.cos(rotvalue) - (ys - centerh) * math.sin(rotvalue)) + centerw
            yd = int((xs - centerw) * math.sin(rotvalue) + (ys - centerh) * math.cos(rotvalue)) + centerh
            if yd >= 0 and yd < inH and xd >= 0 and xd < inW:
                tmpInImage[ys][xs] = inImage[yd][ys]
            else:
                tmpInImage[ys][xs] = 255

    # 확대
    for i in range(outH):
        for k in range(outW):
            outImage[i][k] = tmpInImage[i // zoomvalue][k // zoomvalue]

    displayImage()


# 회전 + 확대 (양선형 보간) 알고리즘
def rotateZoomImage2():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global startTime
    startTime = time.time()
    ## 중요코드 : 출력영상 크기 결정 ##
    rotvalue = math.radians(askinteger("안내", "회전할 각도를 입력해 주세요"))
    zoomvalue = askinteger("안내", "확대할 값을 입력해주세요")
    outH = inH * zoomvalue
    outW = inW * zoomvalue
    # 메모리 할당 (틀만들기)
    tmpInImage = malloc(inH, inW)  # 중간 징검다리
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘
    centerh = inH // 2
    centerw = inW // 2

    # 회전
    for i in range(inH):
        for k in range(inW):
            ys = i;
            xs = k
            xd = int((xs - centerw) * math.cos(rotvalue) - (ys - centerh) * math.sin(rotvalue)) + centerw
            yd = int((xs - centerw) * math.sin(rotvalue) + (ys - centerh) * math.cos(rotvalue)) + centerh
            if yd >= 0 and yd < inH and xd >= 0 and xd < inW:
                tmpInImage[ys][xs] = inImage[yd][xd]
            else:
                tmpInImage[ys][xs] = 255

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
    global startTime
    startTime = time.time()
    ## 중요코드 : 출력영상 크기 결정 ##
    value = askinteger("안내", "축소 배율을 입력해주세요")
    outH = inH // value
    outW = inW // value
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘

    outImage = inImage[::value,::value] # 시작 / 끝 / 스텝 : 잘 활용하면 슬라이싱 하기 진짜 편하다!

    displayImage()


def zoomImage():  # 빈 부분은 어떻게 할지 결정해야 할 것임
    # print("줌은? 거시기가 왜켜져?")
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global startTime
    startTime = time.time()
    value = askinteger("안내", "확대 배율을 입력해주세요")
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH * value
    outW = inW * value
    # 메모리 할당 (틀만들기)

    outImage = np.kron(inImage, np.ones((value,value),dtype=np.uint8)) # 크론: 행렬 각 내부 요소들을 곱해줌 (확장)
    # ex : 1x3 , 1x3을 kron해주면 1x9가 나옴
    print(outImage)
    outImage = outImage.astype(np.uint8)
    outImage = np.where(outImage>255,255,
                        np.where(outImage<0,0,outImage))

    # 더 쉽게할 수 있다... # 백워딩!
    # for i in range(outH):
    #     for k in range(outW):
    #         outImage[i][k] = inImage[i//value][k//value]

    # 프린트 20page 양선형보간법

    displayImage()


# 엠보싱 & 블러링 & 가우시안 필터링 & 샤프닝 효과 이미지
def embossBlurGausSharpingImage(param):
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global startTime
    startTime = time.time()
    # print("가우시안 거시기가 왜켜져?")
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH
    outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘

    MSIZE = 3
    if param == 1:  # 엠보싱
        mask = [[-1, 0, 0],
                [0, 0, 0],
                [0, 0, 1]]
    elif param == 2:  # 블러링
        mask = [[1 / 9, 1 / 9, 1 / 9],
                [1 / 9, 1 / 9, 1 / 9],
                [1 / 9, 1 / 9, 1 / 9]]
    elif param == 3:  # 가우시안 필터링
        mask = [[1 / 16, 1 / 8, 1 / 16],
                [1 / 8, 1 / 4, 1 / 8],
                [1 / 16, 1 / 8, 1 / 16]]
    elif param == 4:  # 샤프닝1
        mask = [[-1, -1, -1],
                [-1, 9, -1],
                [-1, -1, -1]]
    else:  # 샤프닝2
        mask = [[0, -1, 0],
                [-1, 5, -1],
                [0, -1, 0]]

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

    # # 127 더하기 : 좀더 밝게해주면 잘 보임
    # for i in range(outH):
    #     for k in range(outW):
    #         tmpOutImage[i][k] += 127

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
    global startTime
    startTime = time.time()
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH
    outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘

    if param == 1:  # prewitt 수평경계선
        MSIZE = 3
        mask = [[-1, -1, -1],
                [0, 0, 0],
                [1, 1, 1]]
    elif param == 2:  # prewitt 수직경계선
        MSIZE = 3
        mask = [[1, 0, -1],
                [1, 0, -1],
                [1, 0, -1]]
    elif param == 3:  # Sobel 수평경계선
        MSIZE = 3
        mask = [[-1, -2, -1],
                [0, 0, 0],
                [1, 2, 1]]
    elif param == 4:  # Sobel 수직경계선
        MSIZE = 3
        mask = [[1, 0, -1],
                [2, 0, -2],
                [1, 0, -1]]
    elif param == 5:  # Roberts 수직경계선
        MSIZE = 2
        mask = [[0, -1],
                [1, 0]]
    elif param == 6:  # Roberts 수평경계선
        MSIZE = 2
        mask = [[-1, 0],
                [0, 1]]
    elif param == 7:  # High Frequency
        MSIZE = 3
        mask = [[-1 / 9, -1 / 9, -1 / 9],
                [-1 / 9, 8 / 9, -1 / 9],
                [-1 / 9, -1 / 9, -1 / 9]]
    elif param == 8:  # Low Frequency
        MSIZE = 3
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


def edgeImage():
    pass


def edgeLoGDoGImage(param):
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global startTime
    startTime = time.time()
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
    global startTime
    startTime = time.time()
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH
    outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘

    MSIZE = askinteger("안내", "블러링 마스크의 크기를 입력하세요 : 3,5,7,9...")
    mask = [[1 / (MSIZE * MSIZE) for _ in range(MSIZE)] for _ in range(MSIZE)]

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


## 임시 경로에 outImage를 저장하기
import random
def saveTempImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global startTime
    startTime = time.time()
    import tempfile
    saveFp = tempfile.gettempdir() + "/" + str(random.randint(10000, 99999)) + ".raw"
    if saveFp == "" or saveFp == None:
        return
    print(saveFp)
    saveFp = open(saveFp, mode='wb')
    for i in range(outH):
        for k in range(outW):
            saveFp.write(struct.pack('B', outImage[i][k]))
    saveFp.close()
    return saveFp


# 포문돌려서 min max avg 찾기
def findStat(fname):
    # 파일 열고, 읽기.
    fsize = os.path.getsize(fname)  # 파일의 크기(바이트)
    inH = inW = int(math.sqrt(fsize))  # 핵심 코드
    ## 입력영상 메모리 확보 ##
    inImage = []
    inImage = malloc(inH, inW)
    # 파일 --> 메모리
    with open(fname, 'rb') as rFp:
        for i in range(inH):
            for k in range(inW):
                inImage[i][k] = int(ord(rFp.read(1)))
    sum = 0
    for i in range(inH):
        for k in range(inW):
            sum += inImage[i][k]
    avg = sum // (inW * inH)
    maxVal = minVal = inImage[0][0]
    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] < minVal:
                minVal = inImage[i][k]
            elif inImage[i][k] > maxVal:
                maxVal = inImage[i][k]
    return avg, maxVal, minVal


import pymysql
# DB 관련 configration
IP_ADDR = '192.168.56.101';
USER_NAME = 'root';
USER_PASS = '1234'
DB_NAME = 'BigData_DB';
CHAR_SET = 'utf8'


# Mysql에 저장하는 함수
def saveMysql():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global startTime
    startTime = time.time()
    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS,
                          db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()
    # 테이블 생성 : try / catch로 해놔서 만약 테이블 존재하면 그냥 무시
    try:
        sql = '''
                CREATE TABLE rawImage_TBL (
                raw_id INT AUTO_INCREMENT PRIMARY KEY,
                raw_fname VARCHAR(30),
                raw_extname CHAR(5),
                raw_height SMALLINT, raw_width SMALLINT,
                raw_avg  TINYINT UNSIGNED , 
                raw_max  TINYINT UNSIGNED,  raw_min  TINYINT UNSIGNED,
                raw_data LONGBLOB);
            '''
        cur.execute(sql)
    except:
        pass

    # outImage를 임시 폴더에 저장하고, 이걸 fullname으로 전달
    fullname = saveTempImage()
    fullname = fullname.name
    with open(fullname, 'rb') as rfp:
        binData = rfp.read()

    fname, extname = os.path.basename(fullname).split(".")
    fsize = os.path.getsize(fullname)
    height = width = int(math.sqrt(fsize))
    avgVal, maxVal, minValue = findStat(fullname)  # 평균,최대,최소
    sql = "INSERT INTO rawImage_TBL(raw_id , raw_fname,raw_extname,"
    sql += "raw_height,raw_width,raw_avg,raw_max,raw_min,raw_data) "
    sql += " VALUES(NULL,'" + fname + "','" + extname + "',"
    sql += str(height) + "," + str(width) + ","
    sql += str(avgVal) + "," + str(maxVal) + "," + str(minValue)
    sql += ", %s )"  # 괄호 넣어줄려고 이렇게 한거구나!
    tupleData = (binData,)  # 인자를 tuple로 이렇게 넘겨주는게 양식
    cur.execute(sql, tupleData)
    con.commit()
    cur.close()
    con.close()
    os.remove(fullname)
    print("upload complete: " + fullname)


def loadMysql():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global startTime
    startTime = time.time()
    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS,
                          db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()
    sql = "SELECT raw_id, raw_fname, raw_extname, raw_height, raw_width "
    sql += "FROM rawImage_TBL"
    cur.execute(sql)

    queryList = cur.fetchall()
    rowList = [":".join(map(str, row)) for row in queryList]  # 각 속성들을 :로 조인해서 하나의 문자열로 만듬
    import tempfile
    def selectRecord():
        global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
        selIndex = listbox.curselection()[0]  # 선택된 항목을 튜플로 반환: 그거의 첫번째 : 숫자(id)
        subWindow.destroy()
        raw_id = queryList[selIndex][0]
        sql = "SELECT raw_fname, raw_extname, raw_data FROM rawImage_TBL "
        sql += "WHERE raw_id = " + str(raw_id)
        cur.execute(sql)
        fname, extname, binData = cur.fetchone()

        fullPath = tempfile.gettempdir() + '/' + fname + "." + extname # 임시파일공간을 만들어서
        with open(fullPath, "wb") as wfp:
            wfp.write(binData)
        cur.close()
        con.close()

        loadImage(fullPath) # 거기에서 로드
        equalImage()

    # 서브 윈도우에 목록 출력하기
    subWindow = Toplevel(window)
    listbox = Listbox(subWindow)
    button = Button(subWindow, text="select", command=selectRecord)

    for rowStr in rowList:
        listbox.insert(END, rowStr)  # END(끝)에 rowStr 추가

    listbox.pack(expand=1, anchor=CENTER)
    button.pack()
    subWindow.mainloop()

    cur.close()
    con.close()


# CSV 파일을 메모리로 로딩하는 함수
def loadCSV(fname):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global startTime
    startTime = time.time()
    fsize = 0  # 헤더 없는 파일 기준
    fp = open(fname, 'r')
    for _ in fp:
        fsize += 1  # 사이즈 알아내고
    inH = inW = int(math.sqrt(fsize))  # 핵심코드
    fp.close()

    # 입력영상 메모리 확보
    inImage = []
    inImage = malloc(inH, inW)

    # 파일 -> 메모리
    with open(fname, 'r') as rFp:
        for row_list in rFp:
            row, col, value = list(map(int, row_list.strip().split(',')))
            inImage[row][col] = value


def openCSV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global startTime
    startTime = time.time()
    filename = askopenfilename(parent=window,
                               filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))
    if filename == '' or filename == None:
        return
    loadCSV(filename)
    equalImage()


import csv
def saveCSV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global startTime
    startTime = time.time()
    # 일단 저장할 위치 설정
    saveFp = asksaveasfile(parent=window, mode='wb',
                           defaultextension='*.csv', filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))
    if saveFp == '' or saveFp == None:
        return
    # print(saveFp) # <> 형식
    # print(saveFp.name) # 전체경로
    with open(saveFp.name, 'w', newline='') as wFp:
        csvWriter = csv.writer(wFp)
        for i in range(outH):
            for k in range(outW):
                row_list = [i, k, outImage[i][k]]
                csvWriter.writerow(row_list)  # csv에 쓰는 형식을 튜플로 받음
    print('CSV. Save OK')

import xlrd
def loadExcel(fname):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global startTime
    startTime = time.time()
    wb = xlrd.open_workbook(fname)
    sheets = wb.sheets()

    nrows = sheets[0].nrows
    ncols = sheets[0].ncols

    inH = outH = nrows ; inW = outH = ncols
    fsize = inH * inW


    # 입력영상 메모리 확보
    inImage = []
    inImage = malloc(inH, inW)

    # 파일 -> 메모리
    for i in range(inH):
        for k in range(inW):
            inImage[i][k] = sheets[0].cell_value(i,k)

    outImage = inImage[:]

def openExcel():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global startTime
    startTime = time.time()
    filename = askopenfilename(parent=window,
                               filetypes=(("Excel 파일", "*.xls"), ("모든 파일", "*.*")))
    if filename == '' or filename == None:
        return
    loadExcel(filename)
    equalImage()

import xlwt
def saveExcel():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global startTime
    startTime = time.time()
    saveFp = asksaveasfile(parent=window, mode='wb',
        defaultextension='*.xls', filetypes=(("XLS 파일", "*.xls"), ("모든 파일", "*.*")))
    print(saveFp, type(saveFp))
    if saveFp == '' or saveFp == None :
        return
    xlsname = saveFp.name
    sheetName = os.path.basename(filename) # 시트네임 가져오기
    wb = xlwt.Workbook()
    ws = wb.add_sheet(sheetName)

    for i in range(outH):
        for k in range(outW):
            ws.write(i,k,int(outImage[i][k]))

    wb.save(xlsname)
    print('Excel. Save OK')


# ExcelArt 파일을 메모리로 로딩하는 함수
import xlrd
# 여기서부터 다시 시작
def loadExcelArt(fname):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global startTime
    startTime = time.time()
    # 일단 이미지 크기
    # fsize =
    pass

    # wb = xlrd.open_workbook(fname)
    # sheets = wb.sheets()
    # nsheets = wb.nsheets
    #
    # nrows = sheets[0].nrows
    # ncols = sheets[0].ncols
    #
    # for i in range(nrows):
    #     for k in range(ncols):
    #         xlrd.book.Book.colour_map


import xlsxwriter
def openExcelArt():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global startTime
    startTime = time.time()
    filename = askopenfilename(parent=window, filetypes=(("XLS 파일", "*.xls"), ("모든 파일", "*.*")))
    # print(saveFp, type(saveFp))
    if filename == '' or filename == None:
        return

    loadExcelArt(filename)
    equalImage()


import xlsxwriter


def saveExcelArt():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global startTime
    startTime = time.time()
    saveFp = asksaveasfile(parent=window, mode='wb',
                           defaultextension='*.xls', filetypes=(("XLS 파일", "*.xls"), ("모든 파일", "*.*")))
    print(saveFp, type(saveFp))
    if saveFp == '' or saveFp == None:
        return
    xlsname = saveFp.name.split(".")
    xlsname = xlsname[0] + str(inH) + "." + xlsname[1]
    sheetName = os.path.basename(filename)  # 시트네임 가져오기
    wb = xlsxwriter.Workbook(xlsname)  # 인자로 xls 이름 줘야함
    ws = wb.add_worksheet(sheetName)  # 인자로 sheetName 줘야함

    # 한 칸 가로세로 사이즈 변경
    ws.set_column(0, outW - 1, 1.0)  # 0번부터 outW-1번까지 1.0으로 : 약 0.34 : 폭 / 너비 단위가 달라서그럼
    for i in range(outH):  # row는 포문돌려야함
        ws.set_row(i, 9.5)  # 약 0.35

    for i in range(outH):
        for k in range(outW):
            data = outImage[i][k]
            # data 값으로 셀의 배경색을 조절 #000000 ~ #FFFFFF
            if data > 15:
                hexStr = '#' + hex(data)[2:] * 3  # 그냥 hex쓰면 앞에 0x 있는거 날리기
            else:
                hexStr = '#' + ('0' + hex(data)[2:]) * 3
            # 셀의 포맷을 준비
            cell_format = wb.add_format()
            cell_format.set_bg_color(hexStr)
            print(cell_format.bg_color)
            ws.write(i, k, '', cell_format)  # 3번째 인자가 값인데, 보기 드러우니까 걍 빈칸으루

    wb.close()
    print('Excel. Save OK')


################################
#####   전역변수 선언부   ######
################################

# inImage, outImage = [], [];
# inH, inW, outH, outW = [0] * 4
# window, canvas, paper = None, None, None
# filename = ""
# # 마우스 사용할꺼니 안할꺼니 확인하는 전역변수
# panYN = False
# # 마우스 좌표 저장할 변수
# sx, sy, ex, ey = [0] * 4
# VIEW_X, VIEW_Y = 512, 512  # 화면에 보일 크기
startTime = 0
endTime = 0

inImage, outImage = [], [] ; inH, inW, outH, outW = [0] * 4
window, canvas, paper = None, None, None
filename = ""
panYN = False
sx,sy,ex,ey = [0] * 4
VIEW_X, VIEW_Y = 512, 512 # 화면에 보일 크기 (출력용)
################################
#######   메인 코드부   ########
################################

window = Tk()
window.geometry("500x500")
window.title("컴퓨터 비전(딥러닝 기법) ver 0.1k")

status = Label(window, text='이미지 정보', bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)
# 마우스 이벤트

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu)
fileMenu.add_command(label="파일 열기", command=openImage)
fileMenu.add_command(label="파일 저장", command=saveImage)

comVisionMenu1 = Menu(mainMenu)
mainMenu.add_cascade(label="화소점처리", menu=comVisionMenu1)
comVisionMenu1.add_command(label="밝게하기", command=lambda: plusminusImage(1))
comVisionMenu1.add_command(label="어둡게하기", command=lambda: plusminusImage(2))
comVisionMenu1.add_command(label="영상 곱셈", command=lambda: mulDivImage(1))
comVisionMenu1.add_command(label="영상 나눗셈", command=lambda: mulDivImage(2))
comVisionMenu1.add_command(label="화소값 반전", command=reverseImage)
comVisionMenu1.add_command(label="입력/출력 영상의 평균값 구하기", command=showAverage)  # 출력은 메시지박스
comVisionMenu1.add_command(label="Posterizing", command=posterizingImage)
comVisionMenu1.add_command(label="Gamma 보정", command=gammaCorrectionImage)
comVisionMenu1.add_command(label="명암 대비 스트레칭", command=strectchImage)
comVisionMenu1.add_command(label="End-In 탐색", command=endInImage)
comVisionMenu1.add_command(label="히스토그램 평활화", command=histFlatImage)
comVisionMenu1.add_command(label="파라볼라 변환(캡)", command=lambda: parabolaImage(1))
comVisionMenu1.add_command(label="파라볼라 변환(컵)", command=lambda: parabolaImage(2))
comVisionMenu1.add_command(label="모핑", command=morphImage)

comVisionMenu2 = Menu(mainMenu)
mainMenu.add_cascade(label="화소(통계)", menu=comVisionMenu2)
comVisionMenu2.add_command(label="이진화", command=biImage)
comVisionMenu2.add_command(label="축소(평균)", command=shrinkStatImage)
comVisionMenu2.add_command(label="확대(양선형보간)", command=zoomImage2)
comVisionMenu2.add_separator()
comVisionMenu2.add_command(label="히스토그램", command=histoImage)

comVisionMenu3 = Menu(mainMenu)
mainMenu.add_cascade(label="기하학 처리", menu=comVisionMenu3)
comVisionMenu3.add_command(label="상하반전", command=updownImage)
moveMenu = Menu(comVisionMenu3)
comVisionMenu3.add_cascade(label="이동", menu=moveMenu)
moveMenu.add_command(label="아래로", command=lambda: moveImage(1))
moveMenu.add_command(label="위로", command=lambda: moveImage(2))
moveMenu.add_command(label="오른쪽", command=lambda: moveImage(3))
moveMenu.add_command(label="왼쪽", command=lambda: moveImage(4))
moveMenu.add_command(label="마우스로 이동", command=moveClickImage)
comVisionMenu3.add_command(label="회전", command=rotateImage)
comVisionMenu3.add_command(label="회전_역방향", command=rotateImage2)
comVisionMenu3.add_command(label="회전후 확대", command=rotateZoomImage1)
comVisionMenu3.add_command(label="회전후 확대(양선형 보간)", command=rotateZoomImage2)
comVisionMenu3.add_command(label="축소", command=shrinkImage)
comVisionMenu3.add_command(label="확대", command=zoomImage)

comVisionMenu4 = Menu(mainMenu)
mainMenu.add_cascade(label="화소 영역 처리", menu=comVisionMenu4)
comVisionMenu4.add_command(label="엠보싱처리", command=lambda: embossBlurGausSharpingImage(1))
comVisionMenu4.add_command(label="블러링", command=lambda: embossBlurGausSharpingImage(2))
sharpingMenu = Menu(comVisionMenu4)
comVisionMenu4.add_cascade(label="샤프닝", menu=sharpingMenu)
sharpingMenu.add_command(label="회선마스크1", command=lambda: embossBlurGausSharpingImage(4))
sharpingMenu.add_command(label="회선마스크2", command=lambda: embossBlurGausSharpingImage(5))
boundaryMenu = Menu(comVisionMenu4)
comVisionMenu4.add_cascade(label="경계선 검출", menu=boundaryMenu)
boundaryMenu.add_command(label="Prewitt 수평 경계선", command=lambda: boundaryFreqencyImage(1))
boundaryMenu.add_command(label="Prewitt 수직 경계선", command=lambda: boundaryFreqencyImage(2))
boundaryMenu.add_command(label="Sobel 수평 경계선", command=lambda: boundaryFreqencyImage(3))
boundaryMenu.add_command(label="Sobel 수직 경계선", command=lambda: boundaryFreqencyImage(4))
boundaryMenu.add_command(label="Roberts 수평 경계선", command=lambda: boundaryFreqencyImage(5))
boundaryMenu.add_command(label="Roberts 수직 경계선", command=lambda: boundaryFreqencyImage(6))
comVisionMenu4.add_command(label="가우시안 필터링", command=lambda: embossBlurGausSharpingImage(3))
# 이게 람다를 안주니까 ㅄ같이 되네 왜지?? command= embossBlurGausSharpingImage(3) 로 썼더니 버그가 생겼었음
comVisionMenu4.add_command(label="고주파", command=lambda: boundaryFreqencyImage(7))
comVisionMenu4.add_command(label="저주파", command=lambda: boundaryFreqencyImage(8))
comVisionMenu4.add_command(label="에지 검출", command=edgeImage)
comVisionMenu4.add_command(label="LoG 에지 검출", command=lambda: edgeLoGDoGImage(1))
comVisionMenu4.add_command(label="LoG 에지 검출", command=lambda: edgeLoGDoGImage(2))
comVisionMenu4.add_command(label="DoG 에지 검출", command=edgeDoGImage)
comVisionMenu4.add_command(label="다중 블러링", command=multiBlurringImage)

comVisionMenu5 = Menu(mainMenu)
mainMenu.add_cascade(label="데이터베이스 입출력", menu=comVisionMenu5)
comVisionMenu5.add_command(label="MySQL에서 불러오기", command=loadMysql)
comVisionMenu5.add_command(label="MySQL에 저장하기", command=saveMysql)
comVisionMenu5.add_separator()
comVisionMenu5.add_command(label="CSV 열기", command=openCSV)
comVisionMenu5.add_command(label="CSV로 저장", command=saveCSV)
comVisionMenu5.add_separator()
comVisionMenu5.add_command(label="Excel 열기", command=openExcel)
comVisionMenu5.add_command(label="Excel로 저장", command=saveExcel)
comVisionMenu5.add_separator()
comVisionMenu5.add_command(label="Excel art로 열기", command=openExcelArt)
comVisionMenu5.add_command(label="Excel art로 저장", command=saveExcelArt)

window.mainloop()