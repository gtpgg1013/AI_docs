from tkinter import *
from tkinter import messagebox
import os
import math

## 전역변수 선언부
# folder = askdirectory(parent=window) #쓰려면 window 밑으로
fnamelist = []
for dirName, subDirlist, fnames in os.walk('C:/images'):
    for fname in fnames:
        if os.path.splitext(fname)[1].upper() == '.GIF':
            fnamelist.append(os.path.join(dirName,fname))

# dirName = "C:/images/Pet_GIF/Pet_GIF(256x256)/"
# fnamelist = ["cat01_256.gif","cat02_256.gif","cat03_256.gif","cat04_256.gif","cat05_256.gif","cat06_256.gif"]
# fnamelist = ["cat0"+{}+"_256.gif".format(i) for i in range(0,15)]
# photolist = [None] * 15
num = 0 # 현재 사진 순번

## 함수 선언부
def clickPrev():
    global num
    num -= 1
    if(num<0):
        num = len(fnamelist) - 1
    photo = PhotoImage(file=fnamelist[num])
    pLabel.configure(image=photo)
    pLabel.photo = photo
    nameLabel.configure(text=os.path.split(fnamelist[num])[1])

def clickNext():
    global num
    num += 1
    if(num>=len(fnamelist)):
        num = 0
    photo = PhotoImage(file=fnamelist[num])
    pLabel.configure(image=photo)
    pLabel.photo = photo
    nameLabel.configure(text=os.path.split(fnamelist[num])[1])

# def pressPrev(event):
#     global num
#     num -= 1
#     if(num<0):
#         num = len(fnamelist) - 1
#     photo = PhotoImage(file=dirName+fnamelist[num])
#     pLabel.configure(image=photo)
#     pLabel.photo = photo
#     nameLabel.configure(text=fnamelist[num])
#
# def pressNext(event):
#     global num
#     num += 1
#     if(num>=len(fnamelist)):
#         num = 0
#     photo = PhotoImage(file=dirName+fnamelist[num])
#     pLabel.configure(image=photo)
#     pLabel.photo = photo
#     nameLabel.configure(text=fnamelist[num])
#
# def pressHome(event):
#     global num
#     num = 0
#     photo = PhotoImage(file=dirName+fnamelist[num])
#     pLabel.configure(image=photo)
#     pLabel.photo = photo
#     nameLabel.configure(text=fnamelist[num])
#
# def pressEnd(event):
#     global num
#     num = len(fnamelist) - 1
#     photo = PhotoImage(file=dirName + fnamelist[num])
#     pLabel.configure(image=photo)
#     pLabel.photo = photo
#     nameLabel.configure(text=fnamelist[num])
#
# def PressNum(event):
#     # messagebox.showinfo(int(chr(event.keycode)))
#     global num
#     num = num + int(chr(event.keycode))
#     if num > len(fnamelist) - 1:
#         num = len(fnamelist) - 1
#     photo = PhotoImage(file=dirName + fnamelist[num])
#     pLabel.configure(image=photo)
#     pLabel.photo = photo
#     nameLabel.configure(text=fnamelist[num])

def pressKey(event):
    global num
    if event.keycode == 36:
        num = 0
    elif event.keycode == 35:
        num = len(fnamelist)-1
    elif event.keycode in range(49,58):
        num += (event.keycode-48)
        if num > len(fnamelist) - 1:
            num = len(fnamelist) - 1
    photo = PhotoImage(file=fnamelist[num])
    pLabel.configure(image=photo)
    pLabel.photo = photo
    nameLabel.configure(text=os.path.split(fnamelist[num])[1])

from tkinter.simpledialog import *
def jumpNum(event=0):
    # messagebox.showinfo(int(chr(event.keycode)))
    if event==0 :
        event = askinteger("건너뛸 수", "숫자-->")
    print(event)
    global num
    num = num + int(event)
    if num > len(fnamelist) - 1:
        num = len(fnamelist) - 1
    photo = PhotoImage(file=fnamelist[num])
    pLabel.configure(image=photo)
    pLabel.photo = photo
    nameLabel.configure(text=os.path.split(fnamelist[num])[1])

from tkinter.filedialog import *
def selectFile():
    filename = askopenfilename(parent=window, filetypes=(("GIF파일", "*.gif;*.raw"), ("모든파일", "*.*"))) #이름, 파일타입
    pLabel.configure(text=str(filename))

def expandFile():
    exp = askinteger("안내", "확대할 배율(2~6)을 입력하세요")
    photo = PhotoImage(file=fnamelist[num])
    photo = photo.zoom(exp,exp)
    pLabel.configure(image=photo)
    pLabel.photo = photo

def shrinkFile():
    shrk = askinteger("안내", "축소할 배율(2~6)을 입력하세요")
    photo = PhotoImage(file=fnamelist[num])
    photo = photo.subsample(shrk, shrk)
    pLabel.configure(image=photo)
    pLabel.photo = photo


## 메인 코드부
window = Tk()
mainMenu = Menu(window)
window.config(menu=mainMenu)

passMenu = Menu(mainMenu)
mainMenu.add_cascade(label="이동", menu=passMenu)
passMenu.add_command(label="앞으로", command=clickNext)
passMenu.add_separator()
passMenu.add_command(label="뒤로", command=clickPrev)

jumpMenu = Menu(mainMenu)
mainMenu.add_cascade(label="건너뛰기",menu=jumpMenu)
# for i in range(0,2):
jumpMenu.add_command(label=1, command=lambda: jumpNum(1)) #콜백함수에서 파라미터를 넘기기 위한 일종의 약속 : lambda식 이용
jumpMenu.add_command(label=3, command=lambda: jumpNum(3)) #콜백함수에서 파라미터를 넘기기 위한 일종의 약속 : lambda식 이용
jumpMenu.add_command(label=5, command=lambda: jumpNum(5)) #콜백함수에서 파라미터를 넘기기 위한 일종의 약속 : lambda식 이용
jumpMenu.add_command(label='원하는 수',command=jumpNum)
jumpMenu.add_separator()
jumpMenu.add_command(label="파일 선택", command=selectFile)

effectMenu = Menu(mainMenu)
mainMenu.add_cascade(label="이미지 효과",menu=effectMenu)
effectMenu.add_command(label="확대하기",command=expandFile)
effectMenu.add_command(label="축소하기",command=shrinkFile)

window.title("GIF Picture Viewer (Ver 0.0.1)")
window.geometry("600x600")
window.resizable(width=FALSE,height=TRUE)

btnPrev = Button(window, text="<<Prev", command=clickPrev)
btnNext = Button(window, text=">>Next", command=clickNext)

photo = PhotoImage(file=fnamelist[num])
pLabel = Label(window, image=photo)
nameLabel = Label(window, text=os.path.split(fnamelist[num])[1])

btnPrev.place(x=100,y=10)
nameLabel.place(x=250,y=10)
btnNext.place(x=450,y=10)
pLabel.pack(expand=YES)

window.bind("<Key>",pressKey)

# window.bind("<Home>",pressHome)
# window.bind("<End>",pressEnd)
# window.bind("<Left>",pressPrev)
# window.bind("<Right>",pressNext)
# # window.bind("0~9",PressNum)
# window.bind(1,PressNum)
# window.bind(2,PressNum)
# window.bind(3,PressNum)
# window.bind(4,PressNum)
# window.bind(5,PressNum)
# window.bind(6,PressNum)
# window.bind(7,PressNum)
# window.bind(8,PressNum)
# window.bind(9,PressNum)
#짧은 코드로 다시

window.mainloop()
