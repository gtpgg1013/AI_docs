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
def malloc(h, w) :
    retMemory = []
    for _ in range(h):
        templist = []
        for _ in range(w):
            templist.append(0)
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
    loadImage(filename)
    equalImage()

def saveImage():
    pass

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
    for i in range(outH):
        for k in range(outW):
            r = g = b = outImage[i][k]
            paper.put("#%02x%02x%02x" % (r,g,b), (k,i)) # 16진수 문자열 포맷팅, i,k로 위치 지정해주기

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
                outImage[i][k] = inImage[i][k] + value
                if outImage[i][k] > 255:
                    outImage[i][k] = 255
    else:
        value = askinteger("나누기", "나눌 값", minvalue=1, maxvalue=255)
        for i in range(inH):
            for k in range(inW):
                outImage[i][k] = inImage[i][k] - value
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

    maxpixel = 0
    minpixel = 255

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
    for i in range(inH):
        for k in range(inW):
            newk = int((k-centerw)*math.cos(value) - (i-centerh)*math.sin(value)) + centerw
            newi = int((k-centerw)*math.sin(value) + (i-centerh)*math.cos(value)) + centerh
            if newk >= 0 and newk < outH and newi >= 0 and newi < outW:
                outImage[newi][newk] = inImage[i][k]

    displayImage()

def shrinkImage():
    global window, canvas, paper, filename, outImage, inImage, inH, outH, inW, outW
    ## 중요코드 : 출력영상 크기 결정 ##
    outH = inH
    outW = inW
    # 메모리 할당 (틀만들기)
    outImage = []
    outImage = malloc(outH, outW)
    # 진짜 컴퓨터 비전 알고리즘
    value = askinteger("안내", "축소 배율을 입력해주세요")
    for i in range(inH):
        for k in range(inW):
            newi = int(i/value)
            newk = int(k/value)
            outImage[newi][newk] = inImage[i][k]

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
    for i in range(inH):
        for k in range(inW):
            newi = int(i * value)
            newk = int(k * value)
            outImage[newi][newk] = inImage[i][k]

    displayImage()

################################
#####   전역변수 선언부   ######
################################

inImage, outImage = [], [] ; inH, inW, outH, outW = [0] * 4
window, canvas, paper = None, None, None
filename = ""

################################
#######   메인 코드부   ########
################################

window = Tk()
window.geometry("400x400")
window.resizable(True, True)

mainMenu = Menu(window)
window.config(menu=mainMenu)
window.title("컴퓨터 비전(딥러닝 기법) ver 0.02")

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
comVisionMenu1.add_command(label="파라볼라 변환(캡)",command=lambda : parabolaImage(1))
comVisionMenu1.add_command(label="파라볼라 변환(컵)",command=lambda : parabolaImage(2))

comVisionMenu2 = Menu(mainMenu)
mainMenu.add_cascade(label="화소(통계)",menu=comVisionMenu2)
comVisionMenu2.add_command(label="이진화",command=biImage)

comVisionMenu3 = Menu(mainMenu)
mainMenu.add_cascade(label="기하학 처리",menu=comVisionMenu3)
comVisionMenu3.add_command(label="상하반전",command=updownImage)
moveMenu = Menu(comVisionMenu3)
comVisionMenu3.add_cascade(label="이동",menu=moveMenu)
moveMenu.add_command(label="아래로",command=lambda :moveImage(1))
moveMenu.add_command(label="위로",command=lambda :moveImage(2))
moveMenu.add_command(label="오른쪽",command=lambda :moveImage(3))
moveMenu.add_command(label="왼쪽",command=lambda :moveImage(4))
comVisionMenu3.add_command(label="회전",command=rotateImage)
comVisionMenu3.add_command(label="축소",command=shrinkImage)
comVisionMenu3.add_command(label="확대",command=zoomImage)


window.mainloop()