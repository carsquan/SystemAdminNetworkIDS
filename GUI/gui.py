# !/usr/bin/python3  
from argparse import Action
import imp
from tkinter import *
from turtle import width  
from Metrics.packetLoss import packetLoss
import asyncio
import Metrics.networkinfo as netinfo
from pandastable import Table, TableModel


#Entering the event main loop  


import tkinter as tk
import time
packetSniffTime = 1
pingTime = 10000
height = 720
width = 1080

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
        self.df =netinfo.return_network()
        self.f = Frame(self.root, height=height, width=width/2)
        self.topfram = Frame(self.root, height=30, width=width)
        self.botFram.pack(side=BOTTOM,fill="x")
        
        self.startBtn = tk.Button(self.topfram, text ="Start", state=DISABLED)
        self.stopBtn = tk.Button(self.topfram, text ="Stop")
        self.startBtn.pack(side=LEFT)
        self.stopBtn.pack(side=LEFT)
        self.table = pt = Table(self.f, dataframe=self.df,showtoolbar=False, showstatusbar=False)
        self.topfram.pack(fill="x",side=TOP,expand=True)
        self.f.pack(fill="both",side=LEFT, expand=True)
        
        self.rightFrame.pack(fill="y",side=RIGHT, expand=True)
        pt.show()
        self.setupBTNS()
        self.update_clock()
        self.updateTable()
        self.updatePKLoss()
        self.root.mainloop()

    def update_clock(self):
        now = time.strftime("%H:%M")
        self.label.configure(text=now)
        self.root.after(1000, self.update_clock)
    
    def updatePKLoss(self):
        pk = packetLoss()
        new_text = f"Packet Loss: {pk[0]}%"
        ping = f"  Latency: {pk[1]} ms"
        self.packetL.configure(text=new_text)
        self.ping.configure(text=ping)
        self.root.after(pingTime, self.updatePKLoss)


    def updateTable(self):
        self.table.redraw()
        self.df =netinfo.return_network()
        self.table.model.df = self.df
        self.root.after(packetSniffTime, self.updateTable)

    def startPKLoss(self):
        print("Starting")
        global packetSniffTime
        packetSniffTime = 1

        self.updateTable()
        self.startBtn.configure(state=DISABLED)
        self.stopBtn.configure(state=ACTIVE)

    def stopPKLoss(self):
        print("Stopping")
        global packetSniffTime
        packetSniffTime = 1000000000000000000
        self.startBtn.configure(state=ACTIVE)
        self.stopBtn.configure(state=DISABLED)
    
    def setupBTNS(self):
        self.stopBtn.configure(command= self.stopPKLoss)
        self.startBtn.configure(command=self.startPKLoss)
        
