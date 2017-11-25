import curses
import serial
import time
import signal

class TimeoutException(Exception):   # Custom exception class
    pass
def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException
signal.signal(signal.SIGALRM, timeout_handler)


class ArduinoDisplay(object):
    def __init__(self,baudrate=9600):
        self.test_without_screen=False #set to true for debugging curses
        self.test_without_arduino=False #set to true for debugging serial

        self.sample_data = 'G2L42.360344N71.094887W12:6.0'

        self.arduino=None
        self.incoming_scout=1
        self.was_data_received=False
        self.last_time_data_received=[time.localtime(),time.localtime()]
        self.scout_data=[['',''],['','']] #2D array - currently set up for two scouts
        self.processed_scout_data=[[(0,0,''),(0,0,''),(0,0,'')],[(0,0,''),(0,0,''),(0,0,'')]]

        if not self.test_without_screen:
            self.scr = curses.initscr()
            curses.halfdelay(5)           # How many tenths of a second are waited, from 1 to 255
            curses.noecho()               # Wont print the input
        if not self.test_without_arduino:
            self.arduino=serial.Serial('/dev/ttyACM0',baudrate)

    def place_data(self):
        # print 'scout '+str(self.incoming_scout)+' data', self.scout_data[self.incoming_scout-1]
        str_time = time.strftime("%H:%M:%S", self.last_time_data_received[self.incoming_scout-1])
        row = int(self.incoming_scout*3.5)
        print 'scout data:',self.scout_data
        if self.was_data_received:
            self.processed_scout_data[self.incoming_scout-1][0]= (row, 5, self.scout_data[self.incoming_scout-1][0])
            self.processed_scout_data[self.incoming_scout-1][1]= (row, 25, self.scout_data[self.incoming_scout-1][1])
            self.processed_scout_data[self.incoming_scout-1][2]= (row, 45, str(str_time))
        elif 'null' in self.scout_data[self.incoming_scout-1][0]:
            self.processed_scout_data[self.incoming_scout-1][0]= (row, 5, 'NO GPS SIGNAL')
            self.processed_scout_data[self.incoming_scout-1][1]= (row, 25, 'NO GPS SIGNAL')
            self.processed_scout_data[self.incoming_scout-1][2]= (row, 45, str(str_time))
        elif 'NO' in self.scout_data[self.incoming_scout-1]:
            self.processed_scout_data[self.incoming_scout-1][0] = (3, 5, 'NO CONNECTION')
            self.processed_scout_data[self.incoming_scout-1][1] = (7, 5, 'NO CONNECTION')
        else:
            pass
        print 'processed_scout_data: ',self.processed_scout_data


    def draw_screen(self):
        self.scr.clear()
        self.scr.addstr(1,2,'SCOUT 1 ------------------------------------------------------')
        self.scr.addstr(5,2,'SCOUT 2 ------------------------------------------------------')
        self.scr.addstr(10,0,'Current Time: '+time.strftime("%H:%M:%S",time.localtime()))
        # print(self.processed_scout_data)
        for scout_data in self.processed_scout_data:
            for dat in scout_data:
                self.scr.addstr(dat[0],dat[1],dat[2])
        self.scr.refresh()

    def process_incoming_data(self,transmitted=None):
        if 'null' not in transmitted and len(transmitted)==29:
            self.was_data_received=True
            # print 'TRANSMITTING:',transmitted
            self.incoming_scout = int(transmitted[transmitted.index('G')+1:transmitted.index('G')+2])
            location_n = transmitted[transmitted.index('L')+1:transmitted.index('N')]+' '+transmitted[transmitted.index('N')]
            location_w = transmitted[transmitted.index('N')+1:transmitted.index('W')]+' '+transmitted[transmitted.index('W')]
            self.last_time_data_received[self.incoming_scout-1] = time.localtime()
            self.scout_data[self.incoming_scout-1] = [location_n,location_w]
        elif 'null' in transmitted:
            self.was_data_received=False
            #maybe have it display warning that received bad data?
            # print 'transmitted: ',transmitted
            # self.incoming_scout=int(transmitted[transmitted.index('S')+1:transmitted.index('S')+2])
            # print self.incoming_scout
            # print ['GPS'+str(self.incoming_scout)+'null', 'GPS'+str(self.incoming_scout)+'null']
            try: #this is cheap but I don't care right now
                self.incoming_scout=int(transmitted[transmitted.index('S')+1:transmitted.index('S')+2])
                self.scout_data[self.incoming_scout-1]=['GPS'+str(self.incoming_scout)+'null', 'GPS'+str(self.incoming_scout)+'null']
            except:
                print 'EXCEPTED'
                self.scout_data[0] = ['FAULTY DATA', 'FAULTY DATA']
                self.scout_data[1] = ['FAULTY DATA', 'FAULTY DATA']
            print('NO GPS TRANSMITTED')
        elif 'NO CONNECTION' in transmitted:
            print('PROCESSING WITHOUT CONNECTION')
            self.was_data_received=False
            self.scout_data[0] = ['NO CONNECTION', 'NO CONNECTION']
            self.scout_data[1] = ['NO CONNECTION', 'NO CONNECTION']
        else:
            self.was_data_received=False
            print('NOPE')


    def run(self):
        if not self.test_without_screen:
            self.draw_screen()
        while True:
            # if not self.test_without_screen:
            #     char = self.scr.getch() # This blocks (waits) until the time has elapsed, or there is input to be handled
            if self.test_without_arduino:
                transmitted=self.sample_data
            else:
                signal.alarm(1)
                try:
                    transmitted = self.arduino.readline()[:-2]
                except TimeoutException:
                    self.incoming_scout= (self.incoming_scout+1)%2+1
                    transmitted='NO CONNECTION'
                else:
                    signal.alarm(0)

            print 'RECEIVED: ',transmitted
            self.process_incoming_data(transmitted)
            print 'scout '+str(self.incoming_scout)+' data', self.scout_data[self.incoming_scout-1]

            self.place_data()
            if not self.test_without_screen:
                self.draw_screen()
                self.scr.addstr(10,0,'Current Time: '+time.strftime("%H:%M:%S",time.localtime()))


if __name__ == '__main__':
    display = ArduinoDisplay(9600)
    display.run()
