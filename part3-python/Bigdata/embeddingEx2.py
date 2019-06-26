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

LARGE_FONT = ("Verdana", 12)


class SeaofBTCapp(Tk): # Tk를 상속받은 놈

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs) # 상속받았으므로 tk.Tk(부모꺼)도 해줌

        Tk.iconbitmap(self) # 걍 아이콘
        Tk.title(self, "Sea of BTC client") # 이름 만들어주기
        Tk.wm_geometry(self,"1280x640")
        Tk.wm_resizable(self, width=False, height=False)

        container = Frame(self) # 컨테이너라는 놈 프레임으로 만들어주고
        container.pack(side="top", fill="both", expand=True) # 컨테이너 붙이고
        container.grid_rowconfigure(0, weight=1) # row 설정
        container.grid_columnconfigure(0, weight=1) # col 설정

        self.frames = {} # frames라는 딕셔너리 필드 선언

        for F in (StartPage, PageOne, PageTwo):
            frame = F(container, self)
            print(frame)

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

        button2 = Button(self, text="Dynamic Indications",
                             command=lambda: controller.show_frame(PageTwo))
        button2.pack()


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
        label = Label(self, text="Dynamic Indications", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = Button(self, text="HomePage",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        canvasforPic = Canvas(self)
        canvasforPic
        cpu = Label(canvasforPic, text="CPU: " + str(psutil.cpu_percent()))
        cpuTime = Label(canvasforPic, text="CPUTime: " + str(psutil.cpu_times()))
        cpuStats = Label(canvasforPic, text="CPUStats " + str(psutil.cpu_stats()))
        cpu2 = Label(canvasforPic, text="CPU_specific: " + str(psutil.cpu_times_percent()))

        cpu.pack()
        cpuTime.pack()
        cpuStats.pack()
        cpu2.pack()

        canvasforPic.pack(side=RIGHT)

        # 밑에서 쓸 현재시각
        nowtime = 0

        def refreshHWIndicators():  # 1초마다 바뀌는 내용 수정
            try:
                timer = threading.Timer(1, refreshHWIndicators)
                cpu.configure(text="CPU: " + str(psutil.cpu_percent()))
                cpu2.configure(text="CPU_specific " + str(psutil.cpu_times_percent()))
                cpuTime.configure(text="CPUTime: " + str(psutil.cpu_times()))

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
        x = np.arange(0, 2 * np.pi, 0.01)

        def animate(i):
            line.set_ydata(np.sin(x + i / 10.0))  # update the data
            return line,

        canvas = FigureCanvasTkAgg(f, self)
        canvas.get_tk_widget()

        ax = f.add_subplot(111)
        line, = ax.plot(x, np.sin(x))

        ani = animation.FuncAnimation(f, animate, np.arange(1, 200), interval=25, blit=False)

        canvas.draw()
        canvas.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=True)

        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)


app = SeaofBTCapp()
app.mainloop()
