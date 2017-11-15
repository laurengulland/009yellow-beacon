"""
For Software Architecture description:
    see Yellow 2.009 Google Drive > Tech Review > Electronics Design > Queen Software > Queen Software Architecture
"""

import pandas as pd
import numpy as np
import time
import json
import serial

from mvp2_0_view.py import GUI
from mvp2.0_model.py import Scouts

class Controller(object):
    def __init__(self):
        #create model object
        #create gui object
        #set up all the variables!
        self.screen_location = [(0,0),(1,1)] #[(top left), (bottom right)]
        self.something = 0
        self.scout_queue = [] #store as list of bytearray objects
        self.poi_queue = [] #store as list of bytearray objects
        self.scouts = Scouts() #initialize model
        self.next_poi_id = 0 #keep track of unused poi ids
        #Load constants from json file (UNTESTED)
        json_data = json.load(open('mvp2.0_constants.json'))
        self.screen_width,self.screen_height = json_data["screen_width"],json_data["screen_height"]
        #initialize serial communication
        self.port = serial.Serial('COM4') #MUST SELECT CORRECT PORT ON TABLET
        time.sleep(1) #wait after establishing serial connection before proceeding

    def construct_scout_displays(self,range=[(0,0),(1,1)]):
        #figure this function out
        #interact with model, via data_within_range()?
        pass

    def parse_inputs(self):
        '''
        decide correct course of action
        '''
        #Parse input and decide whether GPS or button is most accurate
        packet = self.port.read(83)
        length = packet[1]
        packtype = packet[2]
        content = bytearray(packet[3:2+length])
        if packtype == 0x00:
            self.parse_gps_inputs(content)
        if packtype == 0x01:
            self.parse_button_presses(content)
        if packtype == 0x02:
            self.transmit_data()

    def parse_gps_inputs(self, content):
        '''
        parses payload of gps input
        '''
        trtime = int(time.time()) #time since epoch rounded to the second
        lat = self.get_signed_coord(content[0:5])
        lon = self.get_signed_coord(content[5:10])
        scout_id = content[10]
        poi = content[11]
        is_poi = poi != 0x00
        # add to model
        self.scouts.add_data_point(scout_id, trtime,(lat,lon),is_poi)
        # add to queue
        if is_poi:
            poi_queue.append(self.get_poi_packet(content))
        else:
            payload = self.get_scout_payload(content,trtime)
            self.add_payload_to_scout_queue(payload)

    def add_payload_to_scout_queue(self, payload):
        '''
        if there's room in the last bytearray, add it there
        otherwise, create a new packet
        '''
        if len(payload)!=15:
            raise Exception
        if self.scout_queue == [] or self.scout_queue[-1][1]>75:
            packet = bytearray(83)
            packet[0] = 0x7e
            packet[1] = 17
            packet[2] = 0x03
            packet[3] = 0x00
            packet[4:19] = payload
        else:
            packet = self.scout_queue[-1]
            packet[packet[1]+2:packet[1]+17] = payload
            packet[1] = packet[1]+15

    def get_poi_packet(self,content):
        '''
        build the complete poi package, sans description
        '''
        packet = bytearray(83)
        packet[0] = 0x7e
        packet[1] = 16
        packet[2] = 0x03
        packet[3] = 0x01
        poi_hex = hex(self.next_poi_id)[2:]
        self.next_poi_id +=1
        while len(poi_hex)<4:
            poi_hex = '0'+poi_hex
        packet[4] = int(poi_hex[2:],16)
        packet[5] = int(poi_hex[0:2],16)
        packet[6:18] = content
        return packet

    def get_scout_payload(self,content,trtime):
        '''
        use info from content and transmission time to log scout info
        '''
        payload = bytearray(15)
        payload[0:11] = content[0:11]
        payload[11:15] = self.time_int_to_bytearray(trtime)

    def time_int_to_bytearray(self,trtime):
        '''
        helper function to convert integer seconds from epoch to hex.
        uses same least-significant-first convention as lat/long
        '''
        hexstring = hex(trtime)[2:]
        return bytearray([
               int(hexstring[6:8],16),
               int(hexstring[4:6],16),
               int(hexstring[2:4],16),
               int(hexstring[0:2],16),
               ])

    def get_signed_coord(self, coord_bytes):
        '''
        helper function to convert coordinate bytes to numbers
        '''
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

    def parse_button_presses(self, content):
        '''
        takes in content as a bytearray and calls the necessary function, which might be in controller or view
        '''
        #need more information about what is being displayed (i.e. what the button press means)
        #specifically, we need a menu_map that details what each button press would do at a given point in the UI
        return #because menu_map does not exist
        if content[0]<6:
            self.menu_map[content[0]]()
        else:
            x = content[2]
            y = content[4]
            if x>y:
                if content[1] == 0x02:
                    self.menu_map[(content[0],'left')]()
                else:
                    self.menu_map[(content[0],'right')]()
            else:
                if content[3]==0x02:
                    self.menu_map[(content[0],'down')]()
                else:
                    self.menu_map[(content[0],'up')]()

    def transmit_data(self):
        '''
        send packets from queues, if available.
        sends scout packets first, then poi.
        sends no-content packet if nothing to send.
        '''
        if self.scout_queue == []:
            if self.poi_queue == []:
                packet = bytearray(83)
                packet[0]=0x7e
                packet[1]=1
                packet[2]=0x03
            else:
                packet = self.poi_queue.pop(0)
        else:
            packet = self.scout_queue.pop(0)
        self.port.write(packet)

    def update_view(self):
        #update the view with the current range
        #calls view.render()?
        pass

    def run(self):
        pass
        #LOOOOOOP:
            #read inputs from serial, send to parse_inputs()
            #trigger update for view if necessary?
            # initiate transmissions?
        #quit everythin on shutdown



class Scout_Display(object):
    def __init__(self,scout_id=0):
        self.id = scout_id
        self.current_position = []
        self.positions = []

if __name__ == '__main__':
    controller = Controller()
    controller.run()
