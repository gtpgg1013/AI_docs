import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from tkinter import *

import numpy as np
import matplotlib.animation as animation
window = Tk()

window.title("Sea of BTC client")  # 이름 만들어주기

container = Frame()  # 컨테이너라는 놈 프레임으로 만들어주고
container.pack(side="top", fill="both", expand=True)  # 컨테이너 붙이고
container.grid_rowconfigure(0, weight=1)  # row 설정
container.grid_columnconfigure(0, weight=1)

window.mainloop()