from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import numpy as np
import time
from sklearn import svm, metrics, neural_network, neighbors, gaussian_process,\
    tree, ensemble, naive_bayes, discriminant_analysis
import pandas as pd
import math

def malloc(h, w, initValue=0,layers = 1, dataType=np.uint8) :
    retMemory = np.zeros((h,w,layers),dtype=dataType)
    retMemory += initValue
    return retMemory

def changeValue(lst):
    return [math.ceil(float(v) / 255) for v in lst]

def studyCSV(param):
    global csv, train_data, train_label, test_data, test_label,clf
    global inImage, outImage, inH, inW, outH, outW, window, canvas, paper

    filename = askopenfilename(parent=window,
                               filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))
    if filename == None or filename == "":
        return

    ## 훈련데이터, 테스트데이터 준비
    csv = pd.read_csv(filename)
    train_data = csv.iloc[:, 1:].values  # 이렇게 해야 값이 들어오나(value 안붙이면 return이 DF)
    train_data = list(map(changeValue, train_data))  # 값이 0~1 범위를 0~255로 : map객체를 list화 시키기
    train_label = csv.iloc[:, 0].values

    # 1. Classifier 생성(선택) --> 머신러닝 알고리즘 선택
    if param == 'SVC':
        clf = svm.SVC(gamma='auto')
    elif param == 'nuSVC':
        clf = svm.NuSVC(gamma='auto')
    elif param == 'LSVC':
        clf = svm.SVC(kernel='linear', C=0.025)
    elif param == 'GaussianProcess':
        clf = gaussian_process.GaussianProcessClassifier(1.0*gaussian_process.kernels.RBF(1.0))
    elif param == 'DecisionTree':
        clf = tree.DecisionTreeClassifier(max_depth=5)
    elif param == 'RForest':
        clf = ensemble.RandomForestClassifier(max_depth=5,n_estimators=10,max_features=1)
    elif param == 'MLP':
        clf = neural_network.MLPClassifier(alpha=1,max_iter=1000)
    elif param == 'AdaBoost':
        clf = ensemble.AdaBoostClassifier()
    elif param == 'GaussianNB':
        clf = naive_bayes.GaussianNB()
    elif param == 'Quadratic':
        clf = discriminant_analysis.QuadraticDiscriminantAnalysis()

    # 2. 데이터로 학습시키기
    # clf.fit( [훈련데이터], [정답])
    clf.fit(train_data, train_label)
    status.configure(text= filename + " 파일 훈련 성공")

import os.path
import joblib
def studyDUMP():
    global csv, train_data, train_label, test_data, test_label, clf
    global inImage, outImage, inH, inW, outH, outW, window, canvas, paper

    filename = askopenfilename(parent=window,
                               filetypes=(("DUMP 파일", "*.dmp"), ("모든 파일", "*.*")))
    if filename == None or filename == "":
        return
    clf = joblib.load(filename)
    status.configure(text=filename + " 파일 로딩 성공")
    statusMLName.configure(text="현재 사용중인 모델 : "+os.path.basename(filename))

def studySave():
    global csv, train_data, train_label, test_data, test_label,clf
    global inImage, outImage, inH, inW, outH, outW, window, canvas, paper

    saveFp = asksaveasfile(parent=window, mode='wb', defaultextension='.',
                               filetypes=(("DUMP 파일", "*.dmp"), ("모든 파일", "*.*")))
    if saveFp == None or saveFp == "":
        return

    import joblib
    joblib.dump(clf, saveFp.name)
    status.configure(text=saveFp.name + " 파일 저장 성공")

def studyScore():
    global csv, train_data, train_label, test_data, test_label,clf
    global inImage, outImage, inH, inW, outH, outW, window, canvas, paper
    
    if clf == None:
        status.configure(text="모델을 먼저 로드해주세요")
        return

    filename = askopenfilename(parent=window,
                               filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))
    if filename == None or filename == "":
        return

    ## 훈련데이터, 테스트데이터 준비
    csv = pd.read_csv(filename)
    test_data = csv.iloc[:, 1:].values  # 이렇게 해야 값이 들어오나(value 안붙이면 return이 DF)
    test_data = list(map(changeValue, test_data))  # 값이 0~1 범위를 0~255로 : map객체를 list화 시키기
    test_label = csv.iloc[:, 0].values

    result = clf.predict(test_data)
    score = metrics.accuracy_score(result, test_label)

    status.configure(text="정답률: "+ "{0:.2f}".format(score*100)+"%")

# 이제는 캔버스에 그리기
def predictMouse():
    global csv, train_data, train_label, test_data, test_label,clf
    global inImage, outImage, inH, inW, outH, outW, window, canvas, paper

    if canvas != None : # 예전에 실행한 적이 있다.
        canvas.destroy()

    inImage = malloc(280,280)

    if clf == None:
        status.configure(text='모델을 먼저 생성해야 합니다.')
        return

    VIEW_X, VIEW_Y = 280, 280
    canvas = Canvas(window, height=VIEW_X, width=VIEW_Y, bg='black') # 글자가 까마니깐
    canvas.create_image((VIEW_Y // 2, VIEW_X // 2), image=paper, state='normal')

    canvas.pack(expand=1, anchor=CENTER)
    status.configure(text='')

    # 이벤트 바인드
    canvas.bind('<Button-3>', rightMouseClick)
    canvas.bind('<Button-2>', midMouseClick)
    canvas.bind('<Button-1>', leftMouseClick)
    canvas.bind('<B1-Motion>', leftMouseMove) # rubber band 만들장
    canvas.bind('<ButtonRelease-1>', leftMouseDrop)
    canvas.configure(cursor='plus')

def rightMouseClick(event):
    global csv, train_data, train_label, test_data, test_label,clf
    global inImage, outImage, inH, inW, outH, outW, window, canvas, paper
    inH, inW = 280, 280; outH, outW = 28, 28
    # inImage = malloc(inH,inW)
    # for i in range(inH):
    #     for k in range(inW):
    #         pixel = paper.get(k,i) # (r,g,b)
    #         if pixel[0] == 0:
    #             inImage[i,k] = 0
    #         else :
    #             inImage[i,k] = 1

    outImage = malloc(outH,outW)
    # 280 --> 28 축소
    scale = 10
    for i in range(outH):
        for k in range(outW):
            fromY = i*scale; toY = fromY+scale; fromX = k*scale; toX = fromX+scale
            outImage[i,k] = inImage[fromY:toY,fromX:toX].mean()

    # 2차원 --> 1차원
    my_data = outImage.flatten()
    # my_data = []
    # for i in range(28):
    #     for k in range(28):
    #         my_data.append(outImage[i,k])

    # # 출력해서 확인해보기
    # for i in range(28):
    #     for k in range(28):
    #         print("%2d" % my_data[i], end='')
    #         if i%28 == 0:
    #             print()
    # 예측하기
    result = clf.predict([my_data])
    status.configure(text="예측 숫자: "+ str(result[0]))

def midMouseClick(event):
    global csv, train_data, train_label, test_data, test_label,clf
    global inImage, outImage, inH, inW, outH, outW, window, canvas, paper
    import numpy
    canvas.delete('all')
    inImage = malloc(280,280)

    canvas.pack(expand=1, anchor=CENTER)
    status.configure(text='이미지 정보:' + str(outW) + 'x' + str(outH))


leftMousePressYN = False
def leftMouseClick(event):
    global leftMousePressYN
    leftMousePressYN = True

def leftMouseMove(event):
    global leftMousePressYN
    global csv, train_data, train_label, test_data, test_label,clf
    global inImage, outImage, inH, inW, outH, outW, window, canvas, paper
    if leftMousePressYN == FALSE:
        return
    x = event.x; y = event.y
    canvas.create_rectangle(x-10, y-10, x+10, y+10, width=0, fill='white')
    # 주위 20x20개를 찍는다
    for i in range(-10,10,1): # 값의 중앙에서 찍히는게 좋으니까
        for k in range(-10,10,1):
            if 0 <= x+i <280 and 0 <= y+k < 280:
                inImage[y+k][x+i] = 1 # 이렇게 하면 이제 inImage에 바로 그리는 거에 따라서 찍히지! 클릭 순간순간마다 사각형으로 찍히는거네?


def leftMouseDrop(event):
    global leftMousePressYN
    leftMousePressYN = False

def displayImageML() :
    global csv, train_data, train_label, test_data, test_label,clf
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if canvas != None : # 예전에 실행한 적이 있다.
        canvas.destroy()
    global VIEW_X, VIEW_Y
    # VIEW_X, VIEW_Y = 512, 512
    ## 고정된 화면 크기
    # 가로/세로 비율 계산

    if inW <= 512 and inH <= 512 : # 정방형 관계없이 둘다 512보다 작으면 그냥 사용
        VIEW_X = inH
        VIEW_Y = inW
    else : # 한쪽이라도 512보다 크면
        ratio = inH / inW
        if ratio < 1:
            VIEW_X = int(512 * ratio)
            if inW > 512 :
                VIEW_Y = 512
            else :
                VIEW_Y = inW
        elif ratio > 1:
            ratio = 1/ratio
            if inH > 512 :
                VIEW_X = 512
            else :
                VIEW_X = inH
            VIEW_Y = int(512 * ratio)
        else :
            if inH > 512:
                VIEW_X = 512
            else:
                VIEW_X = inH
            if inW > 512:
                VIEW_Y = 512
            else:
                VIEW_Y = inW

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
            r, g, b = outImage[i,k,R], outImage[i,k,G], outImage[i,k,B]
            tmpStr += ' #%02x%02x%02x' % (r,g,b)
        rgbStr += '{' + tmpStr + '} '
    paper.put(rgbStr)

    canvas.pack(expand=1, anchor=CENTER)
    status.configure(text='이미지 정보:' + str(outW) + 'x' + str(outH))

def loadImageML(fname):
    global csv, train_data, train_label, test_data, test_label,clf
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    photo = Image.open(fname)
    inW, inH = photo.size # (photo.width, photo.height)
    inImage =  np.array(photo)

def openImageML():
    global csv, train_data, train_label, test_data, test_label,clf
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    filename = askopenfilename(parent=window,
                               filetypes=(("칼라 파일", "*.jpg;*.png;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if filename == None or filename == '':
        return
    loadImageML(filename)
    equalImageML()
    displayImageML()

def  equalImageML() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    # outImage = ImageEnhance._Enhance(inImage)
    # print(inImage)
    # print(inImage.shape)
    # print(outImage)
    outImage = inImage.copy()

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

# 머신러닝 관련 전역변수
csv, train_data, train_label, test_data, test_label, clf = [None] * 6

####################
#### 메인 코드부 ####
####################
window = Tk()
window.geometry("500x500")
window.title("머신러닝 툴 (MNIST) ver 0.01")

status = Label(window, text='', bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)
statusMLName = Label(window, text='', bd=1, relief=SUNKEN, anchor=W)
statusMLName.pack(side=BOTTOM, fill=X)

## 마우스 이벤트
mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="학습시키기", menu=fileMenu)
fileMenu.add_command(label="CSV 파일로 SVC 모델 학습", command=lambda :studyCSV('SVC'))
fileMenu.add_command(label="CSV 파일로 nuSVC 모델 학습", command=lambda :studyCSV('nuSVC'))
fileMenu.add_command(label="CSV 파일로 Linear SVC 모델 학습", command=lambda :studyCSV('LSVC'))
fileMenu.add_command(label="CSV 파일로 가우시안 모델 학습", command=lambda :studyCSV('GaussianProcess'))
fileMenu.add_command(label="CSV 파일로 의사결정나무 모델 학습", command=lambda :studyCSV('DecisionTree'))
fileMenu.add_command(label="CSV 파일로 Random Forest 모델 학습", command=lambda :studyCSV('RForest'))
fileMenu.add_command(label="CSV 파일로 MLP 모델 학습", command=lambda :studyCSV('MLP'))
fileMenu.add_command(label="CSV 파일로 AdaBoost 모델 학습", command=lambda :studyCSV('AdaBoost'))
fileMenu.add_command(label="CSV 파일로 GaussianNB 모델 학습", command=lambda :studyCSV('GaussianNB'))
fileMenu.add_command(label="CSV 파일로 Quadratic 모델 학습", command=lambda :studyCSV('Quadratic'))

fileMenu.add_command(label="학습된 모델 가져오기", command=studyDUMP)
fileMenu.add_separator()
fileMenu.add_command(label="정답률 확인하기", command=studyScore)
fileMenu.add_separator()
fileMenu.add_command(label="학습모델 저장하기", command=studySave)

predictMenu = Menu(mainMenu)
mainMenu.add_cascade(label="예측하기", menu=predictMenu)
predictMenu.add_command(label="그림파일 불러오기", command=openImageML)
predictMenu.add_separator()
predictMenu.add_command(label="마우스로 직접 쓰기", command=predictMouse)

window.mainloop()