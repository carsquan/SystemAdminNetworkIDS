# !/usr/bin/python3  
from argparse import Action
import imp
import queue
import threading
from tkinter import *   
from turtle import width  
import pandas as pd
from Metrics.packetLoss import packetLoss
import asyncio
import Metrics.networkinfo as netinfo
from pandastable import Table, TableModel
import Metrics.throughput as through
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import datetime
import tkinter as tk
import time
from Policies.anom import *

packetSniffTime = 10
pingTime = 10000
height = 720
width = 1080
dfTime = 60000
canvasTime = 1000
throughputtime = 10000
uptime = 0

class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry(f"{width}x{height}")

        self.botFram = Frame(self.root, height=30, width=width,relief="groove") 
        self.rightFrame = Frame(self.root, height=height, width=width/2)
        self.label = tk.Label(self.botFram,text="")
        self.root.title('Network Monitor')
        self.packetL = tk.Label(self.botFram, text="0.00%")
        self.ping = tk.Label(self.botFram,text="0")
        self.label.pack(side=RIGHT)
        self.packetL.pack(side=LEFT)
        self.ping.pack(side=LEFT)
        self.gui_queue = queue.Queue()

        self.df =netinfo.return_network()

        #Dataframe for throughput2
        self.throughputDF =  pd.DataFrame()
        
    
        self.f = Frame(self.root, height=height, width=width/2)
        self.topfram = Frame(self.root, height=30, width=width)
        self.botFram.pack(side=BOTTOM,fill="x")
        
        self.startBtn = tk.Button(self.topfram, text ="Start", state=DISABLED)
        self.stopBtn = tk.Button(self.topfram, text ="Stop")
        self.startBtn.pack(side=LEFT)
        self.stopBtn.pack(side=LEFT)
        self.table = pt = Table(self.f, dataframe=self.df,showtoolbar=False, showstatusbar=False, editable=False, enable_menus=False)
        self.topfram.pack(fill="x",side=TOP)
        self.f.pack(fill="both",side=LEFT, expand=True)
        self.rightFrame.pack(fill="both",side=RIGHT, expand=True)
        self.otherDF = df = pd.DataFrame(columns=["X","Time"])
        pt.show()
        self.makeCanvas()
        self.setupBTNS()
        self.update_clock()
        self.periodicGuiUpdate()
        self.updateTable()
        self.updatePKLoss()
        threading.Thread(target=self.start_loop).start()
        self.updateCanvas()
        self.root.after(6000, self.updateDF)
        self.anomBtn = tk.Button(self.topfram, text ="Anomalies", command=self.createAnomalyPage)
        self.anomBtn.pack(side=RIGHT)
        self.root.mainloop()

    def update_clock(self):
        now = time.strftime("%H:%M")
        self.label.configure(text=now)
        #self.root.after(1000, self.update_clock)
    
    def updatePKLoss(self):
        pk = packetLoss()
        new_text = f"Packet Loss: {pk[0]}%"
        ping = f"  Latency: {pk[1]} ms"
        self.packetL.configure(text=new_text)
        self.ping.configure(text=ping)
        self.updateOtherDF(pk[0],pk[1])
        self.update_clock()
        self.root.after(pingTime, self.updatePKLoss)

    #Packet Snigg Table
    def updateTable(self):
        self.table.redraw()
        self.df =netinfo.return_network()
        self.table.model.df = self.df
        self.root.after(packetSniffTime, self.updateTable)

    def startPKLoss(self):
        print("Starting")
        global packetSniffTime
        packetSniffTime = 1

        
        self.startBtn.configure(state=DISABLED)
        self.stopBtn.configure(state=ACTIVE)
        self.updateTable()

    def stopPKLoss(self):
        print("Stopping")
        global packetSniffTime
        packetSniffTime = 1000000000000000000
        self.startBtn.configure(state=ACTIVE)
        self.stopBtn.configure(state=DISABLED)
    
    def setupBTNS(self):
        self.stopBtn.configure(command= self.stopPKLoss)
        self.startBtn.configure(command=self.startPKLoss)

    def makeCanvas(self):
        fig = Figure(figsize=(5,6), dpi=100)
        self.ax = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, master=self.rightFrame)
        self.throughputDF = through.addUpDownToDF(self.throughputDF,uptime)
        self.throughputDF.plot(x="Time",y="X",ax=self.ax,title="Download Speed Over Time")
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)

    
    def updateCanvas(self):
        self.ax.clear()
        self.throughputDF.plot(x="Time",y="X",ax=self.ax,title="Download Speed Over Time")
        
        self.canvas.draw()
        self.root.after(canvasTime, self.updateCanvas)
        

    async def makePlot(self):
        global uptime
        uptime+=throughputtime
        self.throughputDF = through.addUpDownToDF(self.throughputDF,uptime)
        print(self.throughputDF)
        await asyncio.sleep(throughputtime*100)

    def periodicGuiUpdate(self):
        while True:
            try:
                
                fn = self.gui_queue.get_nowait()
                print("yo!!")
            except queue.Empty:
                break
            fn()
        self.root.after(1000, self.periodicGuiUpdate)

    def start_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(self.makePlot())
        loop.run_forever()
        
    def updateDF(self):
        self.throughputDF = through.addUpDownToDF(self.throughputDF,uptime)
        self.root.after(dfTime, self.updateDF)

    def updateOtherDF(self,pkLoss,ping):
        time_now = datetime.datetime.now().strftime("%H:%M:%S")
        self.otherDF.loc[len(self.otherDF.index)] = [ping,time_now] 
        
    def createAnomalyPage(self):
        newWindow = tk.Toplevel(self.root)
        packetLossAnom = findOutliers(self.otherDF)
        downAnom = findOutliers(self.throughputDF)
        
        packetlossLabel = tk.Label(newWindow, text = "Packet Loss Anomaly's")
        packlossanom = tk.Label(newWindow, text = str(packetLossAnom))
        #packlossanomTable = Table(newWindow, dataframe=packetLossAnom,showtoolbar=False, showstatusbar=False)

        downloadSpeedLabel = tk.Label(newWindow, text = "Download Speed Anomaly's")
        downloadanom = tk.Label(newWindow, text = str(downAnom))
        #downloadanom = Table(newWindow, dataframe=downAnom,showtoolbar=False, showstatusbar=False)

        packetlossLabel.pack()
        packlossanom.pack()
        #packlossanomTable.show()
        #packlossanomTable.pack()

        downloadSpeedLabel.pack()
        downloadanom.pack()

