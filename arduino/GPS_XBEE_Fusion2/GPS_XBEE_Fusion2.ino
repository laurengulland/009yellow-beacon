//GPS Library
#include <Adafruit_GPS.h>

//XBee Library
#include <XBee.h>

//XBee Preamble

#define XBeeSerial Serial1 //Teensy Ports 0/RX1 and 1/TX1

//Create XBee object
XBee xbee = XBee();

uint8_t payload[] = { 0, 0, 0, 0, 0, 0 };

// SH + SL Address of receiving XBee - Need to test mesh
XBeeAddress64 addr64 = XBeeAddress64(0x13A200, 0x41515876);
ZBTxRequest zbTx = ZBTxRequest(addr64, payload, sizeof(payload));
ZBTxStatusResponse txStatus = ZBTxStatusResponse();

//LED Debugging Initialization
int statusLed = 13;
int errorLed = 14;
int buttonValue;
int buttonPin = 15;
int buttonLed = 16;

int count = 0x00;

volatile unsigned long last_interrupt;

unsigned long latTX;
unsigned long lonTX;

float GPSlat = 42.047843;
float GPSlon = 21.308923;

byte buf[4];

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

//GPS Preamble

#define GPSSerial Serial2 //Teensy Ports 9/RX2 and 10/TX2

// Connect to the GPS on the hardware port
Adafruit_GPS GPS(&GPSSerial);
     
// Set GPSECHO to 'false' to turn off echoing the GPS data to the Serial console
// Set to 'true' if you want to debug and listen to the raw GPS sentences
#define GPSECHO false

uint32_t timer = millis();
uint32_t timer1 = millis();
float Pi = 3.14159;

String currLatLong;
String timeString;
String compassString;
String stringOut;

void setup()
{
  //GPS Setup
    
  // connect at 115200 so we can read the GPS fast enough and echo without dropping chars
  // also spit it out
  Serial.begin(9600);  //Change to 9600 for Serial connect to Raspberry Pi
  Serial.println("Adafruit GPS library basic test!");
     
  // 9600 NMEA is the default baud rate for Adafruit MTK GPS's- some use 4800
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
  
  // Ask for firmware version
  GPSSerial.println(PMTK_Q_RELEASE);

  currLatLong = "null";

  XBeeSerial.begin(9600);
  xbee.setSerial(XBeeSerial);

  pinMode(buttonPin, INPUT);
  pinMode(statusLed, OUTPUT);
  pinMode(errorLed, OUTPUT);
  pinMode(buttonLed, OUTPUT);
  digitalWrite(buttonPin, HIGH);

//  attachInterrupt(buttonPin,transmitWaypoint,FALLING);
}

void loop() // run over and over again
{
  // read data from the GPS in the 'main loop'
  char c = GPS.read();
  // if you want to debug, this is a good time to do it!
  if (GPSECHO)
    if (c) Serial.print(c);
  // if a sentence is received, we can check the checksum, parse it...
  if (GPS.newNMEAreceived()) {
    // a tricky thing here is if we print the NMEA sentence, or data
    // we end up not listening and catching other sentences!
    // so be very wary if using OUTPUT_ALLDATA and trytng to print out data
    if (!GPS.parse(GPS.lastNMEA())) // this also sets the newNMEAreceived() flag to false
      return; // we can fail to parse a sentence in which case we should just wait for another
  }
  // if millis() or timer wraps around, we'll just reset it
  if (timer > millis()) timer = millis();
  if (timer1 > millis()) timer1 = millis();

//  buttonValue = analogRead(buttonPin);
//  Serial.println(buttonValue);
//  if (buttonValue < 200) {
//    digitalWrite(16, HIGH);
//  }
//  else {
//    digitalWrite(16,LOW);
//    Serial.print("off");
//  }
  
  // approximately every 0.5 seconds or so, print out the current stats
  if (millis() - timer > 500) {
    timer = millis(); // reset the timer
    Serial.print("\nTime: ");
    Serial.print(GPS.hour, DEC); Serial.print(':');
    Serial.print(GPS.minute, DEC); Serial.print(':');
    Serial.print(GPS.seconds, DEC); Serial.print('.');
    Serial.println(GPS.milliseconds);
    Serial.print("Date: ");
    Serial.print(GPS.day, DEC); Serial.print('/');
    Serial.print(GPS.month, DEC); Serial.print("/20");
    Serial.println(GPS.year, DEC);
    Serial.print("Fix: "); Serial.print((int)GPS.fix);
    Serial.print(" quality: "); Serial.println((int)GPS.fixquality);
    int dateYear = GPS.year;
    int dateMonth = GPS.month;
    int dateDay = GPS.day;
    int dateHour = GPS.hour;
    int dateMinute = GPS.minute;
    int dateSecond = GPS.seconds;
    int unixTime = 946702800 + 31536000*dateYear + 2678400*(dateMonth - 1) + 86400*(dateDay - 1) + 3600*dateHour + 60*dateMinute + dateSecond - 86400*2 - 3600*5;
    Serial.println(unixTime);
    if (GPS.fix) {
      Serial.print("Location: ");
      Serial.print(GPS.latitude, 4); Serial.print(GPS.lat);
      Serial.print(", ");
      Serial.print(GPS.longitude, 4); Serial.println(GPS.lon);
      Serial.print("Speed (knots): "); Serial.println(GPS.speed);
      Serial.print("Angle: "); Serial.println(GPS.angle);
      Serial.print("Altitude: "); Serial.println(GPS.altitude);
      Serial.print("Satellites: "); Serial.println((int)GPS.satellites);
//
//      currLatLong = String("GPS") + "Loc" + String(fabs(GPS.latitudeDegrees), 6) + GPS.lat + String(fabs(GPS.longitudeDegrees), 6) + GPS.lon;
//    }
//    else {
//      currLatLong = String("GPS") + "Loc" + "null";
//      }
////    Serial.print("Output Processed LatLong String: "); Serial.println(currLatLong);
//
//    timeString = String("Time") + String(GPS.minute,DEC) + ":" + String(GPS.seconds,DEC) + "." + String(GPS.milliseconds);
//
//  Serial.println(GPS.latitude);
//  String GPSLatituderead = String(fabs(GPS.latitudeDegrees),6);
//
//  float latitude = GPSLatituderead.toFloat();
//  Serial.println(GPSLatituderead);
//  Serial.println(latitude);
//  latTX = (long) (latitude*1000000);
//  Serial.println(latTX);
//  Serial.println(GPS.lon);
//  String londir = GPS.lon;
//  if(londir == "W"){
//    Serial.println("Lon got");
  }
//  lonTX = (long) (GPSlon*1000000);
////  Serial.println(latTX);
////  Serial.println(lonTX);
//  
//  payload[0] = latTX & 255;
//  payload[1] = (latTX >> 8) & 255;  
//  payload[2] = (latTX >> 16) & 255;
//  payload[3] = (latTX >> 24) & 255;
//  payload[4] = 0x01;
//  payload[5] = count;
//  count += 1;
//  if (count == 0xFF) {
//    count = 0x00;
//  }
//  
//  xbee.send(zbTx);
//// flash TX indicator
//  flashLed(statusLed, 1, 100);

//  // after sending a tx request, we expect a status response
//  // wait up to half second for the status response
//  if (xbee.readPacket(500)) {
//    // got a response!
//
//    // should be a znet tx status              
//    if (xbee.getResponse().getApiId() == ZB_TX_STATUS_RESPONSE) {
//      xbee.getResponse().getZBTxStatusResponse(txStatus);
//
//      // get the delivery status, the fifth byte
//      if (txStatus.getDeliveryStatus() == SUCCESS) {
//        // success.  time to celebrate
//        flashLed(statusLed, 5, 50);
//        Serial.println("Success");
//      } else {
//        // the remote XBee did not receive our packet. is it powered on?
//        flashLed(errorLed, 3, 500);
//      }
//    }
//  } else if (xbee.getResponse().isError()) {
//    //nss.print("Error reading packet.  Error code: ");  
//    //nss.println(xbee.getResponse().getErrorCode());
//  } else {
//    // local XBee did not provide a timely TX Status Response -- should not happen
//    flashLed(errorLed, 2, 50);
//  }
  }
}

//void transmitWaypoint() {
//  if (millis() - last_interrupt > 1000) {
//  digitalWrite(16, HIGH);
//  char c = GPS.read();
//  // if you want to debug, this is a good time to do it!
//  latTX = (long) (GPSlat*1000000);
//  lonTX = (long) (GPSlon*1000000);
//
//  Serial.println("Waypoint");
//  
//  payload[0] = latTX & 255;
//  payload[1] = (latTX >> 8) & 255;  
//  payload[2] = (latTX >> 16) & 255;
//  payload[3] = (latTX >> 24) & 255;
//  payload[4] = 0x01;
//  payload[5] = 0xFF;
//  
//  xbee.send(zbTx);
//// flash TX indicator
//  flashLed(statusLed, 1, 100);
//
//  // after sending a tx request, we expect a status response
//  // wait up to half second for the status response
//  if (xbee.readPacket(500)) {
//    // got a response!
//
//    // should be a znet tx status              
//    if (xbee.getResponse().getApiId() == ZB_TX_STATUS_RESPONSE) {
//      xbee.getResponse().getZBTxStatusResponse(txStatus);
//
//      // get the delivery status, the fifth byte
//      if (txStatus.getDeliveryStatus() == SUCCESS) {
//        // success.  time to celebrate
//        flashLed(statusLed, 5, 50);
//        Serial.println("Success");
//      } else {
//        // the remote XBee did not receive our packet. is it powered on?
//        flashLed(errorLed, 3, 500);
//      }
//    }
//  } else if (xbee.getResponse().isError()) {
//    //nss.print("Error reading packet.  Error code: ");  
//    //nss.println(xbee.getResponse().getErrorCode());
//  } else {
//    // local XBee did not provide a timely TX Status Response -- should not happen
//    flashLed(errorLed, 2, 50);
//  }
//  digitalWrite(16,LOW);
//  }
//  last_interrupt = millis();
//  
//}

