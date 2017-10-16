#!usr/bin/python
# $ pip install pyserial
import serial
ser=serial.Serial('/dev/ttyACM0',9600)
while True:
    x = ser.readline()
    print(x)
