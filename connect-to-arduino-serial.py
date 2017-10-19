#!usr/bin/python
# $ pip install pyserial
import serial
import time
import curses

arduino=serial.Serial('/dev/ttyACM0',9600)
last_time=None
test=False
scr = curses.initscr()
curses.halfdelay(5)           # How many tenths of a second are waited, from 1 to 255
curses.noecho()               # Wont print the input
scr.clear()
scr.addstr(0,0,'initializing')


def update_screen(scout_unit, (n,w), new_time, last_time):
    scr.clear()
    scr.addstr(0,0,scout_unit)

while True:
    scr.addstr(0,0,'initializing')
    sample='G2L42.360344N71.094887W12:6.0'
    transmitted = arduino.readline()[:-2]
    if test:
        transmitted=sample
    if len(transmitted)>=29:
        scout_unit = 'Scout '+transmitted[transmitted.index('G')+1:transmitted.index('G')+2]
        location_n = transmitted[transmitted.index('L')+1:transmitted.index('N')]+' '+transmitted[transmitted.index('N')]
        location_w = transmitted[transmitted.index('N')+1:transmitted.index('W')]+' '+transmitted[transmitted.index('W')]
        new_time = transmitted[transmitted.index('W')+1:]

        # print scout_unit,'\t',location_n,', ',location_w,'\t',new_time
        update_screen(scout_unit, (location_n,location_w),new_time,last_time)
        last_time = new_time
    elif 'null' in transmitted:
        #don't update
        scr.clear()
        scr.addstr(0,0,'no GPS transmission')
        # print('no GPS transmission')
    # print(str(it)+', '+transmitted)


#
#
# while True:
#     char = scr.getch()        # This blocks (waits) until the time has elapsed,
#                               # or there is input to be handled
#     scr.clear()               # Clears the screen
#     if char != curses.ERR:    # This is true if the user pressed something
#         scr.addstr(0, 0, chr(char))
#     else:
#         scr.addstr(10, 10, "Waiting")
