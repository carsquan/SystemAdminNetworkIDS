# !/usr/bin/python3  
import imp
from tkinter import *  
from Metrics.packetLoss import packetLoss
import asyncio

#Entering the event main loop  


import tkinter as tk
import time

class App():
    def __init__(self):
        self.root = tk.Tk()
        self.label = tk.Label(text="")
        self.packetL = tk.Label(text="0.00%")
        self.ping = tk.Label(text="0.00%")
        self.label.pack()
        self.packetL.pack()
        self.ping.pack()
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
        ping = f"Ping: {pk[1]}"
        self.packetL.configure(text=new_text)
        self.ping.configure(text=ping)
        self.root.after(10000, self.updatePKLoss)


def runGUI():

    top = Tk()
    t = Label(top)
    t.pack()
    e1 = Entry(top)
    e1.pack()
    e2 = Entry(top)
    e2.pack()

    def my_after(): 
        new_text = packetLoss()

        t.config(text=new_text)

        # call again after 100 ms
        top.after(10, my_after)
        
    # call first time 
    my_after()

    # call first time after 100 ms
    #top.after(100, my_after)

    top.mainloop()
  