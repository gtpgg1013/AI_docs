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
    if canvas != None:  # 예전에 실행한 적이 있다.
        canvas.destroy()
    # 이건 걍 귀찮아서 안지운거
    VIEW_X = outW;
    VIEW_Y = outH;
    step = 1

    window.geometry(str(int(VIEW_Y * 1.2)) + 'x' + str(int(VIEW_X * 1.2)))  # 벽
    canvas = Canvas(window, height=VIEW_Y, width=VIEW_X)
    paper = PhotoImage(height=VIEW_Y, width=VIEW_X)
    canvas.create_image((VIEW_Y // 2, VIEW_X // 2), image=paper, state='normal')

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

    # canvas.bind('<Button-1>', mouseClick)
    # canvas.bind('<ButtonRelease-1>', mouseDrop)
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
    outImage = inImage.copy()
    outImage = ImageOps.invert(outImage)

    displayImageColor()


# 이진화 알고리즘
def bwImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    tmpoutImage = inImage.copy().convert("LA")
    outH = tmpoutImage.size[0]
    outW = tmpoutImage.size[1]
    outImage = Image.new("1", (outH, outW))  # 걍 new 이미지
    print(type(tmpoutImage))
    img_numpy = np.array(inImage.copy().convert("L"), 'uint8')  # convert를 LA로 안하고 L로 하면 np 배열로 구할 수 있음
    ## 영상의 평균 구하기.
    # sum = 0
    sum = img_numpy.sum()
    # for i in range(outH) :
    #     for k in range(outH) :
    #         sum += img_numpy[i][k]
    avg = sum // (inW * inH)
    print(img_numpy)
    print(img_numpy.ndim)
    print(avg)
    img_numpy = np.where(img_numpy >= avg, 1,
                         np.where(img_numpy < avg, 0, img_numpy))

    for i in range(1, inH):
        for k in range(1, inW):
            outImage.putpixel((i, k), int(img_numpy[k, i]))  # 왜 이걸 반대로 해야지 되는가?

    outImage = outImage.convert('RGB')

    displayImageColor()


# 파라볼라 알고리즘
def parabolaImageColor(param):
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global startTime
    startTime = time.time()
    # LookUpTable 기법 활용
    outImage = inImage.copy()
    (outH, outW) = outImage.size

    LUT = np.array([i for i in range(256)])  # 색깔 LUT 만들기 : LUT[]에 인덱스로 걍 때려넣으면 되네....?
    if param == 1:
        LUT = 255 - 255 * np.power((LUT / 128) - 1, 2)
        for i in range(0, inH):
            for k in range(0, inW):
                tmptup = outImage.getpixel((k, i))
                outImage.putpixel((k, i), (int(LUT[tmptup[0]]), int(LUT[tmptup[1]]), int(LUT[tmptup[2]])))
    else:
        LUT = 255 * np.power((LUT / 128) - 1, 2)
        for i in range(0, inH):
            for k in range(0, inW):
                tmptup = outImage.getpixel((k, i))
                outImage.putpixel((k, i), (int(LUT[tmptup[0]]), int(LUT[tmptup[1]]), int(LUT[tmptup[2]])))

    displayImageColor()


# 상하/좌우반전 알고리즘
def banjunImageColor(param):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outImage = inImage.copy()
    (outH, outW) = outImage.size
    if param == 2:
        outImage = outImage.transpose(Image.FLIP_LEFT_RIGHT)
    else:
        outImage = outImage.transpose(Image.FLIP_TOP_BOTTOM)

    displayImageColor()


# 블러링
def blurImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outImage = inImage.copy()
    outImage = outImage.filter(ImageFilter.BLUR)
    outW = outImage.width
    outH = outImage.height

    displayImageColor()


import matplotlib.pyplot as plt


# 현재 흑백사진은 안됨 => 안되는 이유 파악해서 할 것
def histoImageColor():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    global startTime
    startTime = time.time()

    inW, inH = inImage.size
    outW, outH = outImage.size

    inImage_raw = inImage.load()
    outImage_raw = outImage.load()

    inRcountlist = [_ for _ in range(256)]
    inGcountlist = [_ for _ in range(256)]
    inBcountlist = [_ for _ in range(256)]
    outRcountlist = [_ for _ in range(256)]
    outGcountlist = [_ for _ in range(256)]
    outBcountlist = [_ for _ in range(256)]

    for i in range(inH):
        for k in range(inW):
            inRcountlist[inImage.getpixel((k, i))[0]] += 1
            inGcountlist[inImage.getpixel((k, i))[1]] += 1
            inBcountlist[inImage.getpixel((k, i))[2]] += 1

    for i in range(outH):
        for k in range(outW):
            outRcountlist[outImage.getpixel((k, i))[0]] += 1
            outGcountlist[outImage.getpixel((k, i))[1]] += 1
            outBcountlist[outImage.getpixel((k, i))[2]] += 1

    # status.configure(text='이미지 정보' + str(outW) + 'x' + str(outH) + "\t 시간(초)" + "{0:.2f}".format(endTime))
    # 좀만 있다가 해보자
    fig = plt.figure(figsize=(16, 8))
    hist1 = fig.add_subplot(2, 1, 1)
    hist2 = fig.add_subplot(2, 1, 2)
    hist1.plot(inRcountlist, label='inImage Red', color='Red')
    hist1.plot(inGcountlist, label='inImage Green', color='Green')
    hist1.plot(inBcountlist, label='inImage Blue', color='Blue')
    hist2.plot(outRcountlist, label='outImage Red', color='Red')
    hist2.plot(outGcountlist, label='outImage Green', color='Green')
    hist2.plot(outBcountlist, label='outImage Blue', color='Blue')
    fig.legend(loc='upper left')
    plt.show()


# 확대
def zoomInImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    value = askinteger("확대", "값(0~8)-->", minvalue=2, maxvalue=8)
    outImage = inImage.copy()
    outImage = outImage.resize((inH * value, inW * value))  # Image.open.resize의 인자는 tuple형식으로(H,W) 받음
    outW = outImage.width
    outH = outImage.height

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

window.mainloop()