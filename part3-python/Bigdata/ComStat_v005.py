from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import numpy as np
import time
import psutil
import time
import random
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

####################
#### 함수 선언부 ####
####################

def staticIndicators():
    global canvas
    if not canvas == None:
        canvas.destroy()
    canvas = Canvas(window, height=VIEW_X, width=VIEW_Y-200)
    cpuCount = Label(canvas, text="CPUCount " + str(psutil.cpu_count()))
    cpuStats = Label(canvas, text="CPUStats " + str(psutil.cpu_stats()))
    netIfAddr = Label(canvas, text="Network Interface card: " + str(psutil.net_if_addrs()))
    cpuCount.pack()
    cpuStats.pack()
    netIfAddr.pack()
    canvas.pack()

def dynamicIndicators():
    global canvas
    if not canvas == None:
        canvas.destroy()
    canvas = Canvas(window, height=VIEW_X, width=VIEW_Y-200)
    cpu = Label(canvas, text="CPU: " + str(psutil.cpu_percent()))
    cpuTime = Label(canvas, text="CPUTime: " + str(psutil.cpu_times()))
    cpuStats = Label(canvas, text="CPUStats " + str(psutil.cpu_stats()))
    getLodaAvg = Label(canvas, text="getLoadAvg " + str(psutil.getloadavg()))
    cpu2 = Label(canvas, text="CPU_specific: " + str(psutil.cpu_times_percent()))
    disk = Label(canvas, text='DISK : ' + str(psutil.disk_usage('/').percent))
    ram = Label(canvas, text="RAM :" + str(psutil.virtual_memory().percent))

    cpu.pack(side=TOP, fill=X)
    cpuTime.pack()
    cpuStats.pack()
    getLodaAvg.pack()
    cpu2.pack(side=TOP, fill=X)
    ram.pack(side=TOP, fill=X)
    disk.pack(side=TOP, fill=X)
    # canvas.pack()

    fig = plt.Figure()

    x = np.arange(0, 2 * np.pi, 0.01)  # x-array

    graphCanvas = FigureCanvasTkAgg(fig, master=canvas)
    graphCanvas.draw()
    graphCanvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    ax = fig.add_subplot(111)
    line, = ax.plot(x, np.sin(x))
    ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), interval=25, blit=False)



    # 시간을 X축으로
    nowTime = [time.time()]

    # 각 값을 Y축으로
    cpuTimeInd = psutil.cpu_times()
    cpuList = [[cpuTimeInd.user], [cpuTimeInd.system], [cpuTimeInd.idle], [cpuTimeInd.interrupt]]
    fig = plt.figure(figsize=(16,8))
    plt.title("In & Out RGB")
    hist1 = fig.add_subplot(2, 1, 1)
    hist2 = fig.add_subplot(2, 1, 2)
    hist1.plot(nowTime,cpuList[0],'ro-',label='cpuTime_user')
    hist1.plot(nowTime,cpuList[1],'go-',label='cpuTime_system')
    hist1.plot(nowTime,cpuList[2],'bo-',label='cpuTime_idle')
    hist1.plot(nowTime, cpuList[3],'yo-', label='cpuTime_interrupt')
    fig.legend(loc='upper left')
    # plt.show()

    canvas.pack()

    def refreshHWIndicators():  # 1초마다 바뀌는 내용 수정
        try:
            timer = threading.Timer(1, refreshHWIndicators)
            cpu.configure(text="CPU: " + str(psutil.cpu_percent()))
            cpu2.configure(text="CPU_specific " + str(psutil.cpu_times_percent()))
            ram.configure(text="RAM :" + str(psutil.virtual_memory().percent))
            disk.configure(text='DISK : ' + str(psutil.disk_usage('/').percent))
            cpuTime.configure(text="CPUTime: " + str(psutil.cpu_times()))
            nowTime.append(time.time())
            cpuList[0].append(cpuTimeInd.user)
            cpuList[1].append(cpuTimeInd.system)
            cpuList[2].append(cpuTimeInd.idle)
            cpuList[3].append(cpuTimeInd.interrupt)

            hist1.plot(nowTime, cpuList[0], 'ro-', label='cpuTime_user')
            hist1.plot(nowTime, cpuList[1], 'go-', label='cpuTime_system')
            hist1.plot(nowTime, cpuList[2], 'bo-', label='cpuTime_idle')
            hist1.plot(nowTime, cpuList[3], 'yo-', label='cpuTime_interrupt')
            fig.legend(loc='upper left')
            # plt.show()
            timer.start()
        except:
            pass
    refreshHWIndicators()
    # plt.show()

# def refreshHWIndicators(): # 1초마다 바뀌는 내용 수정
#     timer = threading.Timer(1,refreshHWIndicators)
#     cpu.configure(text="CPU: " + str(psutil.cpu_percent()))
#     cpu2.configure(text="CPU_specific "+ str(psutil.cpu_times_percent()))
#     ram.configure(text="RAM :" + str(psutil.virtual_memory().percent))
#     disk.configure(text='DISK : ' + str(psutil.disk_usage('/').percent))
#     cpuTime.configure(text="CPUTime: "+str(psutil.cpu_times()))
#     timer.start()

def animate(i):
    line.set_ydata(np.sin(x+i/10.0))  # update the data
    return line,


####################
#### 전역변수 선언부 ####
####################
R, G, B = 0, 1, 2 # 3차원으로 쉽게 다루려고 전역 상수 지정해줌
inImage, outImage = None, None # 이제 넘파이로 다룰래
inH, inW, outH, outW = [0] * 4
window, canvas, paper = None, None, None
filename = ""
# panYN = False
sx, sy, ex, ey = [0] * 4
VIEW_X, VIEW_Y = 512, 512  # 화면에 보일 크기 (출력용)

####################
#### 메인 코드부 ####
####################
window = Tk()
window.geometry("1000x500")
window.title("Comstat v0.05")

buttonStatic = tkinter.Button(window, text='정적 지표', overrelief="solid", width=15, command=staticIndicators, repeatdelay=1000, repeatinterval=100)
buttonStatic.pack(side='right')
buttonDynamic = tkinter.Button(window, text='동적 지표', overrelief="solid", width=15, command=dynamicIndicators, repeatdelay=1000, repeatinterval=100)
buttonDynamic.pack(side='right')

# fig = plt.Figure()
#
# x = np.arange(0, 2*np.pi, 0.01)        # x-array
#
# graphCanvas = FigureCanvasTkAgg(fig, master=window)
# graphCanvas.get_tk_widget().grid(column=0,row=1)
#
# ax = fig.add_subplot(111)
# line, = ax.plot(x, np.sin(x))
# ani = animation.FuncAnimation(fig,animate, np.arange(1,200), interval=25, blit=False)

# cpu = Label(window, text="CPU: "+str(psutil.cpu_percent()))
# cpuTime = Label(window, text="CPUTime: "+str(psutil.cpu_times()))
# cpuStats = Label(window, text="CPUStats "+str(psutil.cpu_stats()))
# getLodaAvg = Label(window, text="getLoadAvg "+str(psutil.getloadavg()))
# cpu2 = Label(window, text="CPU_specific: "+str(psutil.cpu_times_percent()))
# disk = Label(window, text='DISK : '+str(psutil.disk_usage('/').percent))
# ram = Label(window, text="RAM :"+str(psutil.virtual_memory().percent))
#
# cpu.pack(side=TOP,fill=X)
# cpuTime.pack()
# cpuStats.pack()
# getLodaAvg.pack()
# cpu2.pack(side=TOP,fill=X)
# ram.pack(side=TOP,fill=X)
# disk.pack(side=TOP,fill=X)


status = Label(window, text='이미지 정보:', bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

# refreshHWIndicators()

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu)
# fileMenu.add_command(label="파일 열기", command=openImageColor)
# fileMenu.add_separator()
# fileMenu.add_command(label="파일 저장", command=saveImageColor)
#
# comVisionMenu1 = Menu(mainMenu)
# mainMenu.add_cascade(label="화소점 처리", menu=comVisionMenu1)
# comVisionMenu1.add_command(label="덧셈/뺄셈", command=addImageColor)
# comVisionMenu1.add_command(label="반전하기", command=revImageColor)

window.mainloop()