from tkinter import *
from tkinter import messagebox
def fileClick():
    messagebox.showinfo('요기제목','요기내용')

window = Tk()
mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu) #클릭으로 메뉴 확장시킬 땐 casacade
fileMenu.add_command(label="열기",command=fileClick)
fileMenu.add_separator()
fileMenu.add_command(label="종료", command=None)

window.mainloop()
