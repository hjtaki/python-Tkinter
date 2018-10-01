import matplotlib

matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk

import urllib
import json

import pandas as pd
import numpy as np

from matplotlib import pyplot as plt

LARGE_FONT =("Verdana",12)
NORM_FONT =("Verdana",10)
SMALL_FONT =("Verdana",8)

style.use("ggplot")

f = Figure(figsize=(5, 5), dpi=100)
a = f.add_subplot(111)

exchange = "BTC-e"
DatCounter = 9000
ProgramName = "btce"
resampleSize = "15Min"
DataPace = "1d"
candleWidth = 0.008
topIndicator = "none"
middleIndicator = "none"
bottomIndicator = "none"

EMAs = []
SMAs = []


def addTopIndicator(what):
    global topIndicator
    global DatCounter

    if DataPace == "tick":
        popupmsg("Indicators in Tick Data not available")

    elif what == "none":
        topIndicator = what
        DatCounter = 9000

    elif what == "rsi":
        rsiQ = tk.Tk()
        rsiQ.wm_title("Periods?")
        label = ttk.Label(rsiQ,text = "Choose how many periods you wnat each RSI calculation to consider")
        label.pack(side = "top", fill = "x", pady =10)

        e = ttk.Entry(rsiQ)
        e.insert(0,14)
        e.pack()
        e.focus_set()

        def callback():
            global topIndicator
            global DatCounter
            group = []
            periods = e.get()
            group.append("rsi")
            group.append(periods)

            topIndicator = group
            DatCounter = 9000
            print("set top indicator to",group)
            rsiQ.destroy()
        b = ttk.Button(rsiQ, text = "Submit", width = 10, command = callback)
        b. pack()
        tk.mainloop()

    # elif what == "macd":
    #     global topIndicator
    #     global DatCounter
    #     topIndicator = "macd"
    #     DatCounter = 9000




# def addMiddleIndicator():
#
# def addBottomIndicator():


def changeTimeFrame(tf):
    global DataPace
    global DatCounter
    if tf == "7d" and resampleSize == "1Min":
        popupmsg("Too much data shosen, choose a smaller time frame or higher Interval")
    else:
        DataPace = tf
        DatCounter = 9000


def changeSampleSize(size,width):
    global resampleSize
    global DatCounter
    global candleWidth
    if DataPace == "7d" and resampleSize == "1Min":
        popupmsg("Too much data shosen, choose a smaller time frame or higher OHLC Interval")
    elif DataPace == "tick":
        popupmsg("you are viewing tick data, not OHLC")

    else:
        resampleSize = size
        DatCounter = 9000
        candleWidth = width

def changeExchange(toWhat,pn):
    global  exchange
    global DatCounter
    global programName

    exchange = toWhat
    programName = pn
    DatCounter = 9000

def popupmsg(msg):
    popup =tk.Tk()

    # def leavemini() :
    #     popup.destroy()

    popup.wm_title("!")
    label = ttk.Label(popup,text = msg, font = NORM_FONT)
    label.pack(side = "top",fill="x",pady=10)
    B1 = ttk.Button(popup,text = "Okay", command = popup.destroy())
    B1.pack()
    popup.mainloop()


def animate(i):
    pullData = open("Tkinter/sampleData.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachline in dataList:
        if len(eachline)>1:
            x, y = eachline.split(',')
            xList.append(int(x))
            yList.append(int(y))

    a.clear()
    a.plot(xList,yList)

def animate2(i):
    pullData = open("Tkinter/sampleData2.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachline in dataList:
        if len(eachline)>1:
            x, y = eachline.split(',')
            xList.append(int(x))
            yList.append(int(y))

    a.clear()
    a.plot(xList,yList)



class SeaofBTCapp(tk.Tk):
    def __init__(self, *args,**kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        # tk.Tk.iconbitmap(self, default="android_uDz_icon.ico")
        tk.Tk.wm_title(self, "diagnostic tool")

        container = tk.Frame(self)
        container.pack(side = "top", fill ="both", expand = True)
        container.grid_rowconfigure(0,weight = 1)
        container.grid_columnconfigure(0,weight = 1)

        # first menubar
        menubar =tk.Menu(container)
        filemenu =tk.Menu(menubar,tearoff=0)
        filemenu.add_command(label = "Save settings",
                             command = lambda :popupmsg("Nor supported just yet"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit",command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        # exchange option
        exchangeChoice = tk.Menu(menubar, tearoff=1)
        exchangeChoice.add_command(label="BTC-a",
                                   command=lambda: changeExchange("BTC-A", "btce1"))
        exchangeChoice.add_command(label="BTC-b",
                                   command=lambda: changeExchange("BTC-B", "btce2"))
        exchangeChoice.add_command(label="BTC-c",
                                   command=lambda: changeExchange("BTC-C", "btce3"))
        exchangeChoice.add_command(label="BTC-d",
                                   command=lambda: changeExchange("BTC-D", "btce4"))

        menubar.add_cascade(label="Exchange", menu=exchangeChoice)

        # timeFrame and sameple size option
        dataTF = tk.Menu(menubar, tearoff =1)

        dataTF.add_command(label = "Tick",
                           command=lambda: changeTimeFrame('tick'))
        dataTF.add_command(label = "1 day",
                           command=lambda: changeTimeFrame('1d'))
        dataTF.add_command(label = "3 days",
                           command=lambda: changeTimeFrame('3d'))
        dataTF.add_command(label = "1 w",
                           command=lambda: changeTimeFrame('7d'))

        menubar.add_cascade(label = "Data time frame", menu = dataTF)

        OHLCI = tk.Menu(menubar, tearoff =1)

        OHLCI.add_command(label = "Tick",
                           command=lambda: changeTimeFrame('tick'))
        OHLCI.add_command(label = "1Min",
                           command=lambda: changeSampleSize('1Min',0.0005))
        OHLCI.add_command(label = "5 min",
                           command=lambda: changeSampleSize('5Min',0.003))
        OHLCI.add_command(label = "15 min",
                           command=lambda: changeSampleSize('15Min',0.008))
        OHLCI.add_command(label = "30 min",
                           command=lambda: changeSampleSize('30 Min',0.016))
        OHLCI.add_command(label = "1 hour",
                           command=lambda: changeSampleSize('1 H',0.0032))
        OHLCI.add_command(label = "3 hour",
                           command=lambda: changeSampleSize('3 H',0.0096))
        menubar.add_cascade(label="OHLC Interval", menu = OHLCI)


        # adding indicator

        topIndi = tk.Menu(menubar, tearoff=1)

        topIndi.add_command(label="None",
                            command=lambda: addTopIndicator('none'))
        topIndi.add_command(label="RSI",
                            command=lambda: addTopIndicator('rsi'))
        topIndi.add_command(label="MACD",
                            command=lambda: addTopIndicator('macd'))
        menubar.add_cascade(label="Top indicator", menu=topIndi)





        tk.Tk.config(self,menu=menubar)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):
        # for F in (StartPage, BTCePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column =0, sticky ="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="choose one options ", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="page1",
                            command = lambda: controller.show_frame(PageOne))
        button1.pack()

        button2 = ttk.Button(self, text="page2",
                            command = lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = ttk.Button(self, text="close", command = quit)
        button3.pack()




class PageOne(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Page One", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to home",
                            command = lambda: controller.show_frame(StartPage))
        button1.pack()

        canvas = FigureCanvasTkAgg(f,self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH, expand = True)

        canvas = FigureCanvasTkAgg(f,self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM,fill=tk.BOTH, expand = True)



class PageTwo(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Page Two", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to home",
                            command = lambda: controller.show_frame(StartPage))
        button1.pack()


        # gragh
        canvas = FigureCanvasTkAgg(f,self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH, expand = True)

        # toolbar = NavigationToolbar2TkAgg(canvas,self)
        # toolbar.update()
        # canvas._tkcanvas.pack()


app = SeaofBTCapp()
app.geometry("1280x720")
ani = animation.FuncAnimation(f,animate,interval=1000)
app.mainloop()


# todo :16 ongoing