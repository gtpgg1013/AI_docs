import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from tkinter import *

import numpy as np
import matplotlib.animation as animation

import psutil
import threading

import time
import math

LARGE_FONT = ("Verdana", 12)


class SeaofBTCapp(Tk): # Tk를 상속받은 놈

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs) # 상속받았으므로 tk.Tk(부모꺼)도 해줌

        Tk.iconbitmap(self) # 걍 아이콘
        Tk.title(self, "Comstat v0.08") # 이름 만들어주기
        Tk.wm_geometry(self,"1280x640")
        Tk.wm_resizable(self, width=False, height=False)

        container = Frame(self) # 컨테이너라는 놈 프레임으로 만들어주고
        container.pack(side="top", fill="both", expand=True) # 컨테이너 붙이고
        container.grid_rowconfigure(0, weight=1) # row 설정
        container.grid_columnconfigure(0, weight=1) # col 설정

        self.frames = {} # frames라는 딕셔너리 필드 선언

        for F in (StartPage, PageOne, PageTwo, PageThree):
            frame = F(container, self)
            # print(frame)

            self.frames[F] = frame # 딕셔너리에 저장

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage) # 스타트 페이지 보이기

    def show_frame(self, cont): # 페이지 띄우는 메서드
        frame = self.frames[cont] # 프레임 딕셔너리의 몇번째 프레임
        frame.tkraise() # 프레임이 여러개일 때 맨 앞으로 가져오는 메서드


class StartPage(Frame): # 첫번째 페이지

    def __init__(self, parent, controller): # 프레임을 상속받은 놈
        Frame.__init__(self, parent)
        label = Label(self, text="COM_STAT v0.07", font=LARGE_FONT) # 라벨 써주고
        label.pack(pady=100, padx=100)

        button = Button(self, text="Static Indications",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = Button(self, text="CPU Times",
                             command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = Button(self, text="CPU Stats",
                             command=lambda: controller.show_frame(PageThree))
        button3.pack()        


class PageOne(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Static Indications", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = Button(self, text="HomePage",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = Button(self, text="Dynamic Indications",
                             command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="CPU times", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = Button(self, text="HomePage",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        canvasforPic = Canvas(self)
        cpuTime1 = Label(canvasforPic, text="CPUTime-user: " + str(psutil.cpu_times().user))
        cpuTime2 = Label(canvasforPic, text="CPUTime-system: " + str(psutil.cpu_times().system))
        cpuTime3 = Label(canvasforPic, text="CPUTime-idle: " + str(psutil.cpu_times().idle))
        cpuTime4 = Label(canvasforPic, text="CPUTime-interrupt: " + str(psutil.cpu_times().interrupt))

        ylim = 0
        tcpuTimeInd = psutil.cpu_times()
        tcpuTimeList = [tcpuTimeInd.user, tcpuTimeInd.system, tcpuTimeInd.idle, tcpuTimeInd.interrupt]
        for tcpu in tcpuTimeList:
            if ylim < tcpu:
                ylim = tcpu


        cpuTime1.pack()
        cpuTime2.pack()
        cpuTime3.pack()
        cpuTime4.pack()

        canvasforPic.pack(side=RIGHT)

        # 밑에서 쓸 현재시각
        nowtime = 0

        def refreshHWIndicators():  # 1초마다 바뀌는 내용 수정
            # global cpuUser, cpuSys, cpuI, cpuC
            # global x, plotCpuUser, plotCpuSys, plotCpuI, plotCpuC, t # 요놈들 쓸거임
            
            try:
                timer = threading.Timer(1, refreshHWIndicators)
                cpuTime1 = Label(canvasforPic, text="CPUTime-user: " + str(psutil.cpu_times().user))
                cpuTime2.configure(text="CPUTime-system: " + str(psutil.cpu_times().system))
                cpuTime3.configure(text="CPUTime-idle: " + str(psutil.cpu_times().idle))
                cpuTime4.configure(text="CPUTime-interrupt: " + str(psutil.cpu_times().interrupt))

                nowtime = time.time()

                timer.start()
            except:
                pass

        refreshHWIndicators()

        ################################################################
        ################## 여기부터 그래프부분 #########################
        ################################################################

        # 처음 하면 되는것 : cpu time 4개를 동적으로 한꺼번에 띄워보자

        f = Figure(figsize=(5, 5), dpi=100)

        # x = np.arange(0, nowtime ,0.01)
        # x = np.arange(0, 2 * np.pi, 0.01)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.get_tk_widget()
        

        ax = f.add_subplot(111)
        ax.set_title("CPU time")
        ax.set_ylim(0,ylim *1.2)
        ax.set_xlim(0,5.0)
        ax.grid(True)
        ax.set_ylabel("CPU time")
        ax.set_xlabel("Time")

        # Data Placeholders
        cpuUser = np.zeros(0)
        cpuSys = np.zeros(0)
        cpuI = np.zeros(0)
        cpuC = np.zeros(0)
        t = np.zeros(0)

        # set plots
        plotCpuUser, = ax.plot(t, cpuUser, 'b-', label="CPU User")
        plotCpuSys, = ax.plot(t, cpuSys, 'g-', label="CPU System")
        plotCpuI, = ax.plot(t, cpuI, 'r-', label="CPU Idle")
        plotCpuC, = ax.plot(t, cpuC, 'd-', label="CPU Corrpution")

        ax.legend([plotCpuUser, plotCpuSys, plotCpuI, plotCpuC],\
                  [plotCpuUser.get_label(), plotCpuSys.get_label(), plotCpuI.get_label(), plotCpuC.get_label()])

        xmin = 0.0
        xmax = 5.0
        x = 0.0
        
        def updateData(self):
            nonlocal cpuUser, cpuSys, cpuI, cpuC, ylim
            nonlocal x, plotCpuUser, plotCpuSys, plotCpuI, plotCpuC, t # 요놈들 쓸거임
            # print(x)

            cpuTimeInd = psutil.cpu_times()
            cpuTimeList = [[cpuTimeInd.user], [cpuTimeInd.system], [cpuTimeInd.idle], [cpuTimeInd.interrupt]]
            tmpCpuU = cpuTimeList[0][0]
            tmpCpuSys = cpuTimeList[1][0]
            tmpCpuI = cpuTimeList[2][0]
            tmpCpuC = cpuTimeList[3][0]
            # print(tmpCpuC)
            cpuUser = np.append(cpuUser,tmpCpuU)
            cpuSys = np.append(cpuSys,tmpCpuSys)
            cpuI = np.append(cpuI,tmpCpuI)
            cpuC = np.append(cpuC,tmpCpuC)
            t = np.append(t,x)

            x += 0.05

            plotCpuUser.set_data(t, cpuUser)
            plotCpuSys.set_data(t, cpuSys)
            plotCpuI.set_data(t, cpuI)
            plotCpuC.set_data(t, cpuC)

            if x >= xmax - 1.00:
                plotCpuUser.axes.set_xlim(x - xmax +1.0, x+1.0)

            return plotCpuUser

        # line, = ax.plot(x, np.sin(x))

        # ax = f.add_subplot(111)
        # line, = ax.plot(x, np.sin(x))

        ani = animation.FuncAnimation(f, updateData, interval=25, blit=False, frames=200, repeat=True)

        canvas.draw()
        canvas.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=True)

        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)

class PageThree(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="CPU Stats", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = Button(self, text="HomePage",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        canvasforPic = Canvas(self)
        cpustats1 = Label(canvasforPic, text="Ctx_switches: " + str(psutil.cpu_stats().ctx_switches))
        cpustats2 = Label(canvasforPic, text="interrupts: " + str(psutil.cpu_stats().interrupts))
        cpustats3 = Label(canvasforPic, text="syscalls: " + str(psutil.cpu_stats().syscalls))


        cpustats1.pack()
        cpustats2.pack()
        cpustats3.pack()

        canvasforPic.pack(side=RIGHT)

        ylim = 0
        tcpuTimeInd = psutil.cpu_stats()
        tcpuTimeList = [tcpuTimeInd.ctx_switches, tcpuTimeInd.interrupts, tcpuTimeInd.syscalls]
        for tcpu in tcpuTimeList:
            if ylim < tcpu:
                ylim = tcpu

        # 밑에서 쓸 현재시각
        nowtime = 0

        def refreshHWIndicators():  # 1초마다 바뀌는 내용 수정
            # global cpuUser, cpuSys, cpuI, cpuC
            # global x, plotCpuUser, plotCpuSys, plotCpuI, plotCpuC, t # 요놈들 쓸거임
            
            try:
                timer = threading.Timer(1, refreshHWIndicators)
                cpustats1.configure(text="Ctx_switches: " + str(psutil.cpu_stats().ctx_switches))
                print(str(psutil.cpu_stats().ctx_switches))
                cpustats2.configure(text="interrupts: " + str(psutil.cpu_stats().interrupts))
                cpustats3.configure(text="syscalls: " + str(psutil.cpu_stats().syscalls))

                nowtime = time.time()

                timer.start()
            except:
                pass

        refreshHWIndicators()

        ################################################################
        ################## 여기부터 그래프부분 #########################
        ################################################################

        # 처음 하면 되는것 : cpu time 4개를 동적으로 한꺼번에 띄워보자

        f = Figure(figsize=(5, 5), dpi=100)

        # x = np.arange(0, nowtime ,0.01)
        # x = np.arange(0, 2 * np.pi, 0.01)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.get_tk_widget()
        

        ax = f.add_subplot(111)
        ax.set_title("CPU Stat")
        ax.set_ylim(0,ylim+1.2)
        ax.set_xlim(0,5.0)
        ax.grid(True)
        ax.set_ylabel("CPU Stat")
        ax.set_xlabel("Time")

        # Data Placeholders
        cpuC = np.zeros(0)
        cpuI = np.zeros(0)
        cpuS = np.zeros(0)
        t = np.zeros(0)

        # set plots
        plotCpuCtx, = ax.plot(t, cpuC, 'b-', label="Ctx switches")
        plotCpuint, = ax.plot(t, cpuI, 'g-', label="interrupts")
        plotCpuSys, = ax.plot(t, cpuS, 'r-', label="syscalls")

        ax.legend([plotCpuCtx, plotCpuSys, plotCpuint],\
                  [plotCpuCtx.get_label(), plotCpuSys.get_label(), plotCpuint.get_label()])

        xmin = 0.0
        xmax = 5.0
        x = 0.0
        
        def updateData(self):
            nonlocal cpuC, cpuS, cpuI, ylim
            nonlocal x, plotCpuCtx, plotCpuSys, plotCpuint, t # 요놈들 쓸거임
            # print(x)

            cpuTimeInd = psutil.cpu_stats()
            cpuTimeList = [[cpuTimeInd.ctx_switches], [cpuTimeInd.interrupts], [cpuTimeInd.syscalls]]
            tmpCpuC = cpuTimeList[0][0]
            tmpCpuI = cpuTimeList[1][0]
            tmpCpuS = cpuTimeList[2][0]
            # print(tmpCpuC)
            cpuC = np.append(cpuC,tmpCpuC)
            cpuI = np.append(cpuI,tmpCpuI)
            cpuS = np.append(cpuS,tmpCpuS)
            t = np.append(t,x)

            x += 0.05

            plotCpuCtx.set_data(t, cpuC)
            plotCpuint.set_data(t, cpuI)
            plotCpuSys.set_data(t, cpuS)

            if x >= xmax - 1.00:
                plotCpuCtx.axes.set_xlim(x - xmax +1.0, x+1.0)

            return plotCpuCtx

        # line, = ax.plot(x, np.sin(x))

        # ax = f.add_subplot(111)
        # line, = ax.plot(x, np.sin(x))

        ani = animation.FuncAnimation(f, updateData, interval=25, blit=False, frames=200, repeat=True)

        canvas.draw()
        canvas.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=True)

        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)



# 전역 변수
# x, plotCpuUser, plotCpuSys, plotCpuI, plotCpuC, t = 0, None, None, None, None, None
# cpuUser, cpuSys, cpuI, cpuC = None, None, None, None


#  메인 코드

app = SeaofBTCapp()
app.mainloop()
