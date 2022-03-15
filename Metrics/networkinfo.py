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
    dest_mac = macConvert(str(binascii.hexlify(eth_header[0]))[2:14])
    src_mac = macConvert(str(binascii.hexlify(eth_header[1]))[2:14])
    type =  packetType(binascii.hexlify(eth_header[2]))
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

def macConvert(mac):
    return f"{mac[:2]}:{mac[2:4]}:{mac[4:6]}:{mac[6:8]}:{mac[8:10]}:{mac[10:12]}"

def packetType(type):
    if type == b'0800':
        return "IP4"
    else:
        return str(type)[2:6]
    