/*
 * Queen Serial: SH -> 0x13A200, SL -> 0x41515876
 * Scout 1 Serial: SH -> 0x13A200, SL -> 0x4164D65A
 */

//Libraries
#include <XBee.h> //XBee library
#include <Adafruit_GPS.h> //Adafruit GPS library

#define XBeeSerial Serial1 //Teensy Ports 0/RX1 and 1/TX1
XBee xbee = XBee(); //Create XBee object
XBeeResponse response = XBeeResponse();
ZBRxResponse rx = ZBRxResponse();

uint8_t payload[] = { 0, 0, 0, 0, 0, 0 };
XBeeAddress64 addr64 = XBeeAddress64(0x13A200, 0x41515876);
ZBTxRequest zbTx = ZBTxRequest(addr64, payload, sizeof(payload));
ZBTxStatusResponse txStatus = ZBTxStatusResponse();


#define GPSSerial Serial2 //Teensy Ports 9/RX2 and 10/TX2
// Connect to the GPS on the hardware port
Adafruit_GPS GPS(&GPSSerial);
     
// Set GPSECHO to 'false' to turn off echoing the GPS data to the Serial console
// Set to 'true' if you want to debug and listen to the raw GPS sentences
#define GPSECHO false

uint32_t timer = millis();
uint32_t timer1 = millis();
float Pi = 3.14159;

int count = 0x00;

float GPSlat = 42.047843;
float GPSlon = 21.308923;

long latTX;
long lonTX;

String currLatLong;
String timeString;
String compassString;
String stringOut;

int statusLed = 13;

void flashLed(int pin, int times, int wait) {

  for (int i = 0; i < times; i++) {
    digitalWrite(pin, HIGH);
    delay(wait);
    digitalWrite(pin, LOW);

    if (i + 1 < times) {
      delay(wait);
    }
  }
}

void setup() {
  Serial.begin(9600);
    GPS.begin(9600);
  // uncomment this line to turn on RMC (recommended minimum) and GGA (fix data) including altitude
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  // uncomment this line to turn on only the "minimum recommended" data
  //GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY);
  // For parsing data, we don't suggest using anything but either RMC only or RMC+GGA since
  // the parser doesn't care about other sentences at this time
  // Set the update rate
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ); // 1 Hz update rate
  // For the parsing code to work nicely and have time to sort thru the data, and
  // print it out we don't suggest using anything higher than 1 Hz
     
  // Request updates on antenna status, comment out to keep quiet
  GPS.sendCommand(PGCMD_ANTENNA);

  delay(1000);

  XBeeSerial.begin(9600);
  xbee.setSerial(XBeeSerial);
  pinMode(statusLed, OUTPUT);
}

void loop() {
  xbee.readPacket();
  if(xbee.getResponse().isAvailable()){
    if(xbee.getResponse().getApiId() == ZB_RX_RESPONSE){
      flashLed(statusLed, 1,100);
      xbee.getResponse().getZBRxResponse(rx);
      if(rx.getDataLength() == 5){
        char c = GPS.read();
        if (GPS.newNMEAreceived()) {
            if (!GPS.parse(GPS.lastNMEA())) // this also sets the newNMEAreceived() flag to false
              return; // we can fail to parse a sentence in which case we should just wait for another
          }
//          float GPSlat = GPS.latitude;
//          float GPSlon = GPS.longitude;
          latTX = (long) (GPSlat*1000000);
          lonTX = (long) (GPSlon*1000000);
          payload[0] = latTX & 255;
          payload[1] = (latTX >> 8) & 255;  
          payload[2] = (latTX >> 16) & 255;
          payload[3] = (latTX >> 24) & 255;
          payload[4] = 0x01;
          payload[5] = count;
          count += 1;
          if (count == 0xFF) {
            count = 0x00;
          }
          xbee.send(zbTx);
          flashLed(statusLed,5,50);
      }
    }
  }
}
