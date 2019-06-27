import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
import matplotlib.animation as animation
import psutil
import threading
import time
import math
import datetime
import platform
from tkinter import font
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageOps


LARGE_FONT = ("Verdana", 12)


class SeaofBTCapp(Tk): # Tk를 상속받은 놈

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs) # 상속받았으므로 tk.Tk(부모꺼)도 해줌

        Tk.iconbitmap(self) # 걍 아이콘
        Tk.title(self, "Comstat v0.2") # 이름 만들어주기
        Tk.wm_geometry(self,"1180x590")
        Tk.wm_resizable(self, width=False, height=False)

        self.container = Frame(self) # 컨테이너라는 놈 프레임으로 만들어주고
        self.container.pack(side="top", fill="both", expand=True) # 컨테이너 붙이고
        self.container.grid_rowconfigure(0, weight=1) # row 설정
        self.container.grid_columnconfigure(0, weight=1) # col 설정

        self.frames = [] # frames라는 리스트 필드 선언

        firstFrame = StartPage(self.container, self)
        firstFrame.grid(row=0, column=0, sticky="nsew")

        self.frames.append(firstFrame)
        firstFrame.tkraise()

    def show_frame(self, cont):  # 페이지 띄우는 메서드
        self.frames.pop().destroy()
        frame = cont(self.container, self)
        frame.pack()
        frame.tkraise()  # 프레임이 여러개일 때 맨 앞으로 가져오는 메서드
        self.frames.append(frame)


        # for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
        #     frame = F(container, self)
        #     # print(frame)
        #
        #     self.frames[F] = frame # 딕셔너리에 저장

        #     frame.grid(row=0, column=0, sticky="nsew")

        # self.show_frame(StartPage) # 스타트 페이지 보이기

        self.cpuflag = False
        self.tottime = 0
        self.limit = 80.
        import smtplib
        from email.mime.text import MIMEText
        from datetime import datetime
        def cpuSendEmail():
            timer = threading.Timer(1, cpuSendEmail)
            tmptime = psutil.cpu_percent()
            if tmptime > self.limit:
                # print(tmptime)
                self.cpuflag = True

            if tmptime > self.limit and self.cpuflag == True:
                self.tottime += 1
            else:
                self.tottime = 0
                self.cpuflag = False
            if self.tottime > 4:
                try:
                    print("over, send a email to the user")
                    ############ 메일 보내기 ###############
                    s = smtplib.SMTP('smtp.gmail.com',587)
                    s.starttls()
                    s.login('gangkkformailing@gmail.com','')
                    msg = MIMEText('CPU 수치가 '+str(self.limit)+"을 초과한 지 "+str(self.tottime)+"초 되었습니다."
                                                                                           "컴퓨터 사용량을 확이핸주세요.")

                    msg['Subject'] = "현재시각: "+str(datetime.now()) + "CPU 사용량 임계점 초과 경고 메일"
                    s.sendmail("gangkkformailing@gmail.com","gtpgg1013@gmail.com",msg.as_string())
                    s.quit()

                    ############ 메일 송신 완료 ############
                    self.cpuflag == False
                except:
                    pass
            timer.start()

        cpuSendEmail()

    # def show_frame(self, cont): # 페이지 띄우는 메서드
    #     frame = self.frames[cont] # 프레임 딕셔너리의 몇번째 프레임
    #     frame.tkraise() # 프레임이 여러개일 때 맨 앞으로 가져오는 메서드


class StartPage(Frame): # 첫번째 페이지 # Frame을 상속받은 비슷한 머시기에다가 self를 쓰면 계속 달아주겠다는 말

    def __init__(self, parent, controller): # 프레임을 상속받은 놈
        Frame.__init__(self, parent)

        bigFont = font.Font(self, family='Courier',size=40,weight='bold')
        label = Label(self, text="COM_STAT v0.2", font=bigFont, height=1) # 라벨 써주고

        label.pack(pady=50, padx=10)

        button = Button(self, text="Static Indications",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = Button(self, text="CPU Times",
                             command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = Button(self, text="CPU Stats",
                             command=lambda: controller.show_frame(PageThree))
        button3.pack()

        button4 = Button(self, text="CPU & RAM Usage",
                             command=lambda: controller.show_frame(PageFour))
        button4.pack()

        mName = Label(self, text=platform.machine(), font=LARGE_FONT)
        dName = Label(self, text=platform.node(), font=LARGE_FONT)
        pName = Label(self, text=platform.platform(), font=LARGE_FONT)
        procName = Label(self, text=platform.processor(), font=LARGE_FONT)
        cName = Label(self, text=platform.python_compiler(), font=LARGE_FONT)
        pVer = Label(self, text="Python version : "+platform.python_branch(), font=LARGE_FONT)

        mName.pack(side=BOTTOM,expand=YES)
        dName.pack(side=BOTTOM,expand=YES)
        pName.pack(side=BOTTOM,expand=YES)
        procName.pack(side=BOTTOM,expand=YES)
        cName.pack(side=BOTTOM,expand=YES)
        pVer.pack(side=BOTTOM,expand=YES)


class PageOne(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Static Indications", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = Button(self, text="HomePage",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = Button(self, text="CPU Times",
                             command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = Button(self, text="CPU Status",
                             command=lambda: controller.show_frame(PageThree))
        button3.pack()

        # Label

        cpuFreq_c = Label(self, text="CPUFreq - current : "+str(psutil.cpu_freq().current))
        cpuFreq_mx = Label(self, text="CPUFreq - max : " + str(psutil.cpu_freq().max))
        cpuFreq_min = Label(self, text="CPUFreq - min : " + str(psutil.cpu_freq().min))

        hard_readCount = Label(self, text="Hard - readcount : " + str(psutil.disk_io_counters().read_count>>20))
        hard_writeCount = Label(self, text="Hard - writecount : " + str(psutil.disk_io_counters().write_count>>20))
        hard_readBytes = Label(self, text="Hard - readbytes : " + str(psutil.disk_io_counters().read_bytes>>20))
        hard_writeBytes = Label(self, text="Hard - writebytes : " + str(psutil.disk_io_counters().write_bytes>>20))
        hard_readTime = Label(self, text="Hard - read_time : " + str(psutil.disk_io_counters().read_time))
        hard_writeTime = Label(self, text="Hard - write_time : "+str(psutil.disk_io_counters().write_time))

        netAddr_fam_MAC = Label(self, text="Network Address - family MAC : " + str(psutil.net_if_addrs()['이더넷'][0][1]))
        netAddr_IP = Label(self, text="Network Address - IP : " + str(psutil.net_if_addrs()['이더넷'][1][1]))
        netAddr_netmask = Label(self, text="Network Address - netmask : " + str(psutil.net_if_addrs()['이더넷'][1][2]))

        memory_total = Label(self, text="Memory - total : "+str(psutil.virtual_memory().total))
        memory_available = Label(self, text="Memory - available : "+str(psutil.virtual_memory().available))



        dt = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        bootTime = Label(self, text="Boot Time : "+str(dt))
        UserName = Label(self, text="User name : "+str(psutil.users()[0].name))


        # pack

        cpuFreq_c.pack(side=BOTTOM,expand=YES,pady=5)
        cpuFreq_mx.pack(side=BOTTOM,expand=YES,pady=5)
        cpuFreq_min.pack(side=BOTTOM,expand=YES,pady=5)

        hard_readCount.pack(side=BOTTOM,expand=YES,pady=5)
        hard_writeCount.pack(side=BOTTOM,expand=YES,pady=5)
        hard_readBytes.pack(side=BOTTOM,expand=YES,pady=5)
        hard_writeBytes.pack(side=BOTTOM,expand=YES,pady=5)
        hard_writeTime.pack(side=BOTTOM,expand=YES,pady=5)
        hard_writeTime.pack(side=BOTTOM,expand=YES,pady=5)

        netAddr_fam_MAC.pack(side=BOTTOM,expand=YES,pady=5)
        netAddr_IP.pack(side=BOTTOM,expand=YES,pady=5)
        netAddr_netmask.pack(side=BOTTOM,expand=YES,pady=5)
        # netAddr_broadcast.pack()
        # netAddr_ptp.pack()

        memory_total.pack(side=BOTTOM,expand=YES,pady=5)
        memory_available.pack(side=BOTTOM,expand=YES,pady=5)

        bootTime.pack(side=BOTTOM,expand=YES,pady=5)
        UserName.pack(side=BOTTOM,expand=YES,pady=5)





class PageTwo(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="CPU times", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = Button(self, text="HomePage",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = Button(self, text="CPU status",
                             command=lambda: controller.show_frame(PageThree))
        button2.pack()

        button3 = Button(self, text="CPU & RAM",
                             command=lambda: controller.show_frame(PageFour))
        button3.pack()

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

        ylim *= 0.1


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
                cpuTime1.configure(text="CPUTime-user: " + str(psutil.cpu_times().user))
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
            tmpCpuU = cpuTimeList[0][0] * 0.1
            tmpCpuSys = cpuTimeList[1][0] * 0.1
            tmpCpuI = cpuTimeList[2][0] * 0.1
            tmpCpuC = cpuTimeList[3][0] * 0.1
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

        button2 = Button(self, text="CPU Times",
                             command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = Button(self, text="CPU & RAM",
                             command=lambda: controller.show_frame(PageFour))
        button3.pack()

        canvasforPic = Canvas(self)
        cpustats1 = Label(canvasforPic, text="Ctx_switches: " + str(psutil.cpu_stats().ctx_switches>>20))
        cpustats2 = Label(canvasforPic, text="interrupts: " + str(psutil.cpu_stats().interrupts>>20))
        cpustats3 = Label(canvasforPic, text="syscalls: " + str(psutil.cpu_stats().syscalls>>20))


        cpustats1.pack()
        cpustats2.pack()
        cpustats3.pack()

        canvasforPic.pack(side=RIGHT)

        ylim = 0
        tcpuTimeInd = psutil.cpu_stats()
        tcpuTimeList = [tcpuTimeInd.ctx_switches>>20, tcpuTimeInd.interrupts>>20, tcpuTimeInd.syscalls>>20]
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
                cpustats1.configure(text="Ctx_switches: " + str(psutil.cpu_stats().ctx_switches>>20))
                # print(str(psutil.cpu_stats().ctx_switches))
                cpustats2.configure(text="interrupts: " + str(psutil.cpu_stats().interrupts>>20))
                cpustats3.configure(text="syscalls: " + str(psutil.cpu_stats().syscalls>>20))

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
        ax.set_ylim(0,ylim*2)
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
            tmpCpuC = cpuTimeList[0][0]>>20
            tmpCpuI = cpuTimeList[1][0]>>20
            tmpCpuS = cpuTimeList[2][0]>>20
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


class PageFour(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="CPU Stats", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = Button(self, text="HomePage",
                         command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = Button(self, text="CPU Times",
                         command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = Button(self, text="CPU Status",
                         command=lambda: controller.show_frame(PageThree))
        button3.pack()

        # canvasforPic = Canvas(self)

        #########################################################################
        ############# 요기 캔버스에다가 사진을 박을거임 #########################
        #########################################################################
        self.inImage, self.outImage = None, None
        self.inH, self.inW, self.outH, self.outW = [0] * 4
        self.photo, self.cvPhoto = None, None
        self.paper = None
        self.canvasforPic = None
        self.canvasforLabel = Canvas(self, height=200, width=300)
        # canvasforPic = Canvas(self)

        def loadImageColor(self,fnameOrCvData):
            #######################################
            ### PIL 객체 --> OpenCV 객체로 복사 ###
            ## 이거 왜 되는지 잘 생각해보자!!
            if type(fnameOrCvData) == str:  # 파일명이 들어왔을경우
                cvData = cv2.imread(fnameOrCvData)  # 파일 --> CV 데이터
            else:
                cvData = fnameOrCvData  # 이거 들여쓰기 안해서 실행이 안됬었음

            self.cvPhoto = cv2.cvtColor(cvData, cv2.COLOR_BGR2RGB)  # 중요한 CV개체 # 이거 numpy array임
            # print(cvPhoto)

            self.photo = Image.fromarray(self.cvPhoto)
            # print(type(photo))
            self.inW, self.inH = self.photo.size  # (photo.width, photo.height)
            self.outW, self.outH = self.inW, self.inH

            # 캔버스 제작
            # self를 붙여야 이게 됨
            self.canvasforPic = Canvas(self, height=self.inH, width=self.inW)

            #######################################
            self.inImage = np.array(self.photo)
            self.outImage = self.inImage[:]

            # print(outImage)

        def displayImageColor(self):
            # print(VIEW_X)
            ## 고정된 화면 크기
            # 가로/세로 비율 계산

            self.paper = PhotoImage(height=self.inH, width=self.inW)
            self.canvasforPic.create_image((self.inW//2 , self.inH//2) , image=self.paper, state='normal')
            # paper = PhotoImage('CPU.PNG')

            print(self.inH, self.inW)
            # print(outH)
            import numpy
            rgbStr = ''  # 전체 픽셀의 문자열을 저장
            for i in numpy.arange(self.inH):
                tmpStr = ''
                for k in numpy.arange(self.inW):
                    i = int(i);
                    k = int(k)
                    r, g, b = self.outImage[i, k, R], self.outImage[i, k, G], self.outImage[i, k, B]
                    tmpStr += ' #%02x%02x%02x' % (r, g, b)
                rgbStr += '{' + tmpStr + '} '
            print(len(rgbStr))
            self.paper.put(rgbStr)
            # print(paper)

            self.inImage = self.outImage.copy()
            self.cvPhoto = self.outImage.copy()

            self.canvasforPic.pack(side=LEFT)



        # print("asdasdsadasdasdasdsadasdads")
        # canvasforPic = Canvas(self, height=inH, width=inW)
        loadImageColor(self, "CPU.PNG") # inImage, inH, inW, outH, outW 설정
        # print(self.canvasforPic)
        # print(self.inImage)
        # print(type(self.outImage))
        displayImageColor(self)
        # canvasforPic.pack(expand=1, anchor=CENTER, side=RIGHT)

        #########################################################################################
        ##################### 여기까지 그림박기 끝 ##############################################
        #########################################################################################
        #
        cpuI = Label(self.canvasforLabel, text="Cpu Usage percent: " + str(psutil.cpu_percent()))
        ramI = Label(self.canvasforLabel, text="Ram Usage percent: " + str(psutil.virtual_memory().percent))

        cpuI.pack(side=BOTTOM)
        ramI.pack(side=BOTTOM)

        self.canvasforLabel.pack(side=RIGHT)

        ylim = 100
        cpuRamList = [psutil.cpu_percent(), psutil.virtual_memory().percent]
        # for cr in cpuRamList:
        #     if ylim < cr:
        #         ylim = cr

        # 밑에서 쓸 현재시각
        nowtime = 0

        def refreshHWIndicators():  # 1초마다 바뀌는 내용 수정
            # global cpuUser, cpuSys, cpuI, cpuC
            # global x, plotCpuUser, plotCpuSys, plotCpuI, plotCpuC, t # 요놈들 쓸거임

            try:
                timer = threading.Timer(1, refreshHWIndicators)
                cpuI.configure(text="CPU Usage: " + str(psutil.cpu_percent()))
                # print(str(psutil.cpu_stats().ctx_switches))
                ramI.configure(text="RAM Usage: " + str(psutil.virtual_memory().percent))

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
        ax.set_title("CPU & RAM Usage")
        ax.set_ylim(0, ylim)
        ax.set_xlim(0, 5.0)
        ax.grid(True)
        ax.set_ylabel("CPU & RAM Usage")
        ax.set_xlabel("Time")

        # Data Placeholders
        cpu = np.zeros(0)
        ram = np.zeros(0)
        t = np.zeros(0)

        # set plots
        plotCpu, = ax.plot(t, cpu, 'b-', label="Cpu Usage")
        plotRam, = ax.plot(t, ram, 'g-', label="Ram Usage")

        ax.legend([plotCpu, plotRam], \
                  [plotCpu.get_label(), plotRam.get_label()])

        xmin = 0.0
        xmax = 5.0
        x = 0.0

        def updateData(self):
            nonlocal cpu, ram
            nonlocal x, plotCpu, plotRam, t  # 요놈들 쓸거임
            # print(x)

            cpuRamList = [[psutil.cpu_percent()], [psutil.virtual_memory().percent]]
            tmpC = cpuRamList[0][0]
            tmpR = cpuRamList[1][0]
            # print(tmpCpuC)
            cpu = np.append(cpu, tmpC)
            ram = np.append(ram, tmpR)
            t = np.append(t, x)

            x += 0.05

            plotCpu.set_data(t, cpu)
            plotRam.set_data(t, ram)

            if x >= xmax - 1.00:
                plotCpu.axes.set_xlim(x - xmax + 1.0, x + 1.0)

            return plotCpu

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

R, G, B = 0, 1, 2 # 3차원으로 쉽게 다루려고 전역 상수 지정해줌
inImage, outImage = None, None # 이제 넘파이로 다룰래
inH, inW, outH, outW = [0] * 4
window, canvas, paper = None, None, None
filename = ""
panYN = False
sx, sy, ex, ey = [0] * 4
VIEW_X, VIEW_Y = 512, 512  # 화면에 보일 크기 (출력용)


#  메인 코드

app = SeaofBTCapp()
app.mainloop()