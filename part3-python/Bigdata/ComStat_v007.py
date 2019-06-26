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
    global canvas, canvasF, window, leftFrame, rightFrame
    if not canvas == None:
        canvas.destroy()
    if not canvasF == None:
        canvasF.destroy()

    fig = plt.Figure()

    x = np.arange(0, 2 * np.pi, 0.01)  # x-array

    def animate(i):
        line.set_ydata(np.sin(x + i / 10.0))  # update the data
        return line,

    label = Label(leftFrame, text="SHM Simulation")
    label.pack()

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().grid(column=0,row=1)

    ax = fig.add_subplot(111)
    line, = ax.plot(x, np.sin(x))

    ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), interval=25, blit=False)

    canvasF = Canvas(rightFrame, height=VIEW_X, width=300, relief='solid')
    netIfAddr = Label(canvasF, text="Network Interface card: " + str(psutil.net_if_addrs()))
    netIfAddr.pack()
    canvasF.pack(side=tkinter.LEFT, fill=X)

    print(type(canvas))
    print(type(canvasF))

def dynamicIndicators():
    global canvas, canvasF, window, leftFrame, rightFrame
    if not canvas == None:
        canvas.destroy()
    if not canvasF == None:
        canvasF.destroy()
    canvas = Canvas(leftFrame, height=VIEW_X, width=500, relief='solid')
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

    canvas.pack()

    def refreshHWIndicators():  # 1초마다 바뀌는 내용 수정
        try:
            timer = threading.Timer(1, refreshHWIndicators)
            cpu.configure(text="CPU: " + str(psutil.cpu_percent()))
            cpu2.configure(text="CPU_specific " + str(psutil.cpu_times_percent()))
            ram.configure(text="RAM :" + str(psutil.virtual_memory().percent))
            disk.configure(text='DISK : ' + str(psutil.disk_usage('/').percent))
            cpuTime.configure(text="CPUTime: " + str(psutil.cpu_times()))

            timer.start()
        except:
            pass
    refreshHWIndicators()
    print("0000000000000000")

# def refreshHWIndicators(): # 1초마다 바뀌는 내용 수정
#     timer = threading.Timer(1,refreshHWIndicators)
#     cpu.configure(text="CPU: " + str(psutil.cpu_percent()))
#     cpu2.configure(text="CPU_specific "+ str(psutil.cpu_times_percent()))
#     ram.configure(text="RAM :" + str(psutil.virtual_memory().percent))
#     disk.configure(text='DISK : ' + str(psutil.disk_usage('/').percent))
#     cpuTime.configure(text="CPUTime: "+str(psutil.cpu_times()))
#     timer.start()

# def animate(i):
#     line.set_ydata(np.sin(x+i/10.0))  # update the data
#     return line,


####################
#### 전역변수 선언부 ####
####################
R, G, B = 0, 1, 2 # 3차원으로 쉽게 다루려고 전역 상수 지정해줌
inImage, outImage = None, None # 이제 넘파이로 다룰래
inH, inW, outH, outW = [0] * 4
window, canvas, canvasF, paper = None, None, None, None
leftFrame, rightFrame = None, None
filename = ""
fig, animate = None, None
sx, sy, ex, ey = [0] * 4
VIEW_X, VIEW_Y = 512, 512  # 화면에 보일 크기 (출력용)

####################
#### 메인 코드부 ####
####################
window = Tk()
window.geometry("1350x512")
window.title("Comstat v0.05")

buttonStatic = tkinter.Button(window, text='정적 지표', overrelief="solid", width=15, command=staticIndicators, repeatdelay=1000, repeatinterval=100)
buttonStatic.pack(side='right')
buttonDynamic = tkinter.Button(window, text='동적 지표', overrelief="solid", width=15, command=dynamicIndicators, repeatdelay=1000, repeatinterval=100)
buttonDynamic.pack(side='right')

leftFrame = Frame(window, relief="solid", bd=2)
rightFrame = Frame(window, relief="solid", bd=2)
leftFrame.pack(side="left", fill="both",expand=True)
rightFrame.pack(side="right", fill="both",expand=True)
status = Label(window, text='이미지 정보:', bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

# refreshHWIndicators()

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu)

window.mainloop()