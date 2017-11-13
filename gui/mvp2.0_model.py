import numpy as np
from tables import *

class Scouts(object):
    def __init__(self):
        self.something = 0
        h5file = open_file("tutorial1.h5", mode = "w", title = "Test file")
        table = h5file.create_table(group, 'readout', Particle, "Readout example")
        self.table = table
        #instantiate empty dataframe
        #create file saving or whatever

    def add_data_point(self,scout_id,time,gps_location,is_point_of_interest):
        row = table.row
        row['scout_id'] = scout_id
        row['time'] = time
        row['gps_location'] = gps_location
        row['is_point_of_interest'] = is_point_of_interest
        row.append()
        table.flush()

    # condition = '(name == b"Particle:      5") | (name == b"Particle:      7")'
    def data_from_time(self,begin_time,last_time):
        names = [ x['name'] for x in table.where("""(TDCcount > 3) & (20 <= pressure) & (pressure < 50)""") ]
        pass

    def data_from_scout(self,scout_id):
        pass

    def current_locations(self,number_of_scouts):
        pass

    def data_within_range(self,top_left,bottom_right):
        pass
