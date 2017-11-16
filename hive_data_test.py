# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 22:08:51 2017

@author: Joseph
"""

#hive data testing
#simulates data the Hive receives

def packet_from_hex_string(pstring):
    stringarray = []
    for i in range(80):
        stringarray.append(pstring[2*i:2*i+2])
    outstring = 'uint8_t packet[] = {'
    for substring in stringarray:
        outstring = outstring + '0x'+substring+', '
    outstring = outstring[0:-2] + '};'
    return outstring
 
def fill_hex_string(string):
    return string + '0'*(160-len(string))
    
def packets_to_c(packets):
    string = 'void setup() {Serial.begin(9600);} '
    string = string + ' void loop() { '
    for packet in packets:
        string =string+' { '+packet+' for(int i = 0; i < 80; i++) {Serial.write(packet[i]);} delay(5000); } '
    string = string + ' } '
    return string
    
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
    
def time_int_to_hex(trtime):
        '''
        helper function to convert integer seconds from epoch to hex.
        uses same least-significant-first convention as lat/long
        '''
        hexstring = hex(trtime)[2:]
        return hexstring[6:8] + hexstring[4:6] + hexstring[2:4] + hexstring[0:2]

def single_scout_payload(lat,lon,scoutnum,trtime):
    return number_to_packet_hex(lat)+number_to_packet_hex(lon)+'0'+str(scoutnum)+time_int_to_hex(trtime)

def hive_scouts_packet(scouts):
    if len(scouts)>5:
        raise Exception
    out = '00'
    for scout in scouts:
        out = out + single_scout_payload(scout[0],scout[1],scout[2],scout[3])
    return packet_from_hex_string(fill_hex_string(out))
    
def hive_poi_packet(poi_id,lat,lon,scout_id,category=1,description=''):
    hexstring = hex(poi_id)[2:]
    out = '01'
    while len(hexstring)<4:
        hexstring = '0'+hexstring
    for i in range(2):
        out = out + hexstring[2*i:2*i+2]
    out = out + number_to_packet_hex(lat) + number_to_packet_hex(lon)+'0'+str(scout_id)+'0'+str(category)
    return packet_from_hex_string(fill_hex_string(out + bytes(description,'ascii').hex()))
    
print(packets_to_c(
    [hive_scouts_packet([
    [42.359051,-71.091324,1,1510717000],
    [42.358340,-71.094600,0,1510717000],
    [42.359151,-71.091224,1,1510717010],
    [42.358240,-71.094700,0,1510717010]]),
    hive_poi_packet(0,42.358340,-71.094600,0,1,'')]))