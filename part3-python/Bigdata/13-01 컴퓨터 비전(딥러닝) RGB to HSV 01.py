from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import numpy as np
import time


####################
#### 함수 선언부 ####
####################
def malloc(h, w, initValue=0) :
    retMemory= []
    for _ in range(h) :
        tmpList = []
        for _ in range(w) :
            tmpList.append(initValue)
        retMemory.append(tmpList)
    return retMemory


# 파일을 메모리로 로딩하는 함수
def loadImageColor(fname) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo
    inImage = []
    photo = Image.open(fname)
    # f = f.convert('RGB')
    # inImage = f.load() # f.load()를 쓰면 배열로 가져와줌
    inW, inH = photo.size
    ## 입력영상 메모리 확보 ##
    # 걍 malloc을 3번 호출하는게 나을 듯 : 2번호출할 때도 필요할 거 같음
    for _ in range(3):
        inImage.append(malloc(inH,inW))

    # 포토RGB PIL 파일에서 inImage로 읽어오기
    photoRGB = photo.convert('RGB')
    for i in range(inH):
        for k in range(inW):
            r,g,b = photoRGB.getpixel((k,i))
            inImage[R][i][k] = r
            inImage[G][i][k] = g
            inImage[B][i][k] = b


# 파일을 선택해서 메모리로 로딩하는 함수
def openImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    filename = askopenfilename(parent=window,
                               filetypes=(("칼라 파일", "*.jpg;*.png;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if filename == '' or filename == None:
        return

    loadImageColor(filename)
    equalImageColor()

    displayImageColor()

    # equalImage()


def displayImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global VIEW_X, VIEW_Y
    if canvas != None:  # 예전에 실행한 적이 있다.
        canvas.destroy()
    # 이건 걍 귀찮아서 안지운거

    ## 고정된 화면 크기
    if outH <= VIEW_Y or outW <= VIEW_X :
        VIEW_X = outW
        VIEW_Y = outH
        step = 1
    else :
        VIEW_X = 512
        VIEW_Y = 512
        step = outW / VIEW_X

    window.geometry(str(int(VIEW_X * 1.2)) + 'x' + str(int(VIEW_Y * 1.2)))  # 벽 # VIEX_X , Y는 왜 바꾼거신가
    canvas = Canvas(window, height=VIEW_Y, width=VIEW_X)
    paper = PhotoImage(height=VIEW_Y, width=VIEW_X)
    canvas.create_image((VIEW_X // 2, VIEW_Y // 2), image=paper, state='normal')

    ## 성능 개선
    import numpy
    # 영상이 만약 rgb이미지가 아닌경우 convert시켜주는 함수
    # rgbImage = outImage.convert('RGB')  # convert : 사진객체 다른 포맷으로 전환
    rgbStr = ''  # 전체 픽셀의 문자열을 저장
    for i in numpy.arange(0, outH, step):
        tmpStr = ''
        for k in numpy.arange(0, outW, step):
            i = int(i);
            k = int(k)
            r, g, b = outImage[R][i][k], outImage[G][i][k], outImage[B][i][k] # PIL 라이브러리 사용
            tmpStr += ' #%02x%02x%02x' % (r, g, b)
        rgbStr += '{' + tmpStr + '} '
    paper.put(rgbStr)

    canvas.bind('<Button-1>', mouseClick)
    canvas.bind('<ButtonRelease-1>', mouseDrop)
    canvas.pack(expand=1, anchor=CENTER)
    status.configure(text='이미지 정보:' + str(outW) + 'x' + str(outH))


def saveImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if outImage == None:
        return
    saveFp = asksaveasfile(parent=window, mode="wb", defaultextension='*.jpg',
                           filetypes=(("JPG파일", "*.jpg"), ("모든 파일", "*.*")))
    if saveFp == '' or saveFp == None:
        return
    outImage.save(saveFp.name)
    print('Save complete')
    saveFp.close()

# 동일영상 알고리즘
def  equalImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    # outImage = ImageEnhance._Enhance(inImage)
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH,outW))

    ### 진짜 컴퓨터 비전 영상처리 알고리즘 ###
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                outImage[RGB][i][k] = inImage[RGB][i][k]

    displayImageColor()

# 밝기조절
def addImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    value = askinteger("밝게/어둡게", "값-->", minvalue=-255, maxvalue=255)
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH,outW))

    ### 진짜 컴퓨터 비전 영상처리 알고리즘 ###
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                if inImage[RGB][i][k] + value > 255:
                    outImage[RGB][i][k] = 255
                elif outImage[RGB][i][k] + value < 0:
                    outImage[RGB][i][k] = 0
                else:
                    outImage[RGB][i][k] = inImage[RGB][i][k] + value


    displayImageColor()


# 반전영상 알고리즘
def revImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    ### 진짜 컴퓨터 비전 영상처리 알고리즘 ###
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                outImage[RGB][i][k] = 255 - inImage[RGB][i][k]

    displayImageColor()

# 흑백화 알고리즘
def  grayscaleImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    print(inImage)
    outImage = [];
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for i in range(inH) :
        for k in range(inW) :
            for RGB in range(3):
                outImage[RGB][i][k] = int(inImage[0][i][k] * 0.2126 + inImage[1][i][k] * 0.7152 * inImage[2][i][k] * 0.)

    displayImageColor()

# 이진화 알고리즘
def  bwImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    print(inImage)
    outImage = [];
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    grayscaleImage = [];
    for _ in range(3):
        grayscaleImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for i in range(inH) :
        for k in range(inW) :
            for RGB in range(3):
                grayscaleImage[RGB][i][k] = inImage[0][i][k] * 0.2126 + inImage[1][i][k] * 0.7152 * inImage[2][i][k] * 0.0722

    for i in range(inH) :
        for k in range(inW) :
            for RGB in range(3):
                if grayscaleImage[RGB][i][k] > 127 :
                    outImage[RGB][i][k] = 255
                else :
                    outImage[RGB][i][k] = 0

    displayImageColor()

# 이진화 알고리즘
def  eightImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    print(inImage)
    outImage = [];
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####

    ## 영상의 평균 구하기.
    sumRGB = [ 0 for _ in range(3) ]
    avgRGB = [ 0 for _ in range(3) ]

    for i in range(inH) :
        for k in range(inW) :
            for RGB in range(3):
                sumRGB[RGB] += inImage[RGB][i][k]
    for RGB in range(3):
        avgRGB[RGB] = sumRGB[RGB] // (inW * inH)

    for i in range(inH) :
        for k in range(inW) :
            for RGB in range(3):
                if inImage[RGB][i][k] > avgRGB[RGB] :
                    outImage[RGB][i][k] = 255
                else :
                    outImage[RGB][i][k] = 0

    displayImageColor()

# 영상 축소 알고리즘 (평균변환)
def  zoomOutImageColor2() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("축소", "값-->", minvalue=2, maxvalue=16)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH//scale;  outW = inW//scale;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for i in range(inH) :
        for k in range(inW) :
            for RGB in range(3):
                if i//scale < outH and k//scale < outW: # 만약 정사각형이 아니면 초과되는 친구들 날려줘야 함
                    outImage[RGB][i//scale][k//scale] += inImage[RGB][i][k]
    for i in range(outH):
        for k in range(outW):
            for RGB in range(3):
                outImage[RGB][i][k] //= (scale*scale)

    displayImageColor()


# 영상 확대 알고리즘 (양선형 보간)
def  zoomInImageColor2() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("확대", "값-->", minvalue=2, maxvalue=8)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH*scale;  outW = inW*scale;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    rH, rW, iH, iW = [0] * 4 # 실수위치 및 정수위치
    x, y = 0, 0 # 실수와 정수의 차이값
    C1,C2,C3,C4 = [0] * 4 # 결정할 위치(N)의 상하좌우 픽셀
    for i in range(outH) :
        for k in range(outW) :
            for RGB in range(3):
                rH = i / scale ; rW = k / scale
                iH = int(rH) ;  iW = int(rW)
                x = rW - iW; y = rH - iH
                if 0 <= iH < inH-1 and 0 <= iW < inW-1 :
                    C1 = inImage[RGB][iH][iW]
                    C2 = inImage[RGB][iH][iW+1]
                    C3 = inImage[RGB][iH+1][iW+1]
                    C4 = inImage[RGB][iH+1][iW]
                    newValue = C1*(1-y)*(1-x) + C2*(1-y)* x+ C3*y*x + C4*y*(1-x)
                    outImage[RGB][i][k] = int(newValue)

    displayImageColor()

import matplotlib.pyplot as plt
# 현재 흑백사진은 안됨 => 안되는 이유 파악해서 할 것
def histoImageColor():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW

    incountlist = [ [_ for _ in range(256) ] for _ in range(3)  ]
    outcountlist = [ [_ for _ in range(256) ] for _ in range(3) ]


    for i in range(inH):
        for k in range(inW):
            for RGB in range(3):
                incountlist[RGB][inImage[RGB][i][k]] += 1

    for i in range(outH):
        for k in range(outW):
            for RGB in range(3):
                outcountlist[RGB][outImage[RGB][i][k]] += 1

    # status.configure(text='이미지 정보' + str(outW) + 'x' + str(outH) + "\t 시간(초)" + "{0:.2f}".format(endTime))
    # 좀만 있다가 해보자
    fig = plt.figure(figsize=(16,8))
    plt.title("In & Out RGB")
    hist1 = fig.add_subplot(2, 1, 1)
    hist2 = fig.add_subplot(2, 1, 2)
    hist1.plot(incountlist[R],label='inImage Red',color='Red')
    hist1.plot(incountlist[G],label='inImage Green',color='Green')
    hist1.plot(incountlist[B],label='inImage Blue',color='Blue')
    hist2.plot(outcountlist[R],label='outImage Red',color='Red')
    hist2.plot(outcountlist[G],label='outImage Green',color='Green')
    hist2.plot(outcountlist[B],label='outImage Blue',color='Blue')
    fig.legend(loc='upper left')
    plt.show()


# 스트레칭 알고리즘
def  stretchImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    maxValList = [ 0 for _ in range(3) ]
    minValList = [ 0 for _ in range(3) ]
    for RGB in range(3):
        maxValList[RGB] = minValList[RGB] = inImage[RGB][0][0]
    for i in range(inH) :
        for k in range(inW) :
            for RGB in range(3):
                if inImage[RGB][i][k] < minValList[RGB] :
                    minValList[RGB] = inImage[RGB][i][k]
                elif inImage[RGB][i][k] > maxValList[RGB] :
                    maxValList[RGB] = inImage[RGB][i][k]
    for i in range(inH) :
        for k in range(inW) :
            for RGB in range(3):
                outImage[RGB][i][k] = int(((inImage[RGB][i][k] - minValList[RGB]) / (maxValList[RGB] - minValList[RGB])) * 255)

    displayImageColor()


# 스트레칭 알고리즘
def  endinImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    ####### 진짜 컴퓨터 비전 알고리즘 #####
    maxValList = [ 0 for _ in range(3) ]
    minValList = [ 0 for _ in range(3) ]

    for RGB in range(3):
        maxValList[RGB] = minValList[RGB] = inImage[RGB][0][0]

    for i in range(inH) :
        for k in range(inW) :
            for RGB in range(3):
                if inImage[RGB][i][k] < minValList[RGB] :
                    minValList[RGB] = inImage[RGB][i][k]
                elif inImage[RGB][i][k] > maxValList[RGB] :
                    maxValList[RGB] = inImage[RGB][i][k]

    minAdd = askinteger("최소", "최소에서추가-->", minvalue=0, maxvalue=255)
    maxAdd = askinteger("최대", "최대에서감소-->", minvalue=0, maxvalue=255)

    for RGB in range(3):
        minValList[RGB] += minAdd
        maxValList[RGB] -= maxAdd

    for i in range(inH) :
        for k in range(inW) :
            for RGB in range(3):
                value = int(((inImage[RGB][i][k] - minValList[RGB]) / (maxValList[RGB] - minValList[RGB])) * 255)
                if value < 0:
                    value = 0
                elif value > 255:
                    value = 255
                outImage[RGB][i][k] = value

    displayImageColor()

# 평활화 알고리즘
def  equalizeImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    histo = [[0] * 256 for _ in range(3)]; sumHisto = [[0] * 256 for _ in range(3)]; normalHisto = [[0] * 256 for _ in range(3)]
    ## 히스토그램
    for i in range(inH) :
        for k in range(inW) :
            for RGB in range(3):
                histo[RGB][inImage[RGB][i][k]] += 1
    ## 누적히스토그램
    sValueList = [0,0,0]
    for i in range(len(histo[0])) : # [0]을 안잡아주면 len이 3 이 되어서 3번밖에 안더함 --> 너무 값이 다 작아져서 전부 0되버리기!
        for RGB in range(3):
            sValueList[RGB] += histo[RGB][i]
            sumHisto[RGB][i] = sValueList[RGB]
    ## 정규화 누적 히스토그램
    for i in range(len(normalHisto[0])): # [0]을 안잡아주면 len이 3 이 되어서 3번밖에 안더함 --> 너무 값이 다 작아져서 전부 0되버리기!
        print(len(normalHisto))
        for RGB in range(3):
            normalHisto[RGB][i] = int(sumHisto[RGB][i] / (inW*inH) * 255)
    ## 영상처리
    for i in range(inH) :
        for k in range(inW) :
            for RGB in range(3):
                outImage[RGB][i][k] = normalHisto[RGB][inImage[RGB][i][k]]
    # print(outImage)
    displayImageColor()

# 파라볼라 알고리즘
def parabolaImageColor(param):
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    # LookUpTable 기법 활용

    LUT = [0 for _ in range(256)]
    if param == 1:
        for input in range(256):
            LUT[input] = int(255 - 255 * math.pow(input / 128 - 1, 2))
        for RGB in range(3):
            for i in range(inH):
                for k in range(inW):
                    outImage[RGB][i][k] = LUT[inImage[RGB][i][k]]
    else:
        for input in range(256):
            LUT[input] = int(255 * math.pow(input / 128 - 1, 2))
        for RGB in range(3):
            for i in range(inH):
                for k in range(inW):
                    outImage[RGB][i][k] = LUT[inImage[RGB][i][k]]

    displayImageColor()


# 모핑 알고리즘
def  morphImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;
    outW = inW;
    ## 추가 영상 선택
    filename2 = askopenfilename(parent=window,
                                filetypes=(("칼라 파일", "*.jpg;*.png;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if filename2 == '' or filename2 == None:
        return
    inImage2 = []
    photo2 = Image.open(filename2)  # PIL 객체
    inW2 = photo2.width;
    inH2 = photo2.height
    ## 메모리 확보
    for _ in range(3):
        inImage2.append(malloc(inH2, inW2))

    photoRGB2 = photo2.convert('RGB')
    for i in range(inH2):
        for k in range(inW2):
            r, g, b = photoRGB2.getpixel((k, i))
            inImage2[R][i][k] = r
            inImage2[G][i][k] = g
            inImage2[B][i][k] = b

    ## 메모리 확보
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    import threading
    import time
    def morpFunc():
        w1 = 1;
        w2 = 0
        for _ in range(20):
            for RGB in range(3):
                for i in range(inH):
                    for k in range(inW):
                        newValue = int(inImage[RGB][i][k] * w1 + inImage2[RGB][i][k] * w2)
                        if newValue > 255:
                            newValue = 255
                        elif newValue < 0:
                            newValue = 0
                        outImage[RGB][i][k] = newValue
            displayImageColor()
            w1 -= 0.05;
            w2 += 0.05
            time.sleep(0.5)

    threading.Thread(target=morpFunc).start()

# 상하반전 알고리즘
def  upDownImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    ### 진짜 컴퓨터 비전 영상처리 알고리즘 ###
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                outImage[RGB][i][k] = inImage[RGB][inH-i-1][k]

    displayImageColor()

# 화면이동 알고리즘
def moveImageColor() :
    global panYN
    panYN = True
    canvas.configure(cursor='mouse')

def mouseClick(event) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx,sy,ex,ey, panYN
    if panYN == False :
        return
    sx = event.x; sy = event.y

def mouseDrop(event) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx, sy, ex, ey, panYN
    if panYN == False :
        return
    ex = event.x;    ey = event.y
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    mx = sx - ex; my = sy - ey
    for RGB in range(3):
        for i in range(inH) :
            for k in range(inW) :
                if  0 <= i-my < outW and 0 <= k-mx < outH :
                    outImage[RGB][i-my][k-mx] = inImage[RGB][i][k]
    panYN = False
    displayImageColor()

# 영상 축소 알고리즘
def  zoomOutImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("축소", "값-->", minvalue=2, maxvalue=16)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH//scale;  outW = inW//scale;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for i in range(outH) :
        for k in range(outW) :
            for RGB in range(3):
                outImage[RGB][i][k] = inImage[RGB][i*scale][k*scale]

    displayImageColor()

# 영상 확대 알고리즘
def zoomInImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("확대", "값-->", minvalue=2, maxvalue=8)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH*scale;  outW = inW*scale;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for i in range(outH) :
        for k in range(outW) :
            for RGB in range(3):
                outImage[RGB][i][k] = inImage[RGB][i//scale][k//scale]

    displayImageColor()

# 영상 회전 알고리즘
def rotateImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    angle = askinteger("회전", "값-->", minvalue=1, maxvalue=360)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    radian = angle * math.pi / 180
    for i in range(inH) :
        for k in range(inW) :
            for RGB in range(3):
                xs = i ; ys = k;
                xd = int(math.cos(radian) * xs - math.sin(radian) * ys)
                yd = int(math.sin(radian) * xs + math.cos(radian) * ys)
                if 0<= xd < inH and 0 <= yd < inW :
                    outImage[RGB][xd][yd] = inImage[RGB][i][k]

    displayImageColor()

# 영상 회전 알고리즘 - 중심, 역방향
def rotateImageColor2() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    angle = askinteger("회전", "값-->", minvalue=1, maxvalue=360)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    radian = angle * math.pi / 180
    cx = inW//2; cy = inH//2
    for i in range(outH) :
        for k in range(outW) :
            for RGB in range(3):
                xs = i ; ys = k;
                xd = int(math.cos(radian) * (xs-cx) - math.sin(radian) * (ys-cy)) + cx
                yd = int(math.sin(radian) * (xs-cx) + math.cos(radian) * (ys-cy)) + cy
                if 0<= xd < outH and 0 <= yd < outW :
                    outImage[RGB][xs][ys] = inImage[RGB][xd][yd]
                else :
                    outImage[RGB][xs][ys] = 255

    displayImageColor()

## 엠보싱 처리
def  embossImageRGB() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    MSIZE = 3
    mask = [ [-1, 0, 0],
             [ 0, 0, 0],
             [ 0, 0, 1] ]
    ## 임시 입력영상 메모리 확보
    tmpInImage = []
    for _ in range(3):
        tmpInImage.append(malloc(inH+MSIZE-1, inW+MSIZE-1))
    tmpOutImage = []
    for _ in range(3):
        tmpOutImage.append(malloc(outH, outW))

    ## 원 입력 --> 임시 입력
    for i in range(inH) :
        for k in range(inW) :
            for RGB in range(3):
                tmpInImage[RGB][i+MSIZE//2][k+MSIZE//2] = inImage[RGB][i][k]
    ## 회선연산
    for i in range(MSIZE//2, inH + MSIZE//2) :
        for k in range(MSIZE//2, inW + MSIZE//2) :
            # 각 점을 처리.
            S = 0.0
            for m in range(0, MSIZE) :
                for n in range(0, MSIZE) :
                    for RGB in range(3):
                        S += mask[m][n]*tmpInImage[RGB][i+m-MSIZE//2][k+n-MSIZE//2]
                tmpOutImage[RGB][i-MSIZE//2][k-MSIZE//2] = S
    ## 127 더하기 (선택)
    for i in range(outH) :
        for k in range(outW) :
            for RGB in range(3):
                tmpOutImage[RGB][i][k] += 127
    ## 임시 출력 --> 원 출력
    for i in range(outH):
        for k in range(outW):
            for RGB in range(3):
                value = tmpOutImage[RGB][i][k]
                if value > 255 :
                    value = 255
                elif value < 0 :
                    value = 0
                outImage[RGB][i][k] = int(value)

    displayImageColor()

## 엠보싱 처리 (Pillow)
def  embossImagePillow() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo
    outH = inH ; outW = inW
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    photo2 = photo.copy()
    photo2 = photo2.filter(ImageFilter.EMBOSS)

    ## 원 입력 --> 임시 입력
    photoRGB = photo.convert('RGB')
    for i in range(outH):
        for k in range(outW):
            r,g,b = photo2.getpixel((k,i))
            outImage[R][i][k] = r
            outImage[G][i][k] = g
            outImage[B][i][k] = b

    displayImageColor()

import colorsys
## 엠보싱 처리 (HSV)
def  embossImageHSV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 입력용 RGB -> 입력용 HSV 모델로 변환
    ###### 메모리 할당 ################
    inImageHSV = [];
    for _ in range(3):
        inImageHSV.append(malloc(outH, outW))
    # RGB -> HSV
    for i in range(inH):
        for k in range(inW):
            r,g,b = inImage[R][i][k], inImage[G][i][k], inImage[B][i][k]
            h,s,v = colorsys.rgb_to_hsv(r/255,g/255,b/255) # 얘는 input을 0-1로 받아줘서 일케 파라미터 넘겨줌
            inImageHSV[0][i][k], inImageHSV[1][i][k], inImageHSV[2][i][k] = h,s,v

    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    MSIZE = 3
    mask = [ [-1, 0, 0],
             [ 0, 0, 0],
             [ 0, 0, 1] ]
    ## 임시 입력영상 메모리 확보
    # 우리는 V만 바꿔줄거기 때문에 3번할 필요 없음
    tmpInImageV = []
    tmpInImageV = malloc(inH+MSIZE-1, inW+MSIZE-1)
    tmpOutImageV = []
    tmpOutImageV = malloc(outH, outW)

    ## 원 입력 --> 임시 입력
    for i in range(inH) :
        for k in range(inW) :
            tmpInImageV[i+MSIZE//2][k+MSIZE//2] = inImageHSV[2][i][k]
    ## 회선연산
    for i in range(MSIZE//2, inH + MSIZE//2) :
        for k in range(MSIZE//2, inW + MSIZE//2) :
            # 각 점을 처리.
            S = 0.0
            for m in range(0, MSIZE) :
                for n in range(0, MSIZE) :
                    S += mask[m][n]*tmpInImageV[i+m-MSIZE//2][k+n-MSIZE//2]
            tmpOutImageV[i-MSIZE//2][k-MSIZE//2] = S * 255 # 얘는 V정보에 다시 255곱해줘야 함
    ## 127 더하기 (선택)
    for i in range(outH) :
        for k in range(outW) :
            tmpOutImageV[i][k] += 127
            if tmpOutImageV[i][k] > 255:
                tmpOutImageV[i][k] = 255
            elif tmpOutImageV[i][k] < 0:
                tmpOutImageV[i][k] = 0

    # HSV --> RGB
    ## 임시 출력 --> 원 출력
    for i in range(outH):
        for k in range(outW):
            h,s,v = inImageHSV[0][i][k], inImageHSV[1][i][k], tmpOutImageV[i][k]
            r,g,b = colorsys.hsv_to_rgb(h,s,v)
            outImage[R][i][k], outImage[G][i][k], outImage[B][i][k] = int(r),int(g),int(b)

    displayImageColor()

## 엠보싱 처리
def  blurImageRGB() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    MSIZE = 3
    # 마스크 점 안찍어주면 안댐 : 다른언어 변환시에 0됨
    mask = [ [1/9, 1/9, 1/9],
             [ 1/9, 1/9, 1/9],
             [ 1/9, 1/9, 1/9] ]
    ## 임시 입력영상 메모리 확보
    tmpInImage = []
    for _ in range(3):
        tmpInImage.append(malloc(inH+MSIZE-1, inW+MSIZE-1,127))
    tmpOutImage = []
    for _ in range(3):
        tmpOutImage.append(malloc(outH, outW))

    ## 원 입력 --> 임시 입력
    # for문 돌릴 때 RGB 포문을 맨 마지막에 넣었더니 답이 이상하네? 왜?
    for RGB in range(3):
        for i in range(inH) :
            for k in range(inW) :
                tmpInImage[RGB][i+MSIZE//2][k+MSIZE//2] = inImage[RGB][i][k]
    ## 회선연산
    for RGB in range(3):
        for i in range(MSIZE//2, inH + MSIZE//2) :
            for k in range(MSIZE//2, inW + MSIZE//2) :
                # 각 점을 처리.
                S = 0.0
                for m in range(0, MSIZE) :
                    for n in range(0, MSIZE) :
                        S += mask[m][n]*tmpInImage[RGB][i+m-MSIZE//2][k+n-MSIZE//2]
                tmpOutImage[RGB][i-MSIZE//2][k-MSIZE//2] = S
    # ## 127 더하기 (선택)
    # for i in range(outH) :
    #     for k in range(outW) :
    #         for RGB in range(3):
    #             tmpOutImage[RGB][i][k] += 127
    ## 임시 출력 --> 원 출력
    for RGB in range(3):
        for i in range(outH):
            for k in range(outW):
                value = tmpOutImage[RGB][i][k]
                if value > 255 :
                    value = 255
                elif value < 0 :
                    value = 0
                outImage[RGB][i][k] = int(value)

    displayImageColor()


####################
#### 전역변수 선언부 ####
####################
R, G, B = 0, 1, 2 # 3차원으로 쉽게 다루려고 전역 상수 지정해줌
inImage, outImage = [], []
inH, inW, outH, outW = [0] * 4
window, canvas, paper = None, None, None
filename = ""
panYN = False
sx, sy, ex, ey = [0] * 4
VIEW_X, VIEW_Y = 512, 512  # 화면에 보일 크기 (출력용)

####################
#### 메인 코드부 ####
####################
window = Tk()
window.geometry("500x500")
window.title("컴퓨터 비전(color library) ver 0.01")

status = Label(window, text='이미지 정보:', bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

## 마우스 이벤트
mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu)
fileMenu.add_command(label="파일 열기", command=openImageColor)
fileMenu.add_separator()
fileMenu.add_command(label="파일 저장", command=saveImageColor)

comVisionMenu1 = Menu(mainMenu)
mainMenu.add_cascade(label="화소점 처리", menu=comVisionMenu1)
comVisionMenu1.add_command(label="덧셈/뺄셈", command=addImageColor)
comVisionMenu1.add_command(label="반전하기", command=revImageColor)
comVisionMenu1.add_command(label="파라볼라 변환(캡)", command=lambda: parabolaImageColor(1))
comVisionMenu1.add_command(label="파라볼라 변환(컵)", command=lambda: parabolaImageColor(2))
comVisionMenu1.add_command(label="모핑", command=morphImageColor)

comVisionMenu2 = Menu(mainMenu)
mainMenu.add_cascade(label="통계", menu=comVisionMenu2)
comVisionMenu2.add_command(label="흑백화", command=grayscaleImageColor)
comVisionMenu2.add_command(label="이진화", command=bwImageColor)
comVisionMenu2.add_command(label="8진화", command=eightImageColor)
comVisionMenu2.add_command(label="축소(평균변환)", command=zoomOutImageColor2)
comVisionMenu2.add_command(label="확대(양선형보간)", command=zoomInImageColor2)
comVisionMenu2.add_separator()
comVisionMenu2.add_command(label="히스토그램", command=histoImageColor)
# comVisionMenu2.add_command(label="히스토그램(내꺼)", command=histoImage2)
comVisionMenu2.add_command(label="명암대비", command=stretchImageColor)
comVisionMenu2.add_command(label="End-In탐색", command=endinImageColor)
comVisionMenu2.add_command(label="평활화", command=equalizeImageColor)

comVisionMenu3 = Menu(mainMenu)
mainMenu.add_cascade(label="기하학 처리", menu=comVisionMenu3)
comVisionMenu3.add_command(label="상하반전", command=upDownImageColor)
comVisionMenu3.add_command(label="이동", command=moveImageColor)
comVisionMenu3.add_command(label="축소", command=zoomOutImageColor)
comVisionMenu3.add_command(label="확대", command=zoomInImageColor)
comVisionMenu3.add_command(label="회전1", command=rotateImageColor)
comVisionMenu3.add_command(label="회전2(중심,역방향)", command=rotateImageColor2)

comVisionMenu4 = Menu(mainMenu)
mainMenu.add_cascade(label="화소영역 처리", menu=comVisionMenu4)
comVisionMenu4.add_command(label="엠보싱(RGB)", command=embossImageRGB)
comVisionMenu4.add_command(label="엠보싱(Pillow)", command=embossImagePillow)
comVisionMenu4.add_command(label="엠보싱(HSV)", command=embossImageHSV)
comVisionMenu4.add_separator()
comVisionMenu4.add_command(label="블러링(RGB)", command=blurImageRGB)

# comVisionMenu5 = Menu(mainMenu)
# mainMenu.add_cascade(label="기타 입출력", menu=comVisionMenu5)
# comVisionMenu5.add_command(label="MySQL에서 불러오기", command=loadMysql)
# comVisionMenu5.add_command(label="MySQL에 저장하기", command=saveMysql)
# comVisionMenu5.add_separator()
# comVisionMenu5.add_command(label="CSV 열기", command=openCSV)
# comVisionMenu5.add_command(label="CSV로 저장", command=saveCSV)
# comVisionMenu5.add_separator()
# comVisionMenu5.add_command(label="Excel 열기", command=openExcel)
# comVisionMenu5.add_command(label="Excel로 저장", command=saveExcel)
# comVisionMenu5.add_separator()
# comVisionMenu5.add_command(label="Excel art로 열기", command=openExcelArt)
# comVisionMenu5.add_command(label="Excel art로 저장", command=saveExcelArt)

window.mainloop()