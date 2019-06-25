from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import numpy as np
import time
import cv2


####################
#### 함수 선언부 ####
####################
def malloc(h, w, initValue=0,layers = 1, dataType=np.uint8) :
    retMemory = np.zeros((h,w,layers),dtype=dataType)
    retMemory += initValue
    return retMemory

import numpy as np
# 파일을 메모리로 로딩하는 함수
def loadImageColor(fnameOrCvData) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto

    #######################################
    ### PIL 객체 --> OpenCV 객체로 복사 ###
    ## 이거 왜 되는지 잘 생각해보자!!
    if type(fnameOrCvData) == str: # 파일명이 들어왔을경우
        cvData = cv2.imread(fnameOrCvData) # 파일 --> CV 데이터
    else:
        CvData = fnameOrCvData
    cvPhoto = cv2.cvtColor(cvData, cv2.COLOR_BGR2RGB) # 중요한 CV개체

    photo = Image.fromarray(cvPhoto)
    inW, inH = photo.size  # (photo.width, photo.height)
    #######################################
    inImage = np.array(photo)

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

def displayImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global cvPhoto
    if canvas != None : # 예전에 실행한 적이 있다.
        canvas.destroy()
    global VIEW_X, VIEW_Y
    # VIEW_X, VIEW_Y = 512, 512
    ## 고정된 화면 크기
    # 가로/세로 비율 계산

    if outW <= 512 and outH <= 512 : # 정방형 관계없이 둘다 512보다 작으면 그냥 사용
        VIEW_X = outH
        VIEW_Y = outW
    else : # 한쪽이라도 512보다 크면
        ratio = outH / outW
        if ratio < 1:
            VIEW_X = int(512 * ratio)
            if outW > 512 :
                VIEW_Y = 512
            else :
                VIEW_Y = outW
        elif ratio > 1:
            ratio = 1/ratio
            if outH > 512 :
                VIEW_X = 512
            else :
                VIEW_X = outH
            VIEW_Y = int(512 * ratio)
        else :
            if outH > 512:
                VIEW_X = 512
            else:
                VIEW_X = outH
            if outW > 512:
                VIEW_Y = 512
            else:
                VIEW_Y = outW

    if outH <= VIEW_X :
        stepX = 1
    if outH > VIEW_X :
        stepX = outH / VIEW_X

    if outW <= VIEW_Y:
         stepY = 1
    if outW > VIEW_Y:
        stepY = outW / VIEW_Y

    print(VIEW_X, VIEW_Y, stepX, stepY)

    window.geometry(str(int(VIEW_Y*1.2)) + 'x' + str(int(VIEW_X*1.2)))  # 벽
    canvas = Canvas(window, height=VIEW_X, width=VIEW_Y)
    paper = PhotoImage(height=VIEW_X, width=VIEW_Y)
    canvas.create_image((VIEW_Y // 2, VIEW_X // 2), image=paper, state='normal')

    import numpy
    rgbStr = '' # 전체 픽셀의 문자열을 저장
    for i in numpy.arange(0,outH, stepX) :
        tmpStr = ''
        for k in numpy.arange(0,outW, stepY) :
            i = int(i); k = int(k)
            r , g, b = outImage[i,k,R], outImage[i,k,G], outImage[i,k,B]
            tmpStr += ' #%02x%02x%02x' % (r,g,b)
        rgbStr += '{' + tmpStr + '} '
    paper.put(rgbStr)

    inImage = outImage[:]
    cvPhoto = outImage[:]

    canvas.pack(expand=1, anchor=CENTER)
    status.configure(text='이미지 정보:' + str(outW) + 'x' + str(outH))

import numpy as np
def saveImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if outImage == None:
        return
    outArray = []
    for i in range(outH):
        tmpList = []
        for k in range(outW):
            tup = tuple([outImage[i,k,R],outImage[i,k,G],outImage[i,k,B]]) # rgblist를 튜플로 묶어서 넘겨줘야 저장할 수 있음
            tmpList.append(tup)
        outArray.append(tmpList)

    outArray = np.array(outArray)
    savePhoto = Image.fromarray(outArray.astype(np.uint8),'RGB') # fromarray 메서드에서 튜플로 묶여있는 array를 가져와야 읽을 수 있음

    saveFp = asksaveasfile(parent=window, mode="wb", defaultextension='.',
                           filetypes=(("그림파일", "*.jpg;*.png;*.bmp;*.tif"), ("모든 파일", "*.*")))

    if saveFp == '' or saveFp == None:
        return

    savePhoto.save(saveFp.name)
    print('Save complete')
    saveFp.close()

# 동일영상 알고리즘
def  equalImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    # outImage = ImageEnhance._Enhance(inImage)
    # print(inImage)
    # print(inImage.shape)
    # print(outImage)
    outImage = inImage.copy()

    displayImageColor()

# 밝기조절
# astype을 안바꿔주면 색깔이 이상하게 나옴! : uint8 : 0~255
def addImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outH = inH; outW = inW
    value = askinteger("밝게/어둡게", "값-->", minvalue=-255, maxvalue=255)
    outImage = inImage.astype(np.uint16)
    outImage = outImage + value
    outImage = np.where(outImage>255, 255,\
        np.where(outImage<0, 0, outImage))
    outImage = outImage.astype(np.uint8)

    displayImageColor()


# 반전영상 알고리즘
def revImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outImage = 255 - inImage

    displayImageColor()

# 흑백화 알고리즘
def  grayscaleImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = inImage.copy()
    # print(inImage.shape)
    # print(outImage.shape)
    # print(outImage[:,:,R].shape)
    # print(inImage[:,:,R].shape)
    # print((inImage[:,:,R]*0.233+inImage[:,:,G]*0.23).shape)
    # print(type((inImage[:,:,R] * 0.2126 + inImage[:,:,G] * 0.7152 + inImage[:,:,B] * 0.0722))) # 이런식으로 슬라이싱하여 쓸 수 있다 : 오타는 항상 조심!
    outImage[:,:,R] = np.array((inImage[:,:,R] * 0.2126 + inImage[:,:,G] * 0.7152 + inImage[:,:,B] * 0.0722))
    outImage[:,:,G] = outImage[:,:,R].copy()
    outImage[:,:,B] = outImage[:,:,R].copy()

    displayImageColor()

# 이진화 알고리즘
def  bwImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    grayScaleImage = inImage.copy()
    grayScaleImage[:,:,R] = np.array((inImage[:,:,R] * 0.2126 + inImage[:,:,G] * 0.7152 + inImage[:,:,B] * 0.0722))
    grayScaleImage[:,:,G] = grayScaleImage[:,:,R].copy()
    grayScaleImage[:,:,B] = grayScaleImage[:,:,R].copy()

    outImage = np.where(grayScaleImage>127,255,0)

    displayImageColor()

# 8진화 알고리즘
def  eightImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;

    ## 영상의 평균 구하기.
    meanRGB = [inImage[:,:,R].mean(), inImage[:,:,G].mean(), inImage[:,:,B].mean()]

    outImage = inImage.copy()
    outImage[:,:,R] = np.where(inImage[:,:,R]>meanRGB[R],255,0)
    outImage[:,:,G] = np.where(inImage[:,:,G]>meanRGB[G],255,0)
    outImage[:,:,B] = np.where(inImage[:,:,B]>meanRGB[B],255,0)

    displayImageColor()

# 영상 축소 알고리즘 (평균변환)
def  zoomOutImageColor2() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("축소", "값-->", minvalue=2, maxvalue=16)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH//scale;  outW = inW//scale
    ###### 메모리 할당 ################
    outImage = malloc(outH,outW,layers=3) # 3차원 numpy배열 생성
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    
    for i in range(outH):
        for k in range(outW):
            fromY = i*scale; toY = fromY+scale; fromX = k*scale; toX = fromX+scale
            outImage[i,k,R] = inImage[fromY:toY,fromX:toX,R].mean()
            outImage[i,k,G] = inImage[fromY:toY,fromX:toX,G].mean()
            outImage[i,k,B] = inImage[fromY:toY,fromX:toX,B].mean()

    displayImageColor()


# 영상 확대 알고리즘 (양선형 보간)
def  zoomInImageColor2() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("확대", "값-->", minvalue=2, maxvalue=8)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH*scale;  outW = inW*scale
    ###### 메모리 할당 ################
    outImage = malloc(outH,outW,layers=3)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    rH, rW, iH, iW = [0] * 4 # 실수위치 및 정수위치
    x, y = 0, 0 # 실수와 정수의 차이값
    C1,C2,C3,C4 = [0] * 4 # 결정할 위치(N)의 상하좌우 픽셀

    # 이거 넘파이로 바꿀 방법 있는가?
    for RGB in range(3):
        for i in range(outH) :
            for k in range(outW) :
                rH = i / scale ; rW = k / scale
                iH = int(rH) ;  iW = int(rW)
                x = rW - iW; y = rH - iH
                if 0 <= iH < inH-1 and 0 <= iW < inW-1 :
                    C1 = inImage[iH,iW,RGB]
                    C2 = inImage[iH,iW+1,RGB]
                    C3 = inImage[iH+1,iW+1,RGB]
                    C4 = inImage[iH+1,iW,RGB]
                    newValue = C1*(1-y)*(1-x) + C2*(1-y)* x+ C3*y*x + C4*y*(1-x)
                    try:
                        outImage[i,k,RGB] = int(newValue)
                    except:
                        pass

    displayImageColor()

# histogram 보여주고나면 왜 UI가 바뀜?
import matplotlib.pyplot as plt
# 현재 흑백사진은 안됨 => 안되는 이유 파악해서 할 것
def histoImageColor():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW

    incountlist = [ [ _ for _ in range(256) ] for _ in range(3)  ]
    outcountlist = [ [ _ for _ in range(256) ] for _ in range(3) ]


    for i in range(inH):
        for k in range(inW):
            for RGB in range(3):
                incountlist[RGB][inImage[i,k,RGB]] += 1

    print(outImage)
    for i in range(outH):
        for k in range(outW):
            for RGB in range(3):
                outcountlist[RGB][outImage[i,k,RGB]] += 1

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

    displayImageColor()


# 스트레칭 알고리즘
def  stretchImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW
    outImage = inImage.copy()
    maxValList = [inImage[:,:,R].max(), inImage[:,:,G].max(), inImage[:,:,B].max()]
    minValList = [inImage[:,:,R].min(), inImage[:,:,G].min(), inImage[:,:,B].min()]
    for RGB in range(3):
        outImage[:,:,RGB] = ((inImage[:,:,RGB] - minValList[RGB]) / (maxValList[RGB] - minValList[RGB])) * 255

    displayImageColor()


# 스트레칭 알고리즘
# outImage의 형식을 float로 변환하지 않아서 식을 계산하는 과정에서 손실이 많이 발생했었음
def  endinImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outH = inH;  outW = inW
    outImage = inImage.copy()
    outImage = outImage.astype(np.float16)
    maxValList = [inImage[:,:,R].max(), inImage[:,:,G].max(), inImage[:,:,B].max()]
    minValList = [inImage[:,:,R].min(), inImage[:,:,G].min(), inImage[:,:,B].min()]

    minAdd = askinteger("최소", "최소에서추가-->", minvalue=0, maxvalue=255)
    maxAdd = askinteger("최대", "최대에서감소-->", minvalue=0, maxvalue=255)

    for RGB in range(3):
        minValList[RGB] += minAdd
        maxValList[RGB] -= maxAdd

    for RGB in range(3):
        outImage[:,:,RGB] = ((outImage[:,:,RGB] - minValList[RGB]) / (maxValList[RGB] - minValList[RGB])) * 255 # 여기 계산할때 만약 outImage가 datatype가 uint8이면 손실발생
    
    outImage = np.where(outImage>255, 255,\
        np.where(outImage<0,0,outImage))
    outImage = outImage.astype(np.uint8)
    print(outImage.max(),outImage.min())

    displayImageColor()

# 평활화 알고리즘
def  equalizeImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = malloc(outH, outW, layers=3)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    # 히스토그램
    histo = np.array([np.bincount(inImage[:,:,RGB].flatten(), minlength=256) for RGB in range(3)]) # 256을 min으로 잡아줘야 함
    sumHisto = np.array([[0] * 256 for _ in range(3)]); normalHisto = np.array([[0] * 256 for _ in range(3)])

    ## 누적히스토그램
    # np.bincount 256개 사이즈가 나와야하는데 : minlength=256 주면 됨 : 0~255
    for RGB in range(3):
        sValue = 0
        for i in range(len(histo[0])) : # [0]을 안잡아주면 len이 3 이 되어서 3번밖에 안더함 --> 너무 값이 다 작아져서 전부 0되버리기!
            print(len(histo[0]))
            sValue += histo[RGB,i]
            sumHisto[RGB,i] = sValue
    ## 정규화 누적 히스토그램
    sumHisto.astype(np.float16)
    normalHisto = (sumHisto / (inW*inH)) * 255
    normalHisto = normalHisto.astype(np.uint8)
    ## 영상처리
    for RGB in range(3):
        outImage[:,:,RGB] = normalHisto[RGB][inImage[:,:,RGB]]
    # outImage[:, :, RGB] = normalHisto[RGB][inImage[:, :, RGB]]
    displayImageColor()

# 파라볼라 알고리즘
def parabolaImageColor(param):
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    # LookUpTable 기법 활용
    outH = inH; outW = inW
    # inImage = inImage.astype(np.float32)
    # outImage = inImage.copy()

    LUT = np.array([[ _ for _ in range(256) ] for _ in range(3)])
    if param == 1:
        LUT = (255 - 255 * np.power(LUT / 128 - 1, 2))
        LUT = LUT.astype(np.uint8)
        print(LUT)
        for RGB in range(3):
            outImage[:,:,RGB] = LUT[RGB,inImage[:,:,RGB]]
            outImage = outImage.astype(np.uint8)
    else:
        LUT = (255 * np.power(LUT / 128 - 1, 2))
        LUT = LUT.astype(np.uint8)
        print(LUT)
        for RGB in range(3):
            outImage[:,:,RGB] = LUT[RGB,inImage[:,:,RGB]]
            outImage = outImage.astype(np.uint8)

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
    # inImage2 = []
    photo2 = Image.open(filename2)  # PIL 객체
    inW2 = photo2.width;
    inH2 = photo2.height
    ## 메모리 확보
    inImage2 = malloc(inH, inW, layers=3)

    photoRGB2 = photo2.convert('RGB')
    for i in range(inH2):
        for k in range(inW2):
            r, g, b = photoRGB2.getpixel((k, i))
            inImage2[i][k][R] = r
            inImage2[i][k][G] = g
            inImage2[i][k][B] = b

    ## 메모리 확보
    outImage = malloc(outH, outW, layers=3)

    import threading
    import time
    def morpFunc():
        w1 = 1;
        w2 = 0
        for _ in range(20):
            for RGB in range(3):
                for i in range(inH):
                    for k in range(inW):
                        newValue = int(inImage[i][k][RGB] * w1 + inImage2[i][k][RGB] * w2)
                        if newValue > 255:
                            newValue = 255
                        elif newValue < 0:
                            newValue = 0
                        outImage[i][k][RGB] = newValue
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
    outImage = inImage[:]

    ### 진짜 컴퓨터 비전 영상처리 알고리즘 ###
    outImage = inImage[::-1,:,:]
    # filp 써서 내일 하자
    # outImage = flip(inImage,)

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
    outImage = malloc(outH, outW, layers=3)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for i in range(outH) :
        for k in range(outW) :
            for RGB in range(3):
                outImage[i][k][RGB] = inImage[i*scale][k*scale][RGB]

    displayImageColor()

# 영상 확대 알고리즘
def zoomInImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("확대", "값-->", minvalue=2, maxvalue=8)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH*scale;  outW = inW*scale;
    ###### 메모리 할당 ################
    outImage = malloc(outH, outW, layers=3)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for i in range(outH) :
        for k in range(outW) :
            for RGB in range(3):
                outImage[i][k][RGB] = inImage[i//scale][k//scale][RGB]

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
    global photo, cvPhoto
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
sx, sy, ex, ey = [0] * 4
def  embossImageHSV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx, sy, ex, ey
    # 이벤트 바인드
    canvas.bind('<Button-3>', rightMouseClick_embossImageHSV)
    canvas.bind('<Button-1>', leftMouseClick)
    canvas.bind('<B1-Motion>', leftMouseMove) # rubber band 만들장
    canvas.bind('<ButtonRelease-1>', leftMouseDrop_embossImageHSV)
    canvas.configure(cursor='mouse')

def rightMouseClick_embossImageHSV(event):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx, sy, ex, ey
    sx = 0; sy = 0; ex = inW - 1; ey = inH - 1 # 마지막 선택한 점까지 쓰겠다
    #############################
    __embossImageHSV()
    #############################
    canvas.unbind('<Button-3>')
    canvas.unbind('<Button-1>')
    canvas.unbind('<B1-Motion>')
    canvas.unbind('<ButtonRelease-1>')

def leftMouseClick(event):
    global sx, sy, ex, ey
    sx = event.x; sy = event.y

boxline = None
def leftMouseMove(event):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx, sy, ex, ey, boxline
    ex = event.x ; ey = event.y
    if not boxline:
        pass
    else:
        canvas.delete(boxline)
    boxline = canvas.create_rectangle(sx,sy,ex,ey,fill=None)

def leftMouseDrop_embossImageHSV(event):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx, sy, ex, ey
    ex = event.x;
    ey = event.y  # 마지막 선택한 점까지 쓰겠다
    if inH > VIEW_X :
        sx = int(sx * (inH / VIEW_X)); ex = int(ex * (inH / VIEW_X))
    if inW > VIEW_Y :
        sy = int(sy * (inW / VIEW_Y)); ey = int(ey * (inW / VIEW_Y))

    # 마우스 클릭을 어떤 방향이든지 인정
    if sx > ex :
        sx, ex = ex, sx
    if sy > ey :
        sy, ey = ey, sy
    #############################
    __embossImageHSV()
    #############################
    canvas.unbind('<Button-3>')
    canvas.unbind('<Button-1>')
    canvas.unbind('<B1-Motion>')
    canvas.unbind('<ButtonRelease-1>')

## 엠보싱 처리 (HSV)
from matplotlib.colors import rgb_to_hsv
def  __embossImageHSV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 입력용 RGB -> 입력용 HSV 모델로 변환
    ###### 메모리 할당 ################
    inImageHSV = malloc(inH,inW,layers=3)
    # RGB -> HSV
    inImageHSV = rgb_to_hsv(inImage) # matplotlib에 있당
    # for i in range(inH):
    #     for k in range(inW):
    #         r,g,b = inImage[i,k,R], inImage[i,k,G],inImage[i,k,B]
    #         h,s,v = colorsys.rgb_to_hsv(r/255,g/255,b/255) # 얘는 input을 0-1로 받아줘서 일케 파라미터 넘겨줌
    #         inImageHSV[i,k,R], inImageHSV[i,k,G], inImageHSV[i,k,B] = h,s,v

    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = malloc(outH,outW,layers=3)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    MSIZE = 3
    mask = [ [-1, 0, 0],
             [ 0, 0, 0],
             [ 0, 0, 1] ]
    ## 임시 입력영상 메모리 확보
    # 우리는 V만 바꿔줄거기 때문에 3번할 필요 없음
    tmpInImageV = malloc(inH+MSIZE-1, inW+MSIZE-1)
    tmpOutImageV = malloc(outH, outW)

    ## 원 입력 --> 임시 입력
    tmpInImageV = inImageHSV[:,:,2] # V
    # for i in range(inH) :
    #     for k in range(inW) :
    #         tmpInImageV[i+MSIZE//2][k+MSIZE//2] = inImageHSV[2][i][k]
    ## 회선연산

    for i in range(MSIZE//2, inH + MSIZE//2) :
        for k in range(MSIZE//2, inW + MSIZE//2) :
            # 각 점을 처리.
            S = 0.0
            for m in range(0, MSIZE) :
                for n in range(0, MSIZE) :
                    try:
                        S += mask[m][n]*tmpInImageV[i+m-MSIZE//2][k+n-MSIZE//2]
                    except:
                        pass
            tmpOutImageV[i-MSIZE//2][k-MSIZE//2] = S * 255 # 얘는 V정보에 다시 255곱해줘야 함
    ## 127 더하기 (선택)
    tmpOutImageV = np.where(tmpOutImageV+127 > 255, 255,
                            np.where(tmpOutImageV+127<0, 0, tmpOutImageV+127))
    # for i in range(outH) :
    #     for k in range(outW) :
    #         tmpOutImageV[i][k] += 127
    #         if tmpOutImageV[i][k] > 255:
    #             tmpOutImageV[i][k] = 255
    #         elif tmpOutImageV[i][k] < 0:
    #             tmpOutImageV[i][k] = 0

    # HSV --> RGB
    ## 임시 출력 --> 원 출력
    for i in range(outH):
        for k in range(outW):
            if sx <= k <= ex and sy <= i <= ey: #범위에 포함되면
                h,s,v = inImageHSV[i,k,0], inImageHSV[i,k,1], tmpOutImageV[i][k]
                r,g,b = colorsys.hsv_to_rgb(h,s,v)
                outImage[i,k,R], outImage[i,k,G], outImage[i,k,B] = int(r),int(g),int(b)
            else:
                outImage[i,k,R], outImage[i,k,G], outImage[i,k,B] = inImage[i,k,R], inImage[i,k,G], inImage[i,k,B]

    displayImageColor()

## 블러링 처리
def  blurImageRGB() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = malloc(outH, outW, layers=3)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    MSIZE = 3
    # 마스크 점 안찍어주면 안댐 : 다른언어 변환시에 0됨
    mask = [ [1/9, 1/9, 1/9],
             [ 1/9, 1/9, 1/9],
             [ 1/9, 1/9, 1/9] ]
    ## 임시 입력영상 메모리 확보
    tmpInImage = malloc(inH+MSIZE-1, inW+MSIZE-1,initValue=127,layers=3,dataType=np.float64)
    tmpOutImage = malloc(outH,outW,layers=3,dataType=np.float64)

    ## 원 입력 --> 임시 입력
    npad = ((MSIZE-2,MSIZE-2),(MSIZE-2,MSIZE-2))
    for RGB in range(3):
        tmpInImage[:,:,RGB] = np.pad(inImage[:,:,RGB], npad, 'constant', constant_values=(127))
    # for RGB in range(3):
    #     for i in range(inH) :
    #         for k in range(inW) :
    #             tmpInImage[RGB][i+MSIZE//2][k+MSIZE//2] = inImage[RGB][i][k]
    ## 회선연산
    for RGB in range(3):
        for i in range(MSIZE//2, inH + MSIZE//2) :
            for k in range(MSIZE//2, inW + MSIZE//2) :
                fromY, toY = i, i+MSIZE; fromX, toX = k, k+MSIZE
                try:
                    tmpOutImage[i-MSIZE//2,k-MSIZE//2,RGB] = (tmpInImage[fromY:toY,fromX:toX,RGB] * mask).sum()
                except:
                    pass
                # S += mask[m][n]*tmpInImage[RGB][i+m-MSIZE//2][k+n-MSIZE//2]
                # tmpOutImage[RGB][i-MSIZE//2][k-MSIZE//2] = S
    ## 127 더하기 (선택)
    tmpOutImage = tmpOutImage + 127
    ## 임시 출력 --> 원 출력
    tmpOutImage = np.where(tmpOutImage>255, 255,\
        np.where(tmpOutImage<0, 0, tmpOutImage))
    outImage = tmpOutImage.astype(np.uint8)
    print(outImage.shape)

    displayImageColor()

## 채도 (Pillow)
def  addSvaluePillow() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    value = askfloat("","0~1~10")
    photo2 = photo.copy()
    photo2 = ImageEnhance.Color(photo2)
    photo2 = photo2.enhance(value) # 꼭 이렇게 써줘야 됨

    outH = inH ; outW = inW
    outImage = malloc(inH,inW,layers=3)

    ## 원 입력 --> 임시 입력
    for i in range(outH):
        for k in range(outW):
            r,g,b = photo2.getpixel((k,i))
            outImage[i,k,R]= r
            outImage[i,k,G] = g
            outImage[i,k,B] = b

    displayImageColor()

## 채도 (HSV)
def  addSvalueHSV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 입력용 RGB -> 입력용 HSV 모델로 변환
    ###### 메모리 할당 ################
    inImageHSV = malloc(inH,inW,layers=3,dataType=np.float32)
    value = askfloat('','-255-255')
    value /= 255

    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = malloc(outH,outW,layers=3)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    # RGB -> HSV
    for i in range(inH):
        for k in range(inW):
            r,g,b = inImage[i,k,R], inImage[i,k,G], inImage[i,k,B]
            h,s,v = colorsys.rgb_to_hsv(r/255,g/255,b/255) # 얘는 input을 0-1로 받아줘서 일케 파라미터 넘겨줌
            inImageHSV[i,k,0], inImageHSV[i,k,1], inImageHSV[i,k,2] = h,s,v

    # HSV --> RGB
    ## 임시 출력 --> 원 출력
    for i in range(outH):
        for k in range(outW):
            newS = inImageHSV[i,k,1]+ value
            if newS < 0:
                newS = 0
            elif newS > 1.0:
                newS = 1.0
            h,s,v = inImageHSV[i,k,0], newS, inImageHSV[i,k,2]*255
            r,g,b = colorsys.hsv_to_rgb(h,s,v)
            outImage[i,k,R], outImage[i,k,G], outImage[i,k,B] = int(r),int(g),int(b)

    outImage = outImage.astype(np.uint8)

    displayImageColor()

## 임시 경로에 outImage를 저장하기.
import struct
import random
def saveTempImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    import tempfile

    outArray = []
    for i in range(outH):
        tmpList = []
        for k in range(outW):
            tup = tuple([outImage[i][k][R], outImage[i][k][G], outImage[i][k][B]])  # rgblist를 튜플로 묶어서 넘겨줘야 저장할 수 있음
            tmpList.append(tup)
        outArray.append(tmpList)

    outArray = np.array(outArray)
    savePhoto = Image.fromarray(outArray.astype(np.uint8), 'RGB')  # fromarray 메서드에서 튜플로 묶여있는 array를 가져와야 읽을 수 있음

    saveFp = tempfile.gettempdir() + "/" + str(random.randint(10000, 99999)) + ".jpg"
    if saveFp == '' or saveFp == None :
        return
    print(saveFp)
    savePhoto.save(saveFp)
    return saveFp

def findStat(fname) :
    # 파일 열고, 읽기.
    outW, outH = Image.open(fname).size

    sumList = [0, 0, 0]
    avgList = [0, 0, 0]
    minValList = [0, 0, 0]
    maxValList = [0, 0, 0]
    for i in range(outH) :
        for k in range(outW) :
            for RGB in range(3):
                sumList[RGB] += outImage[i][k][RGB]
    for RGB in range(3):
        avgList[RGB] = sumList[RGB] // (inW * inH)

    for i in range(outH):
        for k in range(outW):
            for RGB in range(3):
                if inImage[i][k][RGB] < minValList[RGB]:
                    minValList[RGB] = inImage[i][k][RGB]
                elif inImage[i][k][RGB] > maxValList[RGB]:
                    maxValList[RGB] = inImage[i][k][RGB]
    return avgList, maxValList, minValList

import pymysql
IP_ADDR = '192.168.56.101'; USER_NAME = 'root'; USER_PASS = '1234'
DB_NAME = 'BigData_DB'; CHAR_SET = 'utf8'
def saveMysqlColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS,
                          db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()

    try:
        sql = '''
                CREATE TABLE colorImage_TBL (
                color_id INT AUTO_INCREMENT PRIMARY KEY,
                color_fname VARCHAR(30),
                color_extname CHAR(5),
                color_height SMALLINT, color_width SMALLINT,
                colorR_avg  TINYINT UNSIGNED , 
                colorR_max  TINYINT UNSIGNED,  colorR_min  TINYINT UNSIGNED,
                colorG_avg  TINYINT UNSIGNED , 
                colorG_max  TINYINT UNSIGNED,  colorG_min  TINYINT UNSIGNED,
                colorB_avg  TINYINT UNSIGNED , 
                colorB_max  TINYINT UNSIGNED,  colorB_min  TINYINT UNSIGNED,
                color_data LONGBLOB);
            '''
        cur.execute(sql)
    except:
        pass

    ## outImage를 임시 폴더에 저장하고, 이걸 fullname으로 전달.
    fullname = saveTempImageColor()
    # 이제 fullname이 str이 됨
    with open(fullname, 'rb') as rfp:
        binData = rfp.read()

    fname, extname = os.path.basename(fullname).split(".") # string 둘로 쪼개고
    im = Image.open(fullname)
    # 일단 수정 후에 저장한다는 전제하에 이름을 다른이름으로 저장
    fname = askstring('안내','파일 이름을 입력해주세요')
    width = im.width ; height = im.height
    avgValList, maxValList, minValueList = findStat(fullname)  # 평균,최대,최소
    sql = "INSERT INTO colorImage_TBL(color_id , color_fname,color_extname,"
    sql += "color_height,color_width,colorR_avg,colorR_max,colorR_min,colorG_avg,"
    sql += "colorG_max,colorG_min,colorB_avg,colorB_max,colorB_min,color_data) "
    sql += " VALUES(NULL,'" + fname + "','" + extname + "',"
    sql += str(height) + "," + str(width) + ","
    sql += str(avgValList[0]) + "," + str(maxValList[0]) + "," + str(minValueList[0])+ ","
    sql += str(avgValList[1]) + "," + str(maxValList[1]) + "," + str(minValueList[1]) + ","
    sql += str(avgValList[2]) + "," + str(maxValList[2]) + "," + str(minValueList[2])
    sql += ", %s )"
    tupleData = (binData,)
    cur.execute(sql, tupleData)
    con.commit()
    cur.close()
    con.close()
    # os.remove(fullname)
    print("업로드 OK --> colorImage_TBL" )


def loadMysqlColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS,
                          db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()
    sql = "SELECT color_id, color_fname, color_extname, color_height, color_width "
    sql += "FROM colorImage_TBL"
    cur.execute(sql)

    queryList = cur.fetchall()
    rowList = [ ':'.join(map(str,row)) for row in queryList]
    import tempfile
    def selectRecord( ) :
        global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
        selIndex = listbox.curselection()[0]
        subWindow.destroy()
        raw_id = queryList[selIndex][0]
        sql = "SELECT color_fname, color_extname, color_data FROM colorImage_TBL "
        sql += "WHERE color_id = " + str(raw_id)
        cur.execute(sql)
        fname, extname, binData = cur.fetchone()

        fullPath = tempfile.gettempdir() + '/' + fname + "." + extname

        with open(fullPath, 'wb') as wfp: # 걍 open에다가 wb(바이너리 쓰기) 형식으로 쓰고
            wfp.write(binData) # 거따가 binData 때려넣기
        cur.close()
        con.close()

        loadImageColor(fullPath)
        equalImageColor()

    ## 서브 윈도에 목록 출력하기.
    subWindow = Toplevel(window)
    listbox = Listbox(subWindow)
    button = Button(subWindow, text='선택', command = selectRecord)

    for rowStr in rowList :
        listbox.insert(END, rowStr)

    listbox.pack(expand=1, anchor=CENTER)
    button.pack()
    subWindow.mainloop()


    cur.close()
    con.close()

# CSV파일을 메모리로 로딩하는 함수
def loadCSVColor(fname) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    fsize = 0 # 헤더 없는 파일 기준
    # 사이즈가 정방형이 아닐수도 있다?
    maxRow = 0
    maxCol = 0
    with open(fname, 'r') as rFp:
        for row_list in rFp:
            row, col, Rvalue, Gvalue, Bvalue = list(map(int,row_list.strip().split(','))) # row_list 각각에 int함수 적용해주고 그 전체에 list함수적용
            if row > maxRow:
                maxRow = row
            if col > maxCol:
                maxCol = col
    inH, inW = maxCol+1, maxRow+1
    print(inH," ",inW)
    ## 입력영상 메모리 확보 ##
    inImage=malloc(inH,inW,layers=3)
    # 파일 --> 메모리
    with open(fname, 'r') as rFp:
        for row_list in rFp:
            row, col, Rvalue, Gvalue, Bvalue = list(map(int, row_list.strip().split(',')))  # row_list 각각에 int함수 적용해주고 그 전체에 list함수적용
            inImage[row][col][R] = Rvalue
            inImage[row][col][G] = Gvalue
            inImage[row][col][B] = Bvalue

# 파일을 선택해서 메모리로 로딩하는 함수
def openCSVColor() :
    global window, canvas, paper, filename, inImage, outImage,inH, inW, outH, outW
    filename = askopenfilename(parent=window,
                filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))
    if filename == '' or filename == None :
        return
    loadCSVColor(filename)
    equalImageColor()

import csv
def saveCSVColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    saveFp = asksaveasfile(parent=window, mode='wb',
        defaultextension='*.csv', filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))
    print(saveFp, type(saveFp))
    if saveFp == '' or saveFp == None :
        return
    with open(saveFp.name, 'w',newline='') as wFp: # newline지정 안해주면 빈중 생겨서 안댐
        csvWriter = csv.writer(wFp)
        for i in range(outH):
            for k in range(outW):
                row_list = [i,k,outImage[i][k][R],outImage[i][k][G],outImage[i][k][B]]
                csvWriter.writerow(row_list) # 인자를 list로 받음
    print('CSV. Save OK')

import xlrd
def loadExcelColor(fname):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    wb = xlrd.open_workbook(fname)
    sheets = wb.sheets()

    nrows = sheets[0].nrows
    ncols = sheets[0].ncols

    inH = outH = nrows ; inW = outH = ncols
    fsize = inH * inW


    # 입력영상 메모리 확보
    inImage = malloc(inH,inW,layers=3)

    # 파일 -> 메모리
    for i in range(inH):
        for k in range(inW):
            rVal, gVal, bVal = sheets[0].cell_value(i,k).split(",")
            inImage[i,k,R] = int(rVal)
            inImage[i,k,G] = int(gVal)
            inImage[i,k,B] = int(bVal)

    outImage = inImage[:]

def openExcelColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    filename = askopenfilename(parent=window,
                               filetypes=(("Excel 파일", "*.xls"), ("모든 파일", "*.*")))
    if filename == '' or filename == None:
        return
    loadExcelColor(filename)
    equalImageColor()

import xlwt
# xlwt로 저장하면 256 * 256R까지밖에 저장안됨
def saveExcelColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
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
            ws.write(i,k,str(outImage[i,k,R])+","+str(outImage[i,k,G])+","+str(outImage[i,k,G]))

    wb.save(xlsname)
    print('Excel. Save OK')

#####################################
####### OpenCV용 데이터 처리 ########
#####################################

def toColorOutArr(pillowPhoto):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    # if inImage == None:
    #     return

    outH = pillowPhoto.height; outW = pillowPhoto.width
    # outImage = malloc(outH,outW,layers=3)

    photoRGB = pillowPhoto.convert('RGB')
    outImage = np.array(photoRGB)
    # inImage = outImage[:]
    # cvPhoto = outImage[:]
    displayImageColor()

def embossOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    # if not inImage:
    #     return

    # 복사본 준비
    cvPhoto2 = cvPhoto[:]

    # 마스크 준비
    mask = np.zeros((3,3), dtype=np.float32)
    mask[0,0] = -1
    mask[2,2] = 1
    cvPhoto2 = cv2.filter2D(cvPhoto2, -1, mask)
    cvPhoto2 += 127

    # PILLOW 객체에게 아예 통짜로 넘겨버리자 (outImage로)
    photo2 = Image.fromarray(cvPhoto2)
    toColorOutArr(photo2)

def greyscaleOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    # if inImage == None:
    #     return

    # 복사본 준비
    cvPhoto2 = cvPhoto[:]
    cvPhoto2 = cv2.cvtColor(cvPhoto2, cv2.COLOR_RGB2GRAY) # 요부분이 greyscale로 바꿔줌

    # PILLOW 객체에게 아예 통짜로 넘겨버리자 (outImage로)
    photo2 = Image.fromarray(cvPhoto2)
    toColorOutArr(photo2)

def blurOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    # if inImage == None:
    #     return

    mSize = askinteger("블러링", "마스크 크기(홀수): ")
    # 복사본 준비
    cvPhoto2 = cvPhoto[:]

    # 마스크 준비
    mask = np.ones((mSize,mSize), dtype=np.float32) / (mSize*mSize) # 9*9 마스크
    cvPhoto2 = cv2.filter2D(cvPhoto2, -1, mask)
    # cvPhoto2 += 127

    # PILLOW 객체에게 아예 통짜로 넘겨버리자 (outImage로)
    photo2 = Image.fromarray(cvPhoto2)
    toColorOutArr(photo2)

def rotateOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    # if inImage == None:
    #     return
    angle = askinteger("회정", "각도: ")
    # 복사본 준비
    cvPhoto2 = cvPhoto[:]
    rotate_matrix = cv2.getRotationMatrix2D((outH//2, outW//2), angle, 1) # 중앙점, 각도, 스케일
    cvPhoto2 = cv2.warpAffine(cvPhoto2, rotate_matrix, (outH, outW))

    # PILLOW 객체에게 아예 통짜로 넘겨버리자 (outImage로)
    photo2 = Image.fromarray(cvPhoto2)
    toColorOutArr(photo2)

def zoomInOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    # if inImage == None:
    #     return
    scale = askfloat("확대/축소", "배수: ")
    # 복사본 준비
    cvPhoto2 = cvPhoto[:]
    zoomIn_matrix = cv2.resize(cvPhoto2,None,fx=scale,fy=scale)

    # PILLOW 객체에게 아예 통짜로 넘겨버리자 (outImage로)
    photo2 = Image.fromarray(zoomIn_matrix)
    toColorOutArr(photo2)

def waveHorOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    # if inImage == None:
    #     return
    # 복사본 준비
    cvPhoto2 = np.zeros(cvPhoto.shape, dtype=cvPhoto.dtype)
    for i in range(inH):
        for k in range(inW):
            oy = int(15.0 * math.sin(2*3.14*k / 180))
            ox = 0
            if i+oy < inH:
                cvPhoto2[i][k] = cvPhoto[(i+oy) % inH][k]
            else:
                cvPhoto2[i][k] = 0

    # PILLOW 객체에게 아예 통짜로 넘겨버리자 (outImage로)
    photo2 = Image.fromarray(cvPhoto2)
    toColorOutArr(photo2)

def waveVirOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    # if inImage == None:
    #     return
    # 복사본 준비
    cvPhoto2 = np.zeros(cvPhoto.shape, dtype=cvPhoto.dtype)
    for i in range(inH):
        for k in range(inW):
            oy = 0
            ox = int(15.0 * math.sin(2*3.14*i / 180))
            if k+ox < inW:
                cvPhoto2[i][k] = cvPhoto[i][(k+ox) % inW]
            else:
                cvPhoto2[i][k] = 0


    # PILLOW 객체에게 아예 통짜로 넘겨버리자 (outImage로)
    photo2 = Image.fromarray(cvPhoto2)
    toColorOutArr(photo2)

def getClick():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto, pxy

def perspectiveOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto, ClickYN
    # if inImage == None:
    #     return

    pxy = [[0,0] for _ in range(4)]

    spoint = np.float32([[0,0],[inH,0],[0,inW],[inH,inW]])
    epoint = np.float32(pxy)

    # 복사본 준비
    cvPhoto2 = cvPhoto[:]

    # PILLOW 객체에게 아예 통짜로 넘겨버리자 (outImage로)
    photo2 = Image.fromarray(cvPhoto2)
    toColorOutArr(photo2)

def cartoonOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    # if inImage == None:
    #     return
    # 복사본 준비
    cvPhoto2 = cvPhoto[:]
    cvPhoto2 = cv2.cvtColor(cvPhoto2, cv2.COLOR_RGB2GRAY)
    cvPhoto2 = cv2.medianBlur(cvPhoto2,7)
    edges = cv2.Laplacian(cvPhoto2, cv2.CV_8U, ksize=5)
    ret, mask = cv2.threshold(edges, 100, 255, cv2.THRESH_BINARY_INV)
    cvPhoto2 = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)

    # PILLOW 객체에게 아예 통짜로 넘겨버리자 (outImage로)
    photo2 = Image.fromarray(cvPhoto2)
    toColorOutArr(photo2)
import cv2
def faceDetectOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    # if inImage == None:
    #     return
    # 복사본 준비
    cvPhoto2 = cvPhoto[:]
    grey = cv2.cvtColor(cvPhoto2, cv2.COLOR_RGB2GRAY)
    face_cascade = cv2.CascadeClassifier("C:\\Users\\user\\Desktop\\lecture_dir\\part3-python\\Bigdata\\haar\\haarcascade_frontalface_alt.xml")

    #얼굴 찾기
    face_rects = face_cascade.detectMultiScale(grey, 1.1, 5)
    print(face_rects)
    for (x, y, w, h) in face_rects:
        cv2.rectangle(cvPhoto2, (x, y), (x + w, y + w), (0, 255, 0), 3)

    # PILLOW 객체에게 아예 통짜로 넘겨버리자 (outImage로)
    photo2 = Image.fromarray(cvPhoto2)
    toColorOutArr(photo2)

def hanibalDetectOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    # if inImage == None:
    #     return
    # 복사본 준비
    cvPhoto2 = cvPhoto[:]
    grey = cv2.cvtColor(cvPhoto2, cv2.COLOR_RGB2GRAY)
    face_cascade = cv2.CascadeClassifier("C:\\Users\\user\\Desktop\\lecture_dir\\part3-python\\Bigdata\\haar\\haarcascade_frontalface_alt.xml")
    faceMask = cv2.imread("C:\\images\\images(ML)\\mask_hannibal.png") # ndarry네
    h_mask, w_mask = faceMask.shape[:2]

    # 얼굴 찾기
    # 얼굴 찾은 후 거기다가
    face_rects = face_cascade.detectMultiScale(grey, 1.1, 5)
    print(face_rects)
    for (x, y, w, h) in face_rects:
        if h > 0 and w > 0:
            x = int(x + 0.1*w); y = int(y + 0.4*h)
            w = int(0.4*w); h = int(0.4*h)
            cvPhoto2_2 = cvPhoto2[y:y+h, x:x+w] # 찾은 부분을 2_2로 저장
            faceMask_small = cv2.resize(faceMask, (w,h), interpolation=cv2.INTER_AREA) # interpolation : 보간법
            grey_mask = cv2.cvtColor(faceMask_small, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(grey_mask, 50, 255, cv2.THRESH_BINARY) # 임계점 : 50 넘기면 255로 적용 # 임계도 여러종류 있음 # ret은 실패성공 TF, 2번째 리턴이 mask
            mask_inv = cv2.bitwise_not(mask) # 반전하고
            maskedFace = cv2.bitwise_and(faceMask_small,faceMask_small,mask=mask) # mask의 값이 0이 아닌 부분만 src1과 src2를 and연산함
            maskedFrame = cv2.bitwise_and(cvPhoto2_2,cvPhoto2_2,mask_inv)
            cvPhoto2[y:y+h, x:x+h] = cv2.add(maskedFace,maskedFrame)

    # PILLOW 객체에게 아예 통짜로 넘겨버리자 (outImage로)
    photo2 = Image.fromarray(cvPhoto2)
    toColorOutArr(photo2)

def mustacheDetectOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    # if inImage == None:
    #     return
    # 복사본 준비
    cvPhoto2 = cvPhoto[:]
    grey = cv2.cvtColor(cvPhoto2, cv2.COLOR_RGB2GRAY)
    face_cascade = cv2.CascadeClassifier("C:\\Users\\user\\Desktop\\lecture_dir\\part3-python\\Bigdata\\haar\\haarcascade_frontalface_alt.xml")
    faceMask = cv2.imread("C:\\images\\images(ML)\\moustache.png") # ndarry네
    h_mask, w_mask = faceMask.shape[:2]


    # 얼굴 찾기
    # 얼굴 찾은 후 거기다가
    face_rects = face_cascade.detectMultiScale(grey, 1.1, 5)
    print(face_rects)
    for (x, y, w, h) in face_rects:
        if h > 0 and w > 0:
            x = int(x + 0.2*w); y = int(y + 0.6*h)
            w = int(0.6*w); h = int(0.2*h)
            cvPhoto2_2 = cvPhoto2[y:y+h, x:x+w] # 찾은 부분을 2_2로 저장
            faceMask_small = cv2.resize(faceMask, (w,h), interpolation=cv2.INTER_AREA) # interpolation : 보간법
            grey_mask = cv2.cvtColor(faceMask_small, cv2.COLOR_BGR2GRAY)
            # flag를 THRESH_BINARY_INV를 쓰면 반전되서 마스크가 생성됨 <흰-검> <검-흰>
            ret, mask = cv2.threshold(grey_mask, 30, 255, cv2.THRESH_BINARY_INV) # 임계점 : 50 넘기면 255로 적용 # 임계도 여러종류 있음 # ret은 실패성공 TF, 2번째 리턴이 mask
            mask_inv = cv2.bitwise_not(mask) # 반전하고
            masked_mouth = cv2.bitwise_and(faceMask_small, faceMask_small,mask=mask) # 콧수염 까망 + 나머지는 원래 0 (마스킹)
            masked_frame = cv2.bitwise_and(cvPhoto2_2,cvPhoto2_2,mask=mask_inv) # 콧수염 까망
            print(grey_mask)
            print("1s111111111111111111")
            print(mask)
            print("SDJKLFSDVNKL")
            print(mask_inv)
            cvPhoto2[y:y+h,x:x+w] = cv2.add(masked_mouth,masked_frame) # 합 : 콧수염 까망
            # bitwise는 자기자신을 val1,2 로 줬을 때 기준으로 mask가 0인 부분은 까망(0), 나머지는 and연산(살림)

    # PILLOW 객체에게 아예 통짜로 넘겨버리자 (outImage로)
    photo2 = Image.fromarray(cvPhoto2)
    toColorOutArr(photo2)

####################
#### 전역변수 선언부 ####
####################
R, G, B = 0, 1, 2 # 3차원으로 쉽게 다루려고 전역 상수 지정해줌
inImage, outImage = None, None # 이제 넘파이로 다룰래
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
window.title("컴퓨터 비전 (kang's) ver 0.1")

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
comVisionMenu1.add_separator()
comVisionMenu1.add_command(label="모핑", command=morphImageColor)
comVisionMenu1.add_separator()
comVisionMenu1.add_command(label="채도조절(Pillow)", command=addSvaluePillow)
comVisionMenu1.add_command(label="채도조절(HSV)", command=addSvalueHSV)


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

comVisionMenu5 = Menu(mainMenu)
mainMenu.add_cascade(label="기타 입출력", menu=comVisionMenu5)
comVisionMenu5.add_command(label="MySQL에서 불러오기", command=loadMysqlColor)
comVisionMenu5.add_command(label="MySQL에 저장하기", command=saveMysqlColor)
comVisionMenu5.add_separator()
comVisionMenu5.add_command(label="CSV 열기", command=openCSVColor)
comVisionMenu5.add_command(label="CSV로 저장", command=saveCSVColor)
comVisionMenu5.add_separator()
comVisionMenu5.add_command(label="Excel 열기", command=openExcelColor)
comVisionMenu5.add_command(label="Excel로 저장", command=saveExcelColor)
# comVisionMenu5.add_separator()
# comVisionMenu5.add_command(label="Excel art로 열기", command=openExcelArt)
# comVisionMenu5.add_command(label="Excel art로 저장", command=saveExcelArt)

openCVMenu = Menu(mainMenu)
mainMenu.add_cascade(label="OpenCv 딥러닝", menu=openCVMenu)
openCVMenu.add_command(label="엠보싱(OpenCV)", command=embossOpenCV)
openCVMenu.add_command(label="그레이스케일(OpenCV)", command=greyscaleOpenCV)
openCVMenu.add_command(label="블러링(OpenCV)", command=blurOpenCV)
openCVMenu.add_separator()
openCVMenu.add_command(label="회전", command=rotateOpenCV)
openCVMenu.add_command(label="확대", command=zoomInOpenCV)
openCVMenu.add_separator()
openCVMenu.add_command(label="수평 웨이브", command=waveHorOpenCV)
openCVMenu.add_command(label="수직 웨이브", command=waveVirOpenCV)
# openCVMenu.add_command(label="그림 펼치기", command=perspectiveOpenCV)
openCVMenu.add_command(label="카툰화", command=cartoonOpenCV)
openCVMenu.add_separator()
openCVMenu.add_command(label="얼굴인식(머신러닝)", command=faceDetectOpenCV)
openCVMenu.add_command(label="한니발 마스크(머신러닝)", command=hanibalDetectOpenCV)
openCVMenu.add_command(label="콧수염(머신러닝)", command=mustacheDetectOpenCV)

window.mainloop()