import curses
import serial
import time


class ArduinoDisplay(object):
    """docstring for ."""
    def __init__(self,baudrate=9600):
        self.test_without_screen=False #set to true for debugging curses
        self.test_without_arduino=False #set to true for debugging serial

        self.sample_data = 'G2L42.360344N71.094887W12:6.0'
        self.output = 'should be overwritten'
        self.it=0

        self.arduino=None
        self.incoming_scout=1
        self.was_data_received=False
        self.last_time_data_received=[time.localtime(),time.localtime()]
        self.scout_data=[[],[]] #2D array - currently set up for two scouts
        self.processed_scout_data=[[(0,0,''),(0,0,''),(0,0,'')],[(0,0,''),(0,0,''),(0,0,'')]]

        if not self.test_without_screen:
            self.scr = curses.initscr()
            curses.halfdelay(5)           # How many tenths of a second are waited, from 1 to 255
            curses.noecho()               # Wont print the input
        if not self.test_without_arduino:
            self.arduino=serial.Serial('/dev/ttyACM0',baudrate)

    def place_data(self):
        print 'scout '+str(self.incoming_scout)+' data', self.scout_data[self.incoming_scout-1]
        str_time = time.strftime("%H:%M:%S", self.last_time_data_received[self.incoming_scout-1])
        row = int(self.incoming_scout*3.5)
        if self.was_data_received:
            self.processed_scout_data[self.incoming_scout-1][0]= (row, 5, self.scout_data[self.incoming_scout-1][0])
            self.processed_scout_data[self.incoming_scout-1][1]= (row, 25, self.scout_data[self.incoming_scout-1][1])
            self.processed_scout_data[self.incoming_scout-1][2]= (row, 45, str(str_time))
        else:
            self.processed_scout_data[self.incoming_scout-1][0]= (row, 5, 'NO GPS RECEIVED')
            self.processed_scout_data[self.incoming_scout-1][1]= (row, 25, 'NO GPS RECEIVED')
            self.processed_scout_data[self.incoming_scout-1][2]= (row, 45, str(str_time))

    def draw_screen(self):
        self.scr.clear()
        self.scr.addstr(1,2,'SCOUT 1 ------------------------------------------------------')
        self.scr.addstr(5,2,'SCOUT 2 ------------------------------------------------------')
        self.scr.addstr(10,0,'Current Time: '+time.strftime("%H:%M:%S",time.localtime()))

        print self.processed_scout_data
        for scout_data in self.processed_scout_data:
            for dat in scout_data:
            # self.scr.addstr(11,11,'AAAAAA')
            # self.scr.addstr(2,0,str(dat[2]))
                print 'DAT',dat
                self.scr.addstr(dat[0],dat[1],dat[2])
        self.scr.refresh()

    def process_incoming_data(self,transmitted=None):
        if 'null' not in transmitted and len(transmitted)>25:
            self.was_data_received=True
            print 'TRANSMITTING:',transmitted
            # self.scr.addstr(0,0,transmitted)
            self.incoming_scout = int(transmitted[transmitted.index('G')+1:transmitted.index('G')+2])
            location_n = transmitted[transmitted.index('L')+1:transmitted.index('N')]+' '+transmitted[transmitted.index('N')]
            location_w = transmitted[transmitted.index('N')+1:transmitted.index('W')]+' '+transmitted[transmitted.index('W')]
            self.last_time_data_received[self.incoming_scout-1] = time.localtime()
            # location_n = 'location_n_value'
            # location_w = 'location_w_value'
            # new_time = '00:00.00'
            self.scout_data[self.incoming_scout-1] = [location_n,location_w]
        elif 'null' in transmitted:
            self.was_data_received=False
            #maybe have it display warning that received no GPS data
            try:
                self.incoming_scout=int(transmitted[transmitted.index('S')+1:transmitted.index('S')+2])
            except:
                pass
            print('NO GPS TRANSMITTED')
            pass #implement later
        else:
            self.was_data_received=False
            print('NOPE')
            pass #implement later

    def run(self):
        while True:
            self.it+=1
            if not self.test_without_screen:
                char = self.scr.getch() # This blocks (waits) until the time has elapsed, or there is input to be handled
            if self.test_without_arduino:
                transmitted=self.sample_data
            else:
                transmitted = self.arduino.readline()[:-2]
            # print 'RECEIVED: ',transmitted
            self.process_incoming_data(transmitted)
            print 'scout '+str(self.incoming_scout)+' data', self.scout_data[self.incoming_scout-1]

            self.place_data()
            if not self.test_without_screen:
                self.draw_screen()


if __name__ == '__main__':
    display = ArduinoDisplay(9600)
    display.run()
