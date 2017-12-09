/*
 * Queen Serial: SH -> 0x13A200, SL -> 0x41515876
 * Scout 1 Serial: SH -> 0x13A200, SL -> 0x4164D65A
 * Scout 2 Serial: SH -> 0x13A200, SL -> 0x41515879
 * Hive Serial: SH -> 0013A200, SL -> 414FF265
 * Scout PCB Serial: SH -> 0013A200, SL -> 4151A85D
 * Queen PCB Serial: SH -> 0013A200, SL -> 4151A855
 */

//Libraries
#include <XBee.h> //XBee library
#include <Adafruit_GPS.h> //Adafruit GPS library

uint32_t QueenSH = 0x0013A200;
uint32_t QueenSL = 0x4151A856;

//Byte Definition - Define several commonly used bytes to improve readablity
#define EMPTY 0x00
#define START_BYTE 0x7E
#define REQUEST_TABLET 0x02
#define SCOUT_DATA 0x00
#define QUEEN_DATA 0x01
#define TABLET_DATA 0x03
#define PACKET_LENGTH 83

//Variable definition
uint8_t payload[32] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
volatile uint8_t poiPayload[15] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
volatile unsigned long last_interrupt;
volatile unsigned long latTX;
volatile unsigned long lonTX;
volatile uint8_t longdir;
volatile uint8_t latdir;
volatile int unixTime;

float GPSlat = 42.358340;
float GPSlon = 71.094600;
String GPSLatitudeRead;
String GPSLongitudeRead;
float latitude;
float longitude;

byte stale = 0x00;

int statusLed = 13;
int buttonPin = 11;


//XBee Initialization
#define XBeeSerial Serial1 //Teensy Ports 0/RX1 and 1/TX1
XBee xbee = XBee(); //Create XBee object
XBeeResponse response = XBeeResponse();
ZBRxResponse rx = ZBRxResponse();
XBeeAddress64 addr64 = XBeeAddress64(QueenSH, QueenSL); //PCB
ZBTxRequest zbTx = ZBTxRequest(addr64, payload, sizeof(payload));
ZBTxStatusResponse txStatus = ZBTxStatusResponse();

//GPS Initialization
#define GPSSerial Serial2 //Teensy Ports 9/RX2 and 10/TX2
// Connect to the GPS on the hardware port
Adafruit_GPS GPS(&GPSSerial);
     
// Set GPSECHO to 'false' to turn off echoing the GPS data to the Serial console
// Set to 'true' if you want to debug and listen to the raw GPS sentences
#define GPSECHO false

uint32_t timer;
uint32_t timerStale = millis();

void setup() {
  Serial.begin(9600);
  GPS.begin(9600);
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ); // 1 Hz update rate  

  delay(1000);
  GPSSerial.println(PMTK_Q_RELEASE);

  XBeeSerial.begin(9600);
  xbee.setSerial(XBeeSerial);
  pinMode(statusLed, OUTPUT);
  pinMode(buttonPin, INPUT);
  digitalWrite(buttonPin, HIGH);
  attachInterrupt(buttonPin,markWaypoint,FALLING);
}

void loop() {
  timer = millis();
  while(millis()-timer < 500){
  char c = GPS.read();
  if (GPSECHO)
    if (c) Serial.print(c);
  if (GPS.newNMEAreceived()) {
    if (!GPS.parse(GPS.lastNMEA())) // this also sets the newNMEAreceived() flag to false
      return; // we can fail to parse a sentence in which case we should just wait for another
  }
  }
  int dateYear = GPS.year;
  int dateMonth = GPS.month;
  int dateDay = GPS.day;
  int dateHour = GPS.hour;
  int dateMinute = GPS.minute;
  int dateSecond = GPS.seconds;
  unixTime = unixTime = 946702800 + 31536000*dateYear + 2678400*(dateMonth - 1) + 86400*(dateDay - 1) + 3600*dateHour + 60*dateMinute + dateSecond - 86400*2 - 3600*5;
  
  if (timerStale > millis()) timerStale = millis();

  timer = millis();
  if(GPS.fix){
    String GPSLatituderead = String(fabs(GPS.latitudeDegrees),6);
    String GPSLongituderead = String(fabs(GPS.longitudeDegrees),6);
    float longitude = GPSLongituderead.toFloat();
    float latitude = GPSLatituderead.toFloat();
    latTX = (long) (latitude*1000000);
    lonTX = (long) (longitude*1000000);
    String longdirs = GPS.lon;
    stale = 0x00;
    Serial.println("FIX");
    if(longdirs=="E"){
      longdir = 0x01;
    }
    else if(longdirs=="W"){
      longdir = 0x02;
    }
    String latdirs = GPS.lat;
    if(latdirs=="N"){
      latdir = 0x01;
    }
    else if(latdirs=="S"){
      latdir = 0x02;
    }     
  }
  else { //Set to dummy data in middle of Kresege
    if(millis()-timerStale > 120000){
      timerStale = millis();
      stale = 0x01;
    }
    latTX = (long) 42358340;
    lonTX = (long) 71094600;
    latdir = 0x01;
    longdir = 0x02;
  }
  Serial.println(lonTX);
  Serial.println(latTX);
  Serial.println(unixTime);
  xbee.readPacket();
  if(xbee.getResponse().isAvailable()){
    if(xbee.getResponse().getApiId() == ZB_RX_RESPONSE){
      flashLed(statusLed, 1,100);
      xbee.getResponse().getZBRxResponse(rx);
      Serial.println("Request Recieved");

      if(rx.getDataLength() == 5){
          payload[0] = latTX & 255;
          payload[1] = (latTX >> 8) & 255;  
          payload[2] = (latTX >> 16) & 255;
          payload[3] = (latTX >> 24) & 255;
          payload[4] = latdir;
          payload[5] = lonTX & 255;
          payload[6] = (lonTX >> 8) & 255;  
          payload[7] = (lonTX >> 16) & 255;
          payload[8] = (lonTX >> 24) & 255;
          payload[9] = longdir;
          payload[10] = 0x02;               //Scout ID
          payload[11] = unixTime & 255;
          payload[12] = (unixTime >> 8) & 255;  
          payload[13] = (unixTime >> 16) & 255;
          payload[14] = (unixTime >> 24) & 255;
          payload[15] = stale;
          payload[16] = 0x00;               //is POI included 0 no 1 yes
          

          

          if(poiPayload[10]!=0x00){
            payload[16] = 0x01;
            for(int i=0;i<15;i++){
              payload[i+17] = poiPayload[i];
              poiPayload[i] = 0;            //Clean up array for next use
            }
          }

          xbee.send(zbTx);
          for(int i=0;i<32;i++){
            payload[i] = 0x00;
          }
          flashLed(statusLed,5,50);
      }
    }
  }

}

void markWaypoint(){
  if (millis() - last_interrupt > 1000){
    poiPayload[0] = latTX & 255;
    poiPayload[1] = (latTX >> 8) & 255;  
    poiPayload[2] = (latTX >> 16) & 255;
    poiPayload[3] = (latTX >> 24) & 255;
    poiPayload[4] = latdir;
    poiPayload[5] = lonTX & 255;
    poiPayload[6] = (lonTX >> 8) & 255;  
    poiPayload[7] = (lonTX >> 16) & 255;
    poiPayload[8] = (lonTX >> 24) & 255;
    poiPayload[9] = longdir;
    poiPayload[10] = 0x01;                    //Scout ID
    poiPayload[11] = unixTime & 255;
    poiPayload[12] = (unixTime >> 8) & 255;  
    poiPayload[13] = (unixTime >> 16) & 255;
    poiPayload[14] = (unixTime >> 24) & 255;
    }
  last_interrupt = millis();
}

//Debug function to flash Teensy built in LED
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
