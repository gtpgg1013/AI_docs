from tkinter import *
from tkinter import messagebox
from tkinter.colorchooser import *
from tkinter.simpledialog import *

# 전역변수
window = Tk()
window.geometry("500x500")
window.resizable(True,True)
window.title("그림판")
canvas = None
x1, y1, x2, y2 = None, None, None, None
pencolor = 'black'
penwidth = 5
LINE, CIRCLE = 0,1
mode = LINE

# 함수
def mouseClick(event):
    global x1,x2,y1,y2
    x1 = event.x
    y1 = event.y

def mouseDrop(event):
    global x1,x2,y1,y2,penwidth,pencolor,mode
    x2 = event.x
    y2 = event.y
    if mode == LINE:
        canvas.create_line(x1,x2,y1,y2,width=penwidth,fill=pencolor)
    else:
        canvas.create_oval(x1,x2,y1,y2,width=penwidth,fill=pencolor)

def changeMode(event):
    global mode
    if event == LINE:
        mode = LINE
    else:
        mode = CIRCLE

# 메인코드
mainMenu = Menu(window)
window.config(menu=mainMenu)
canvas = Canvas(window, height=600, width=800)
canvas.bind("<Button-1>", mouseClick)
canvas.bind("<ButtonRelease-1>", mouseDrop)
canvas.pack()

picMenu = Menu(mainMenu)
mainMenu.add_cascade(label="도형",menu=picMenu)
picMenu.add_command(label="선",command=lambda : changeMode(LINE))
picMenu.add_command(label="원",command=lambda : changeMode(CIRCLE))

window.mainloop()
