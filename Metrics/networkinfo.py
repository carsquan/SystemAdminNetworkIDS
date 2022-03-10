from scapy.all import *
import socket
import struct
import binascii
import asyncio
import pandas as pd
from collections import Counter

# User information on the network (left side of screen)
filepath = "output.csv"
output = []
df = pd.DataFrame()

# gives us dest mac, src mac, dest IP, source IP 
async def sniff():
    # socket that tell us about the Linux packet interface, that the data is raw, and that we are interested in IP protocol 
    s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket. htons(0x0800))
        # receiving the packet from TCP/UDP
    packet = s.recvfrom(2048)
    ethernet_header = packet[0][0:14]
    eth_header = struct.unpack("!6s6s2s", ethernet_header)
    dest_mac = str(binascii.hexlify(eth_header[0])) 
    src_mac = str(binascii.hexlify(eth_header[1]))
    type =  str(binascii.hexlify(eth_header[2]))
    ipheader = packet[0][14:34]
    ip_header = struct.unpack("!12s4s4s", ipheader)
    src_ip = socket.inet_ntoa(ip_header[1])
    dest_ip = socket.inet_ntoa(ip_header[2])
    
    # Adding Dictionary
    dic = { "Source IP": src_ip, "Source Mac": src_mac,"Destinaton IP": dest_ip,"Destinaton MAC": dest_mac, "type": type,}

    return dic
        
def return_network():
    global df
    output.append(asyncio.run(sniff()))
    df = pd.DataFrame(output)
    return df


# Function to find bandwidth 
def bandwidth():

    return None 
    