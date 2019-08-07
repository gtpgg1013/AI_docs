from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import numpy as np
import time
from sklearn import svm, metrics, neural_network, neighbors, gaussian_process, \
    tree, ensemble, naive_bayes, discriminant_analysis
import pandas as pd
import math
import cv2


def malloc(h, w, initValue=0, layers=1, dataType=np.uint8):
    retMemory = np.zeros((h, w, layers), dtype=dataType)
    retMemory += initValue
    return retMemory


def changeValue(lst):
    return [math.ceil(float(v) / 255) for v in lst]

import os.path
import joblib


def studyCKPT():
    global csv, train_data, train_label, test_data, test_label, clf
    global inImage, outImage, inH, inW, outH, outW, window, canvas, paper

    # filename = askopenfilename(parent=window,
    #                            filetypes=(("ckpt 파일", "*.ckpt"), ("모든 파일", "*.*")))
    # if filename == None or filename == "":
    #     return
    clf = "./tensorflow_mnist_saved_ckpt/model_mnist_cnn.ckpt"
    status.configure(text=clf + " 파일 로딩 성공")
    statusMLName.configure(text="현재 사용중인 모델 : " + clf)


# 이제는 캔버스에 그리기
def predictMouse():
    global csv, train_data, train_label, test_data, test_label, clf
    global inImage, outImage, inH, inW, outH, outW, window, canvas, paper

    if canvas != None:  # 예전에 실행한 적이 있다.
        canvas.destroy()

    inImage = malloc(280, 280)

    if clf == None:
        status.configure(text='모델을 먼저 생성해야 합니다.')
        return

    VIEW_X, VIEW_Y = 280, 280
    canvas = Canvas(window, height=VIEW_X, width=VIEW_Y, bg='black')  # 글자가 까마니깐
    canvas.create_image((VIEW_Y // 2, VIEW_X // 2), image=paper, state='normal')

    canvas.pack(expand=1, anchor=CENTER)
    status.configure(text='')

    # 이벤트 바인드
    canvas.bind('<Button-3>', rightMouseClick)
    canvas.bind('<Button-2>', midMouseClick)
    canvas.bind('<Button-1>', leftMouseClick)
    canvas.bind('<B1-Motion>', leftMouseMove)  # rubber band 만들장
    canvas.bind('<ButtonRelease-1>', leftMouseDrop)
    canvas.configure(cursor='plus')


def rightMouseClick(event):
    global csv, train_data, train_label, test_data, test_label, clf
    global inImage, outImage, inH, inW, outH, outW, window, canvas, paper

    # print("filename : ", filename)
    inH, inW = 280, 280;
    outH, outW = 28, 28
    # inImage = malloc(inH,inW)
    # for i in range(inH):
    #     for k in range(inW):
    #         pixel = paper.get(k,i) # (r,g,b)
    #         if pixel[0] == 0:
    #             inImage[i,k] = 0
    #         else :
    #             inImage[i,k] = 1

    outImage = malloc(outH, outW)
    # 280 --> 28 축소
    scale = 10
    for i in range(outH):
        for k in range(outW):
            fromY = i * scale;
            toY = fromY + scale;
            fromX = k * scale;
            toX = fromX + scale
            outImage[i, k] = inImage[fromY:toY, fromX:toX].mean()

    # mydata reshape
    my_data = outImage.reshape(-1,28*28)

    # print(my_data.shape)
    # print(type(my_data))
    # print(my_data)

    ################################################################
    #####################tensorflow model 부분######################
    ################################################################

    #####################상수 선언 부분#############################
    import tensorflow as tf

    learning_rate = 0.001
    training_epochs = 250
    batch_size = 128

    #####################모델 설정 부분#############################

    tf.reset_default_graph()

    x = tf.placeholder(tf.float32, [None, 28 * 28])
    ximg = tf.reshape(x, [-1, 28, 28, 1])  # img batch*28*28*1(black/white)
    # input(ximg) : batch , in_height, in_width, in_channels
    y = tf.placeholder(tf.float32, [None, 10])

    keep_prob = tf.placeholder(tf.float32)
    keep_prob_flatten = tf.placeholder(tf.float32)

    w1 = tf.Variable(tf.random_normal([2, 2, 1, 32]))
    # filter(w) : filter_height, filter_width, in_channels, out_channels 형식으로 준비
    L1 = tf.nn.conv2d(ximg, w1, strides=[1, 1, 1, 1], padding='SAME')
    # 양 끝은 고정, 가운데 두개만 상하,좌우 / SAME 하면 같은 크기
    # 요 conv2d를 하고 나면 batch * height * width * filter의 Tensor가 return됨
    L1 = tf.nn.relu(L1)
    # w1_1 = tf.Variable(tf.random_normal([2,2,32,32]))
    # L1_1 = tf.nn.conv2d(L1, w1, strides=[1,1,1,1], padding='SAME')
    # L1_1 = tf.nn.relu(L1_1)
    L1_1 = tf.nn.max_pool(L1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")
    L1_1 = tf.nn.dropout(L1_1, keep_prob=keep_prob)
    # L1 이미지 shape => (?, 28, 28, 1)
    # conv => (?,28,28,32)
    # relu => (?, 28, 28, 32)
    # pooling => (?, 14, 14, 32)

    w2 = tf.Variable(tf.random_normal([3, 3, 32, 64]))
    L2 = tf.nn.conv2d(L1_1, w2, strides=[1, 1, 1, 1], padding='SAME')
    L2 = tf.nn.relu(L2)
    # w2_1 = tf.Variable(tf.random_normal([3,3,64,64]))
    # L2_1 = tf.nn.conv2d(L2, w2_1, strides=[1,1,1,1], padding='SAME')
    # L2_1 = tf.nn.relu(L2_1)
    L2_1 = tf.nn.max_pool(L2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")
    L2_1 = tf.nn.dropout(L2_1, keep_prob=keep_prob)

    # L2 이미지 shape => (?, 14, 14, 32)
    # conv => (?,14,14,64)
    # relu => (?, 14, 14, 64)
    # pooling => (?, 7, 7, 64)
    # reshape => (?, 7*7*64)

    w3 = tf.Variable(tf.random_normal([3, 3, 64, 128]))
    L3 = tf.nn.conv2d(L2_1, w3, strides=[1, 1, 1, 1], padding='SAME')
    L3 = tf.nn.relu(L3)
    # w3_1 = tf.Variable(tf.random_normal([3,3,128,128]))
    # L3_1 = tf.nn.conv2d(L3, w3_1, strides=[1,1,1,1], padding='SAME')
    # L3_1 = tf.nn.relu(L3_1)
    L3_1 = tf.nn.max_pool(L3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")
    L3_1 = tf.nn.dropout(L3_1, keep_prob=keep_prob)

    L3_flat = tf.reshape(L3_1, [-1, 4 * 4 * 128])

    w4 = tf.get_variable("w4", shape=[4 * 4 * 128, 625], initializer=tf.contrib.layers.xavier_initializer())
    b1 = tf.Variable(tf.random_normal([625]))
    L4 = tf.matmul(L3_flat, w4) + b1
    L4 = tf.nn.dropout(L4, keep_prob=keep_prob_flatten)

    w5 = tf.get_variable("w5", shape=[625, 10], initializer=tf.contrib.layers.xavier_initializer())
    b2 = tf.Variable(tf.random_normal([10]))
    logits = tf.matmul(L4, w5) + b2
    logits = tf.nn.dropout(logits, keep_prob=keep_prob_flatten)

    prediction = tf.argmax(logits, 1)
    c_pre = tf.equal(tf.argmax(logits, 1), tf.argmax(y, 1))
    acc = tf.reduce_mean(tf.cast(c_pre, tf.float32))

    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=y, logits=logits))
    train = tf.train.RMSPropOptimizer(learning_rate, 0.9).minimize(cost)

    #####################세션 부분#############################

    # print("filename : ", clf)
    # print(my_data)

    saver = tf.train.Saver()
    predict = None

    # from tensorflow.examples.tutorials.mnist import input_data
    # mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

    with tf.Session() as sess:
        saver.restore(sess, clf)

        # print("final_acc: {}".format(
        #     sess.run(acc, feed_dict={x: mnist.test.images, y: mnist.test.labels, keep_prob: 1, keep_prob_flatten: 1})))
        predict = sess.run(prediction, feed_dict={x:my_data, keep_prob: 1, keep_prob_flatten: 1})

    ################################################################
    #####################tensorflow model 부분######################
    ################################################################

    status.configure(text="예측 숫자: " + str(predict[0]))


def midMouseClick(event):
    global csv, train_data, train_label, test_data, test_label, clf
    global inImage, outImage, inH, inW, outH, outW, window, canvas, paper
    global leftMousePressYN
    import numpy
    canvas.delete('all')
    inImage = malloc(280, 280)

    canvas.pack(expand=1, anchor=CENTER)
    status.configure(text='이미지 정보:' + str(outW) + 'x' + str(outH))


    leftMousePressYN = False


def leftMouseClick(event):
    global leftMousePressYN
    leftMousePressYN = True


def leftMouseMove(event):
    global leftMousePressYN
    global csv, train_data, train_label, test_data, test_label, clf
    global inImage, outImage, inH, inW, outH, outW, window, canvas, paper
    if leftMousePressYN == FALSE:
        return
    x = event.x;
    y = event.y
    canvas.create_rectangle(x - 10, y - 10, x + 10, y + 10, width=0, fill='white')
    # 주위 20x20개를 찍는다
    for i in range(-10, 10, 1):  # 값의 중앙에서 찍히는게 좋으니까
        for k in range(-10, 10, 1):
            if 0 <= x + i < 280 and 0 <= y + k < 280:
                inImage[y + k][x + i] = 1  # 이렇게 하면 이제 inImage에 바로 그리는 거에 따라서 찍히지! 클릭 순간순간마다 사각형으로 찍히는거네?


def leftMouseDrop(event):
    global leftMousePressYN
    leftMousePressYN = False


def displayImageML():
    global csv, train_data, train_label, test_data, test_label, clf
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if canvas != None:  # 예전에 실행한 적이 있다.
        canvas.destroy()
    global VIEW_X, VIEW_Y
    # VIEW_X, VIEW_Y = 512, 512
    ## 고정된 화면 크기
    # 가로/세로 비율 계산

    if inW <= 512 and inH <= 512:  # 정방형 관계없이 둘다 512보다 작으면 그냥 사용
        VIEW_X = inH
        VIEW_Y = inW
    else:  # 한쪽이라도 512보다 크면
        ratio = inH / inW
        if ratio < 1:
            VIEW_X = int(512 * ratio)
            if inW > 512:
                VIEW_Y = 512
            else:
                VIEW_Y = inW
        elif ratio > 1:
            ratio = 1 / ratio
            if inH > 512:
                VIEW_X = 512
            else:
                VIEW_X = inH
            VIEW_Y = int(512 * ratio)
        else:
            if inH > 512:
                VIEW_X = 512
            else:
                VIEW_X = inH
            if inW > 512:
                VIEW_Y = 512
            else:
                VIEW_Y = inW

    if outH <= VIEW_X:
        stepX = 1
    if outH > VIEW_X:
        stepX = outH / VIEW_X

    if outW <= VIEW_Y:
        stepY = 1
    if outW > VIEW_Y:
        stepY = outW / VIEW_Y

    print(VIEW_X, VIEW_Y, stepX, stepY)

    window.geometry(str(int(VIEW_Y * 1.2)) + 'x' + str(int(VIEW_X * 1.2)))  # 벽
    canvas = Canvas(window, height=VIEW_X, width=VIEW_Y)
    paper = PhotoImage(height=VIEW_X, width=VIEW_Y)
    canvas.create_image((VIEW_Y // 2, VIEW_X // 2), image=paper, state='normal')

    import numpy
    rgbStr = ''  # 전체 픽셀의 문자열을 저장
    for i in numpy.arange(0, outH, stepX):
        tmpStr = ''
        for k in numpy.arange(0, outW, stepY):
            i = int(i);
            k = int(k)
            r, g, b = outImage[i, k, R], outImage[i, k, G], outImage[i, k, B]
            tmpStr += ' #%02x%02x%02x' % (r, g, b)
        rgbStr += '{' + tmpStr + '} '
    paper.put(rgbStr)

    canvas.pack(expand=1, anchor=CENTER)
    status.configure(text='이미지 정보:' + str(outW) + 'x' + str(outH))


def loadImageML(fname):
    global csv, train_data, train_label, test_data, test_label, clf
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    photo = Image.open(fname)
    inW, inH = photo.size  # (photo.width, photo.height)
    inImage = np.array(photo)


def openImageML():
    global csv, train_data, train_label, test_data, test_label, clf
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    filename = askopenfilename(parent=window,
                               filetypes=(("칼라 파일", "*.jpg;*.png;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if filename == None or filename == '':
        return
    if canvas != None:  # 예전에 실행한 적이 있다.
        canvas.destroy()

    loadImageML(filename)
    equalImageML()
    displayImageML()

    canvas.bind('<Button-3>', rightMouseClick)
    canvas.bind('<Button-2>', midMouseClick)
    canvas.bind('<Button-1>', leftMouseClick)
    canvas.bind('<B1-Motion>', leftMouseMove)  # rubber band 만들장
    canvas.bind('<ButtonRelease-1>', leftMouseDrop)
    canvas.configure(cursor='plus')


def equalImageML():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;
    outW = inW;
    # outImage = ImageEnhance._Enhance(inImage)
    # print(inImage)
    # print(inImage.shape)
    # print(outImage)
    outImage = inImage.copy()


####################
#### 전역변수 선언부 ####
####################
R, G, B = 0, 1, 2  # 3차원으로 쉽게 다루려고 전역 상수 지정해줌
inImage, outImage = None, None  # 이제 넘파이로 다룰래
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
window.title("텐서플로 (MNIST) ver 0.01")

status = Label(window, text='', bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)
statusMLName = Label(window, text='', bd=1, relief=SUNKEN, anchor=W)
statusMLName.pack(side=BOTTOM, fill=X)

## 마우스 이벤트
mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="학습시키기", menu=fileMenu)
fileMenu.add_command(label="학습된 텐서플로 모델 가져오기", command=studyCKPT)

predictMenu = Menu(mainMenu)
mainMenu.add_cascade(label="예측하기", menu=predictMenu)
predictMenu.add_command(label="그림파일 불러오기", command=openImageML)
predictMenu.add_separator()
predictMenu.add_command(label="마우스로 직접 쓰기", command=predictMouse)

window.mainloop()