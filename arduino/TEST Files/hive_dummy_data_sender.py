# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 19:41:46 2017

@author: Joseph
"""

#let's write a script for hive data!

import serial

packetqueue = [
    bytearray([0x7e,0x17,0x03,0x00]+[0xaa]*15+[0x0]*64),
    bytearray([0x7e,16,0x03,0x01]+[0xaa]*14+[0x0]*65),
    bytearray([0x7e,1,0x03]+[0x00]*80)
]

port = serial.Serial('COM9')
while packetqueue != []:
    packet = port.read(83)
    print(packet.hex())
    if packet[2] == 0x02:
        port.write(packetqueue.pop(0))
        print('Sending new packet')
    if packet[2] == 0x00:
        packet[2] == 0x03
        packetqueue.append(packet)
while 1==1:
    packet = port.read(83)
    print(packet.hex())
port.close()
