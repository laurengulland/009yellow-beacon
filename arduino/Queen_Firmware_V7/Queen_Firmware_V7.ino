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

//Byte Definition - Define several commonly used bytes to improve readablity
#define EMPTY 0x00
#define START_BYTE 0x7E
#define REQUEST_TABLET 0x02
#define SCOUT_DATA 0x00
#define QUEEN_DATA 0x01
#define TABLET_DATA 0x03
#define PACKET_LENGTH 83

//Variable Definition - Define variables to be used in the rest of the program
//int scoutSerials[1][2] = {{0x13A200,0x4164D65A}};               //Serial numbers of all scout devices connected to queen, form of [SH,SL] (Breadboard)
int scoutSerials[1][2] = {{0x13A200,0x4151A85D}};                 //Serial numbers of all scout devices connected to queen, form of [SH,SL] (PCB Scout)
uint8_t accumlatedScoutData[83];                                  //Tablet sends single package of accumulated data
uint8_t requestSX[83];                                            //Tablet requests SX transmission routine

int countdebug = 0;
int count = 0; //Counter to track repetitions of searching cycles

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
int resetPin = 4;

uint32_t timer = millis();
uint32_t timerStale = millis();

uint8_t queenPayload[17] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};

//GPS Initialization
#define GPSSerial Serial2 //Teensy Ports 9/RX2 and 10/TX2
// Connect to the GPS on the hardware port
Adafruit_GPS GPS(&GPSSerial);
     
// Set GPSECHO to 'false' to turn off echoing the GPS data to the Serial console
// Set to 'true' if you want to debug and listen to the raw GPS sentences
#define GPSECHO false

//XBee Preamble - Intialize XBee information
#define XBeeSerial Serial1                                        //Teensy Ports 0/RX1 and 1/TX1
#define SXSerial Serial3                                          //Teensy Ports 9/RX2 and 10/TX2
XBee xbee = XBee();                                               //Create XBee object
XBee SXxbee = XBee();
XBeeResponse response = XBeeResponse();

XBeeAddress64 hiveAddr64 = XBeeAddress64(0x0013A200,0x414FF2A7);

//Tablet Preamble
#define TabletSerial Serial                                       //USB Serial

void setup() {
  GPS.begin(9600);
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ); // 1 Hz update rate  

  delay(1000);
  GPSSerial.println(PMTK_Q_RELEASE);
  //Open Serial Ports with Baud rate of 9600 and attach to relevant XBee objects
  XBeeSerial.begin(9600);
  xbee.setSerial(XBeeSerial);
  SXSerial.begin(9600);
  SXxbee.setSerial(SXSerial);
  TabletSerial.begin(9600);
  pinMode(statusLed,OUTPUT);
  pinMode(resetPin,OUTPUT);
  digitalWrite(resetPin,HIGH);
}

void loop() {
  //***QUERY SCOUTS FOR LOCATION DATA***
  for(int i=0;i<1;i++){
    queryScout(scoutSerials[i][0],scoutSerials[i][1]);  //Pass each serial number of scout into queryScout function
    countdebug += 1;
    if(countdebug == 25){
      digitalWrite(resetPin, LOW);
      delay(300);
      digitalWrite(resetPin, HIGH);
      delay(500);
      countdebug = 0;
    }
  }
  //***END QUERY***  

  //***QUEEN GPS QUERY
  timer = millis();
  while(millis()-timer < 500){
    char c = GPS.read();
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
  if(GPS.fix){
    String GPSLatituderead = String(fabs(GPS.latitudeDegrees),6);
    String GPSLongituderead = String(fabs(GPS.longitudeDegrees),6);
    float longitude = GPSLongituderead.toFloat();
    float latitude = GPSLatituderead.toFloat();
    latTX = (long) (latitude*1000000);
    lonTX = (long) (longitude*1000000);
    String longdirs = GPS.lon;
    stale = 0x00;
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
  }
  queenPayload[0] = latTX & 255;
  queenPayload[1] = (latTX >> 8) & 255;  
  queenPayload[2] = (latTX >> 16) & 255;
  queenPayload[3] = (latTX >> 24) & 255;
  queenPayload[4] = latdir;
  queenPayload[5] = lonTX & 255;
  queenPayload[6] = (lonTX >> 8) & 255;  
  queenPayload[7] = (lonTX >> 16) & 255;
  queenPayload[8] = (lonTX >> 24) & 255;
  queenPayload[9] = longdir;
  queenPayload[10] = 0x01;               //Scout ID
  queenPayload[11] = unixTime & 255;
  queenPayload[12] = (unixTime >> 8) & 255;  
  queenPayload[13] = (unixTime >> 16) & 255;
  queenPayload[14] = (unixTime >> 24) & 255;
  queenPayload[15] = stale;
  queenPayload[16] = 0x00;

  sendTeensy(queenPayload,QUEEN_DATA,0x17);
  //***END QUEEN GPS
  
  //***SEND DATA TO HIVE OVER SX***
  if(count == 3){
    while(true){                                        //Maintain loop until broken when request is returned by an empty packet
      
      sendTeensy({},REQUEST_TABLET,EMPTY);              //Request SX packet from Tablet
      uint8_t payload[83];
      while(TabletSerial.available()<83){
        delay(5);                                       //Wait until 83 bytes have accumlated in the serial buffer to ensure complete message read
      }

      for(int i = 0;i<83;i++){                          //Run through all bytes and insert into array
          payload[i] = TabletSerial.read();
      }

      byte lengthByte = payload[1];
      byte typeByte = payload[2];
      
      if(lengthByte==0x01 && typeByte==0x03){           //*** NOTE THIS SEEMS TO BREAK THINGS MUST TEST AS TO WHY***
        break;                                          //Terminates reading loop when tablet passes an empty payload array
      }
        
      ZBTxRequest zbTx = ZBTxRequest(hiveAddr64, payload, sizeof(payload));
      ZBTxStatusResponse txStatus = ZBTxStatusResponse();
  
      SXxbee.send(zbTx);
      delay(100);
    }
    count = 0;
  }
  //***END HIVE TRANSMISSION***
  count += 1;
  delay(2000);                                          //Delay before querying scouts again
}

//Debug function to flash onboard Teensy LED
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

void sendTeensy(uint8_t package[], uint8_t packet, uint8_t packagelength){
  uint8_t toSend[PACKET_LENGTH];                                //Initialize package to be sent 
  for(int i=0;i<PACKET_LENGTH;i++){ 
    toSend[i] = EMPTY;                                          //Fill package with 0s per communication protocol
  }
  toSend[0] = START_BYTE;                                       //Set start byte
  toSend[2] = packet;                                           //Set packet type byte
  if(packet == REQUEST_TABLET){
    toSend[1] = 0x01;                                           //Set length byte to 1 for tablet request packet type
  }
  if(toSend[2] == SCOUT_DATA or toSend[2] == QUEEN_DATA){
    for(int i=0;i<packagelength;i++){
      toSend[i+3] = package[i];                                 //Populate sending array with payload
    }
    toSend[1] = (packagelength+1);                              //Set length byte to the length of the data plus one for the type byte
  }
  for(int i=0;i<sizeof(toSend);i++){
    TabletSerial.write(toSend[i]);                              //Write packet to Serial
  }
}

void queryScout(int scoutSH, int scoutSL){
  XBeeAddress64 addr64 = XBeeAddress64(scoutSH, scoutSL);           //Set address of scout
  uint8_t request[5] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF};              //Assign random set of request bytes; scout just verifies data length
  ZBTxRequest zbTx = ZBTxRequest(addr64, request, sizeof(request)); //Build request
  ZBTxStatusResponse txStatus = ZBTxStatusResponse();               //Define response
  ZBRxResponse rx = ZBRxResponse();
  uint8_t payload[32];
  
  xbee.send(zbTx);                                                  //Send request for information
  flashLed(statusLed,1,100);
  if(xbee.readPacket(3000)){                                        //Wait for 2 seconds to see if we get a response
    if(xbee.getResponse().getApiId() == ZB_TX_STATUS_RESPONSE){     //Check that we got an appropriate response for our request
      xbee.readPacket(2000);                                        //Wait for 2 more seconds for an information packet
      if(xbee.getResponse().getApiId() == ZB_RX_RESPONSE){          //Check that we have an appropriate response
        xbee.getResponse().getZBRxResponse(rx);                     //Read response
        flashLed(statusLed,5,50);
        for(int i = 0; i < rx.getDataLength(); i++){
          payload[i] = rx.getData()[i];                             //Read payload into array
        }
        sendTeensy(payload,SCOUT_DATA,rx.getDataLength());          //Send payload to Teensy
      }
    }
  }
}
