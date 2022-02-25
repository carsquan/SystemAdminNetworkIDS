from scapy.all import srp,Ether,ARP,conf
#Provides Mac and Ip based on port 
def arpPing(ip="192.168.1.0",port="24"):
    conf.verb=0
    ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=f"{ip}/{port}"),
                timeout=2)

    line = "\n------------------------------------\n"
    str =""
    str += "------------------------------------\n"
    str+="MAC & IP"
    str += "\n------------------------------------\n"
    print(str)
    for snd,rcv in ans:
        print(rcv.sprintf(r"%Ether.src% & %ARP.psrc%"))
        str+=rcv.sprintf(r"%Ether.src% & %ARP.psrc%")
        #print("\n")
        str+="\n"
    print(line)
    str+=line
    return str
