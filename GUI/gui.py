# !/usr/bin/python3  
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
height = 640
width = 930

class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry(f"{width}x{height}")
        self.botFram = Frame(self.root, height=30, width=width)
        self.label = tk.Label(self.botFram,text="")
        self.root.title('Network Monitor')
        self.packetL = tk.Label(self.botFram, text="0.00%")
        self.ping = tk.Label(self.botFram,text="0")
        #self.label.place(x=width-40,y=height-15,anchor=SW)
        #self.packetL.place(x=0,y=height-20,anchor=SW)
        #self.ping.place(x=130,y=height-20)
        self.label.pack(side=RIGHT)
        self.packetL.pack(side=LEFT)
        self.ping.pack(side=LEFT)
        self.df =netinfo.return_network()
        f = Frame(self.root, height=height, width=width/2)
        self.botFram.pack(side=BOTTOM,fill="x")
        f.pack(fill="y",side=LEFT)
        self.table = pt = Table(f, dataframe=self.df,showtoolbar=False, showstatusbar=False)
        pt.show()
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
        ping = f"Ping: {pk[1]} ms"
        self.packetL.configure(text=new_text)
        self.ping.configure(text=ping)
        self.root.after(pingTime, self.updatePKLoss)


    def updateTable(self):
        self.table.redraw()
        self.df =netinfo.return_network()
        self.table.model.df = self.df
        self.root.after(packetSniffTime, self.updateTable)
    
    def tableOptions(self):
        options = config.load_options()
        #options is a dict that you can set yourself
        options = {'colheadercolor':'green'}
        config.apply_options(options, self.table)

