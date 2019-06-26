from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.animation as animation
import os
import numpy as np

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Tkinter Matplotlib Embedding")
        self.minsize(640,400)
        self.wm_iconbitmap()
        self.matplotCanvas()

    def matplotCanvas(self):
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8], [5,6,7,8,8,8,3,3])

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side = BOTTOM, fill = BOTH, expand = True)


if __name__ == '__main__':
    root = Root()
    root.mainloop()