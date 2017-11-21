# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 16:42:23 2017

@author: Joseph
"""

def packet_from_hex_string(pstring):
    stringarray = []
    for i in range(83):
        stringarray.append(pstring[2*i:2*i+2])
    outstring = 'uint8_t packet[] = {'
    for substring in stringarray:
        outstring = outstring + '0x'+substring+', '
    outstring = outstring[0:-2] + '};'
    return outstring

def fill_hex_string(string):
    return string + '0'*(166-len(string))

def button_press_packet(button):
    string = '7e02010' + str(button)
    return packet_from_hex_string(fill_hex_string(string))

def joystick_packet(direction):
    if direction == 'up':
        varstring = '01ff0100'
    elif direction == 'down':
        varstring = '02ff0100'
    elif direction == 'right':
        varstring = '010001ff'
    elif direction == 'left':
        varstring == '010002ff'
    string = '7e060106'+varstring
    return packet_from_hex_string(fill_hex_string(string))

def gps_scout_packet(lat,long,scoutnum,poi=False):
    if poi:
        poi = '1'
    else:
        poi = '0'
    return packet_from_hex_string(fill_hex_string('7e0d00'+number_to_packet_hex(lat)+number_to_packet_hex(long)+'0'+str(scoutnum)+'0'+poi))

def number_to_packet_hex(number):
    if number<0:
        signbit='02'
        number = abs(number)
    else:
        signbit='01'
    number = number*10**6
    number = int(number)
    hexstring = hex(number)[2:]
    while len(hexstring)<8:
        hexstring = '0'+hexstring
    hexarray = []
    for i in range(4):
        hexarray.append(hexstring[2*i:2*i+2])
    return ''.join(reversed(hexarray)) + signbit

def hive_data_request_packet():
    return packet_from_hex_string(fill_hex_string('7e0102'))

def packets_to_c(packets):
    string = 'void setup() {Serial.begin(9600);} '
    string = string + ' void loop() { '
    for packet in packets:
        string =string+' { '+packet+' for(int i = 0; i < 83; i++) {Serial.write(packet[i]);} delay(5000); } '
    string = string + ' } '
    return string

#packet_from_hex_string('7e0d000b598602017cc43c040201010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
#print(packet_from_hex_string(button_press_hex_string(0)))
print(packets_to_c([
    gps_scout_packet(42.358306, -71.094515,0,True),
    gps_scout_packet(42.358306, -71.094515,0,True),
    gps_scout_packet(42.358306, -71.094515,0,False),
    gps_scout_packet(42.358306, -71.094515,0,False),
    gps_scout_packet(42.358380,-71.094680,0,False),
    gps_scout_packet(42.358360,-71.094700,0,False),
    gps_scout_packet(42.358340,-71.094700,0,False),
    gps_scout_packet(42.358380,-71.094660,0,True),
    #button_press_packet(0),
    #joystick_packet('up'),
    #hive_data_request_packet()
]))
