from tkinter import *
from tkinter import messagebox
def clickLeft(event):
    txt = ''
    if event.num == 1:
        txt += '왼쪽 버튼: '
    elif event.num ==2:
        txt += '가운데 버튼: '
    else:
        txt += '오른쪽 버튼: '
    txt += str(event.x) + "," + str(event.y)
    messagebox.showinfo('제목',txt)

def keyPress(event):
    messagebox.showinfo('요기제목',chr(event.keycode))

window = Tk()
window.geometry("500x300")

photo = PhotoImage(file="C:/images/Pet_GIF/Pet_GIF(256x256)/cat01_256.gif")
lable1 = Label(window, image=photo)

lable1.bind("<Button>", clickLeft) #이렇게 하면 레이블에 바인드 걸리게 마우스 조작 가능
lable1.pack(expand=1,anchor=CENTER)

window.bind("a",keyPress)
# window.bind("<Key>",keyPress)

# window.bind("<Button>",clickLeft) #전체에 대한 마우스 조작

window.mainloop()
