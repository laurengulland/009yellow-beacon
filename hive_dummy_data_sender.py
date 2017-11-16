# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 19:41:46 2017

@author: Joseph
"""

#let's write a script for hive data!

import serial

packetqueue = [
    bytearray([0x7e,17,0x03,0x00]+[0xaa]*15+[0x0]*64),
    bytearray([0x7e,16,0x03,0x01]+[0xaa]*14+[0x0]*65),
    bytearray([0x7e,1,0x03]+[0x00]*80)
]

port = serial.Serial('COM4')
while packetqueue != []:
    packet = port.read(83)
    if packet[2] == 0x02:
        port.write(packetqueue.pop(0))
port.close()