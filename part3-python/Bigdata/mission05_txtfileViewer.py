from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.filedialog import *

#전역변수 선언부
window = Tk()
window.geometry("400x400")
window.resizable(True, True)
nowFileName = ""
text = Text(window)

#함수 선언부
def openFile():
    global nowFileName
    if nowFileName != "":
        messagebox.showinfo("안내", "파일이 열려있습니다, 파일을 바꾸시려면 바꾸기 메뉴를 이용해 주십시오")
    else:
        filename = askopenfilename(parent=window, filetypes=(("text파일", "*.txt"), ("모든 파일", "*.*")))
        nowFileName = filename
        inFp = open(filename, "r")
        text.delete(1.0,END)
        while True:
            inStr = inFp.readline()
            if not inStr:
                break
            text.insert(1.0,inStr)
        # text.insert(CURRENT,"안녕하세요")
        text.pack()

def saveFile():
    if nowFileName == "":
        messagebox.showinfo("안내", "저장할 파일이 없습니다.")
    else:
        m_file = text.get(1.0,END)
        f = open(nowFileName, 'wt')
        f.write(m_file)
        f.close()
        messagebox.showinfo("안내", "저장이 성공적으로 완료되었습니다.")

def changeFile():
    global nowFileName
    filename = askopenfilename(parent=window, filetypes=(("text파일", "*.txt"), ("모든 파일", "*.*")))
    nowFileName = filename
    inFp = open(filename, "r")
    text.delete(1.0,END)
    while True:
        inStr = inFp.readline()
        if not inStr:
            break
        text.insert(CURRENT,inStr)
    text.pack()

def copyFile():
    new_filename = simpledialog.askstring("안내","파일명을 입력해주세요")
    saveDir = askdirectory()
    m_file = text.get(1.0, END)
    f = open(saveDir+"/"+new_filename+".txt", 'wt')
    f.write(m_file)
    f.close()
    messagebox.showinfo("안내", "복사가 성공적으로 완료되었습니다.")


#메인 코드부
mainMenu = Menu(window)
window.config(menu=mainMenu)
window.title("메모장")

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일",menu=fileMenu)
fileMenu.add_command(label="열기",command=openFile)
fileMenu.add_command(label="저장",command=saveFile)

editMenu = Menu(mainMenu)
mainMenu.add_cascade(label="편집",menu=editMenu)
editMenu.add_command(label="바꾸기",command=changeFile)
editMenu.add_command(label="복사",command=copyFile)
editMenu.add_command(label="붙여넣기",command=lambda : messagebox.showinfo("안내","아직 미구현입니다."))

window.mainloop()