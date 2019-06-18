## 트리뷰 활용
from tkinter import *
from tkinter import ttk
import csv
from tkinter.simpledialog import *
from tkinter.filedialog import *

def openCSV():
    global csvList
    # 파일이름 (전체 경로) 가져오고
    filename = askopenfilename(parent=None,
                               filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))

    # 내용저장할 csvList 제작해주고
    csvList = []
    with open(filename) as rfp: # open객체 rfp에 넣어주고
        reader = csv.reader(rfp) # 통짜로 읽어서 reader에 넣어주고
        headerList = next(reader) # 반복자의 다음 요소를 구하는 함수 # with문 안에 애들은 지역변수가 아닌듯?
        sum = 0
        count = 0
        print(reader)
        for cList in reader: # iterator type인 reader 객체 : for loop로 한 line씩 가져옴(보통)
            csvList.append(cList)
        print(csvList)

    # sheet는 Treeview 객체
    # 기존 시트 클리어 : sheet 안 내용 다 지워주는 method
    sheet.delete(*sheet.get_children())

    # sheet는 ttk의 TreeView로 구현된 객체
    # 첫번째 열 헤더 만들기
    sheet.column('#0', width=70)  # 첫 컬럼의 내부이름
    sheet.heading('#0', text=headerList[0])
    # 두번째 이후 열 헤더 만들기
    sheet['columns'] = headerList[1:]  # 두분째 이후 컬럼의 내부이름(내맘대로)
    for colName in headerList[1:]:
        sheet.column(colName, width=70) # 내부이름
        sheet.heading(colName, text=colName) # 외부이름

    # 내용 채우기
    for row in csvList:
        sheet.insert('', 'end', text=row[0], values=row[1:])
    sheet.pack(expand=1, anchor=CENTER)

import xlrd
def openExcel():
    global csvList
    filename = askopenfilename(parent=None,
                               filetypes=(("엑셀 파일", "*.xls;*.xlsx"), ("모든 파일", "*.*")))

    csvList = []
    workbook = xlrd.open_workbook(filename) # excel : 파일자체가 워크북 / 각 파일 한장한장이 워크시트

    print(workbook.nsheets)
    wsList = workbook.sheets() # 리스트로 리턴
    print(type(wsList[0]))

    headerList = []
    for i in range(wsList[0].ncols): # 이렇게하면 coloum개수 가져올 수 있지
        headerList.append(wsList[0].cell_value(0,i))
    print(headerList)

    # 내용 채우기
    for wsheet in wsList:
        rowCount = wsheet.nrows
        colCount = wsheet.ncols
        for i in range(1, rowCount):
            tmplist = []
            for k in range(colCount):
                tmplist.append(wsheet.cell_value(i,k)) # cell_value : 각 하나 셀의 값
            csvList.append(tmplist)

    for worksheet in workbook.sheets(): # 이렇게하면 하나씩 가져와서 돌림
        print(worksheet.name, worksheet.nrows, worksheet.ncols)

    # with open(filename) as rfp:
    #     reader = csv.reader(rfp)
    #     headerList = next(reader) # 반복자의 다음 요소를 구하는 함수
    #     sum = 0
    #     count = 0
    #     for cList in reader:
    #         csvList.append(cList)

    # 기존 시트 클리어 : sheet 안 내용 다 지워주는 method
    sheet.delete(*sheet.get_children())

    # 첫번째 열 헤더 만들기
    sheet.column('#0', width=70)  # 첫 컬럼의 내부이름
    sheet.heading('#0', text=headerList[0])
    # 두번째 이후 열 헤더 만들기
    sheet['columns'] = headerList[1:]  # 두분째 이후 컬럼의 내부이름(내맘대로)
    for colName in headerList[1:]:
        sheet.column(colName, width=70) # 내부이름
        sheet.heading(colName, text=colName) # 외부이름

    # 내용 채우기
    for row in csvList:
        sheet.insert('', 'end', text=row[0], values=row[1:])
    sheet.pack(expand=1, anchor=CENTER)

window = Tk()
window.geometry('600x500')
sheet = ttk.Treeview(window)

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="CSV 처리", menu=fileMenu)
fileMenu.add_command(label="CSV 열기", command=openCSV)
fileMenu.add_command(label="엑셀 열기", command=openExcel)
fileMenu.add_separator()

window.mainloop()