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
def malloc(h, w) :
    retMemory = []
    for _ in range(h):
        for _ in range(w):
            retMemory.append(0)
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

    print(inH,outW)
    print(ord(inImage[100][100])) # ord는 이진문자 - 읽을 수 있는 문자로!

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
            paper.put("#%02x%02x%02x" % (r,g,b), (i,k)) # 16진수 문자열 포맷팅, i,k로 위치 지정해주기

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
window.title("컴퓨터 비전(딥러닝 기법) ver 0.01")

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일",menu=fileMenu)
fileMenu.add_command(label="파일 열기",command=openImage)
fileMenu.add_command(label="파일 저장",command=saveImage)

comVisionMenu1 = Menu(mainMenu)
mainMenu.add_cascade(label="알고리즘A",menu=comVisionMenu1)
comVisionMenu1.add_command(label="알고리즘1",command=None)
comVisionMenu1.add_command(label="알고리즘2",command=None)
# editMenu.add_command(label="붙여넣기",command=lambda : messagebox.showinfo("안내","아직 미구현입니다."))

window.mainloop()