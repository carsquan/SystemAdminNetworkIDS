# !/usr/bin/python3  
import imp
from tkinter import *
from turtle import width  
from Metrics.packetLoss import packetLoss
import asyncio

#Entering the event main loop  


import tkinter as tk
import time

pingTime = 10000
height = 320
width = 640

class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry(f"{width}x{height}")
        self.label = tk.Label(text="")
        self.packetL = tk.Label(text="0.00%")
        self.ping = tk.Label(text="0")
        self.label.place(x=width-40,y=height-20)
        self.packetL.place(x=0,y=height-20)
        self.ping.place(x=130,y=height-20)
        self.update_clock()
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


