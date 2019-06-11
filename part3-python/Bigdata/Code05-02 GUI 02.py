from tkinter import *
from tkinter import messagebox
def clickButton():
    messagebox.showinfo('요기제목','요기내용')

window = Tk() # root = Tk()
window.title("갱콩콩")
window.geometry("800x1000")
window.resizable(width=False,height=True)

label1= Label(window, text="파이썬 공부중") # 레이블 만들고
label2= Label(window, text="강콩콩", font=("궁서체","30"), fg="blue")
label3= Label(window, text="training for the programming gosu", bg="red", width=20, height=5, anchor=SE)

photo = PhotoImage(file="C:/images/Pet_GIF/Pet_GIF(256x256)/cat01_256.gif")
lable4 = Label(window, image=photo)
button1 = Button(window, text='나를 눌러줘', command=clickButton)
button2 = Button(window, text='나를 눌러줘',image=photo, command=clickButton)

label1.pack() # 레이블 붙이기
label2.pack()
label3.pack()
lable4.pack(side=LEFT)
button1.pack(side=RIGHT)
button2.pack()
window.mainloop()