# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 19:41:46 2017

@author: Joseph
"""

#let's write a script for hive data!

import serial

packetqueue = []

port = serial.Serial('COM9',9600)
while 1==1:
    packet = port.read(83)
    print('Read')
    print(packet.hex())
    packetarray = bytearray(packet)
    if packet[2] == 0x02:
        if len(packetqueue)==0:
            packetqueue.append(bytearray([0x7e,1,0x03]+[0x00]*80))
        port.write(packetqueue.pop(0))
        print('Sending new packet')
    if packet[2] == 0x00:
        packetarray[2] = 0x03
        packetqueue.append(packetarray)
while 1==1:
    packet = port.read(83)
    print('Read')
    print(packet.hex())
port.close()
