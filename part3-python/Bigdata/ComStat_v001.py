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


####################
#### 함수 선언부 ####
####################

# def getCPUTemperature():
#     result = os.popen('vcgencmd mesure_temp').readline()
#     return(result.replace("temp=","").replace("'C\n",""))

def refreshHWIndicators(): # 1초마다 바뀌는 내용 수정
    timer = threading.Timer(1,refreshHWIndicators)
    cpu.configure(text="CPU: " + str(psutil.cpu_percent()))
    cpu2.configure(text="CPU_specific "+ str(psutil.cpu_times_percent()))
    ram.configure(text="RAM :" + str(psutil.virtual_memory().percent))
    disk.configure(text='DISK : ' + str(psutil.disk_usage('/').percent))
    cpuTime.configure(text="CPUTime: "+str(psutil.cpu_times()))
    cpuCount.configure(text="CPUCount "+str(psutil.cpu_count()))
    cpuStats.configure(text="CPUStats "+str(psutil.cpu_stats()))
    cpuFreq.configure(text="CPUFreq "+str(psutil.cpu_freq()))
    getLodaAvg.configure(text="getLoadAvg "+str(psutil.getloadavg()))
    swapMemory.configure(text="swapMemory: " + str(psutil.swap_memory()))
    netIO.configure(text="Network IO: " + str(psutil.net_io_counters()))
    netConn.configure(text="Network Connection" + str(psutil.net_connections()))
    netIfAddr.configure(text="Network Interface card" + str(psutil.net_if_addrs()))
    # netIfStat.configure(ext="Network Interface status: " + str(psutil.net_if_stats()))
    # sensorTemp.configure(text="Sensors Temperatures: " + str(psutil.sensors_temperatures()))
    sensorFans.configure(text="Sensor Fans: " + str(psutil.sensors_battery()))
    bootTime.configure(text="Boot Time: " + str(psutil.boot_time()))
    pids.configure(text="Current Running on PIDs: " + str(psutil.pids()))

    # Process Class 이용
    p = psutil.Process()
    # ioNiceness.configure(text="I/O Niceness: high-" + str(p.ionice(psutil.IOPRIO_HIGH)) + " normal-" + str(
    #     p.ionice(psutil.IOPRIO_NORMAL)) \
    #                                 + " low-" + +str(p.ionice(psutil.IOPRIO_LOW)) + " very low-" + str(
    #     p.ionice(psutil.IOPRIO_VERYLOW)))
    ioCounters.configure(text="I/O Counters: " + str(p.io_counters()))
    numHandles.configure(text="Number of Handles: " + str(p.num_handles()))
    numthreads.configure(text="Number of Threads :" + str(p.num_threads()))
    memoryInfo.configure(text="Memory Information: " + str(p.memory_info()))
    memoryFullInfo.configure(text="Full Memory Info: " + str(p.memory_full_info()))
    memoryPercent.configure(text="Memory Percent: " + str(p.memory_percent()))
    memoryMaps.configure(text="Memory Maps: " + str(p.memory_maps()))
    connnections.configure(text="Connections: " + str(p.connections()))
    timer.start()


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
window.title("컴퓨터 비전 (kang's) ver 0.1")

cpu = Label(window, text="CPU: "+str(psutil.cpu_percent()))
cpuTime = Label(window, text="CPUTime: "+str(psutil.cpu_times()))
cpuCount = Label(window, text="CPUCount "+str(psutil.cpu_count()))
cpuStats = Label(window, text="CPUStats "+str(psutil.cpu_stats()))
cpuFreq = Label(window, text="CPUFreq "+str(psutil.cpu_freq()))
getLodaAvg = Label(window, text="getLoadAvg "+str(psutil.getloadavg()))
cpu2 = Label(window, text="CPU_specific: "+str(psutil.cpu_times_percent()))
ram = Label(window, text="RAM :"+str(psutil.virtual_memory().percent))
swapMemory = Label(window, text="swapMemory: "+str(psutil.swap_memory()))
disk = Label(window, text='DISK : '+str(psutil.disk_usage('/').percent))
hard = Label(window, text='HARD: '+str(psutil.disk_io_counters()))
netIO = Label(window, text="Network IO: "+str(psutil.net_io_counters()))
netConn = Label(window, text="Network Connection: "+ str(psutil.net_connections()))
netIfAddr = Label(window, text="Network Interface card: "+ str(psutil.net_if_addrs()))
netIfStat = Label(window, text="Network Interface status: "+ str(psutil.net_if_stats()))
sensorFans = Label(window,text="Sensor Fans: "+str(psutil.sensors_battery()))
bootTime = Label(window,text="Boot Time: "+str(psutil.boot_time()))
pids = Label(window, text="Current Running on PIDs: "+str(psutil.pids()))

# Process Class 이용
p = psutil.Process()
# ioNiceness = Label(window,text="I/O Niceness: high-"+str(p.ionice(psutil.IOPRIO_HIGH))+" normal-"+str(p.ionice(psutil.IOPRIO_NORMAL))\
#                    +" low-"++str(p.ionice(psutil.IOPRIO_LOW))+" very low-"+str(p.ionice(psutil.IOPRIO_VERYLOW)))
ioCounters = Label(window, text="I/O Counters: "+str(p.io_counters()))
numHandles = Label(window, text="Number of Handles: "+str(p.num_handles()))
numthreads = Label(window, text="Number of Threads :"+str(p.num_threads()))
memoryInfo = Label(window, text="Memory Information: "+str(p.memory_info()))
memoryFullInfo = Label(window, text="Full Memory Info: "+str(p.memory_full_info()))
memoryPercent = Label(window, text="Memory Percent: "+ str(p.memory_percent()))
memoryMaps = Label(window, text="Memory Maps: "+str(p.memory_maps())) # 요건 나중에 map으로 만들어서 시각화하기
connnections = Label(window, text="Connections: "+str(p.connections()))



cpu.pack(side=TOP,fill=X)
cpuTime.pack()
cpuCount.pack()
cpuStats.pack()
cpuFreq.pack()
getLodaAvg.pack()
cpu2.pack(side=TOP,fill=X)
ram.pack(side=TOP,fill=X)
swapMemory.pack()
disk.pack(side=TOP,fill=X)
hard.pack(side=TOP,fill=X)
netIO.pack()
netConn.pack()
netIfAddr.pack()
netIfStat.pack()
sensorFans.pack()
bootTime.pack()
pids.pack()

# Process Class
# ioNiceness.pack()
ioCounters.pack()
numHandles.pack()
memoryInfo.pack()
memoryFullInfo.pack()
memoryPercent.pack()
memoryMaps.pack()
connnections.pack()



status = Label(window, text='이미지 정보:', bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

refreshHWIndicators()

## 마우스 이벤트
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