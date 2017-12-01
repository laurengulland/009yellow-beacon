import serial
import model
import time

class Controller(object):
    def __init__(self):
        self.port = serial.Serial('COM4') #MUST SELECT CORRECT PORT ON TABLE
        self.model = model.Model()

    def run(self):
        for i in range(6):
            data = self.port.read(80)
            self.store_data(data)

    def store_data(self, content):
        is_poi = content[0]
        is_poi = (is_poi == 0x01)
        queen = content[1]
        if queen == 0xFF:
            queen = None
        else:
            queen = str(queen)
        latitude = self.get_signed_coord(content[2:7])
        longitude = self.get_signed_coord(content[7:12])
        scout = content[12]
        if scout == 0xFF:
            scout = None
        else:
            scout = str(scout)
        timestamp = self.get_time_from_bytes(content[13:17])
        is_current = (content[17]==0x01)
        done = False
        description_end = 18
        while not done:
            if content[description_end] == 0:
                done = True
            else:
                description_end +=1
        if description_end == 18:
            description = None
        else:
            description = content[18:description_end]
        self.model.add_hive_data_point(scout, queen, is_poi,is_current,latitude,longitude, description,timestamp)

    def get_time_from_bytes(self, timebytes):
        return timebytes[0]+timebytes[1]*256+timebytes[2]*256**2+timebytes[3]*256**3

    def get_signed_coord(self, coord_bytes):
        return (coord_bytes[0]+coord_bytes[1]*256+coord_bytes[2]*256**2+coord_bytes[3]*256**3)*(-1)**(coord_bytes[4]-1) *10**(-6)

if __name__ == '__main__':
    controller = Controller()
    controller.run()
