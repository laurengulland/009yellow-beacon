# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 19:54:10 2017

@author: Joseph
"""

import serial
import time

def get_signed_coord(coord_bytes):
    hexstring = ''
    for coord_byte in coord_bytes[0:-1]:
        bytehex = str(hex(coord_byte))[2:]
        if len(bytehex)==1:
            bytehex = '0'+bytehex
        hexstring = bytehex+hexstring
    output = int(hexstring,16)
    output = float(output)/(10**6)
    if coord_bytes[-1]==0x02:
        output = -output
    return output

def get_poi_packet(content, trtime, next_poi_id):
    packet = bytearray(83)
    packet[0] = 0x7e
    packet[1] = 16
    packet[2] = 0x03
    packet[3] = 0x01
    poi_hex = hex(next_poi_id)[2:]
    next_poi_id +=1
    while len(poi_hex)<4:
        poi_hex = '0'+poi_hex
    packet[4] = int(poi_hex[2:],16)
    packet[5] = int(poi_hex[0:2],16)
    packet[6:18] = content
    return packet

def get_scout_payload(content,trtime):
    payload = bytearray(15)
    payload[0:11]=content[0:11]
    payload[11:15] = time_int_to_bytearray(trtime)
    return payload


def time_int_to_bytearray(trtime):
    hexstring = hex(trtime)[2:]
    return bytearray([
               int(hexstring[6:8],16),
               int(hexstring[4:6],16),
               int(hexstring[2:4],16),
               int(hexstring[0:2],16),
    ])


next_poi_id = 241
port = serial.Serial('/dev/ttyACM0')
while True:
    print(port.read(1).hex())
'''
time.sleep(2)
packet = port.read(83)
port.close()
length = packet[1]
packtype = packet[2]
content = bytearray(packet[3:2+length])
lat = get_signed_coord(content[0:5])
long = get_signed_coord(content[5:10])
scout_id = content[10]
poi = content[11]
is_poi = poi != 0x00
print(get_poi_packet(content,0,next_poi_id).hex())
print(get_scout_payload(content,int(time.time())).hex())
print(hex(int(time.time())))
# add to model
#self.scouts.add_data_point(scout_id, trtime,(lat,lon),is_poi)
# add to queue
#if is_poi:
#    poi_queue.append(self.get_poi_packet(content, trtime))
#else:
#    packet = self.get_scout_packet(content,trtime)
#    self.add_packet_to_scout_queue(packet)

print(length)
print(packtype)
print(content.hex())
print(lat)
print(long)
'''
