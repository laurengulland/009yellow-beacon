# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 19:54:10 2017

@author: Joseph
"""

import serial
import time

port = serial.Serial('COM4')
time.sleep(2)
for i in range(0,5):
    output = port.read(83)
    print(output.hex())
port.close()