from pythonping import ping
import asyncio
import os


pkt_loss = 0
pkt_total = 0

def packetLoss():
    global pkt_loss
    global pkt_total

    str = ping('74.125.136.113', timeout=1, count=1,)
  
    pkt_total+= 1
  
    if not str.success:
        pkt_loss+= 1

    # returns rate of packet loss
    return [pkt_loss / pkt_total,str.rtt_avg_ms]
