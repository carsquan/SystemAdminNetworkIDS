from pythonping import ping

print(ping('74.125.136.113', timeout=1, count=1,))

pkt_loss = 0
pkt_total = 0

async def packetLoss():
    global pkt_loss
    global pkt_total

    str = ping('74.125.136.113', timeout=1, count=1,)
  
    pkt_total+= 1
  
    if str[2] == 'q':
        pkt_loss+= 1

    # returns rate of packet loss
    return pkt_loss / pkt_total


