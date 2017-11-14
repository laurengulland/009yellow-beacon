"""
For Software Architecture description:
    see Yellow 2.009 Google Drive > Tech Review > Electronics Design > Queen Software > Queen Software Architecture
"""

import pandas as pd
import numpy as np
import time
import json
import serial

from mvp2.0_view.py import GUI
from mvp2.0_model.py import Scouts

class Controller(object):
    def __init__(self):
        #create model object
        #create gui object
        #set up all the variables!
        self.screen_location = [(0,0),(1,1)] #[(top left), (bottom right)]
        self.something = 0
        self.hive_queue = []
        #Load constants from json file (UNTESTED)
        json_data = json.load(open('mvp2.0_constants.json'))
        self.screen_width,self.screen_length = json_data["screen_width"],json_data["screen_length"]
        self.port = serial.Serial('COM4') #MUST SELECT CORRECT PORT ON TABLET
        time.sleep(1) #wait after establishing serial connection before proceeding

    def construct_scout_displays(self,range=[(0,0),(1,1)]):
        #figure this function out
        #interact with model, via data_within_range()?
        pass

    def parse_inputs(self, input):
        #Parse input and decide whether GPS or button is most accurate
        pass

    def parse_gps_inputs(self):
        #parse gps inputs
        #do action depending on the button:
            #add new scout gps tracks/points to model
            #add waypoints to model
        pass

    def parse_button_presses(self):
        #parse button inputs
        #do action depending on the button:
            #send to view
            #force transmit to hive (actuate transmit_data() or whatever)
        pass

    def transmit_or_package_data(self):
        #package data to transmit?? This may not be the right function
        pass

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
