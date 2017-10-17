# Connecting the Raspberry Pi to Arduinos

## Physical connection

All you need is a USB to USB-B cable. Plug them into each other. It's that easy.

## Software Integration

As long as your Arduino has the code you want it to run uploaded to it, it should be automatically running and streaming data to Serial. Usually, you pick that up via the Arduino IDE's Serial Monitor on your laptop if you're connected to it via USB. If your Arduino is connected to the RasPi, the RasPi is picking up that data via USB!

To print all the information the Arduino is passing via Serial to the RasPi, run:
```bash
$ cd 009yellow-beacon/
$ python connect-to-arduino-serial.py
```
To exit the program, just Ctrl-C from the RasPi keyboard.

If you want this program to do more complex things, just edit the [Python script](https://github.com/laurengulland/009yellow-beacon/blob/master/connect-to-arduino-serial.py), which is currently extremely simple.
