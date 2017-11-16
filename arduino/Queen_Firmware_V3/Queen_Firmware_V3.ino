/*
 * Queen Serial: SH -> 0x13A200, SL -> 0x41515876
 * Scout 1 Serial: SH -> 0x13A200, SL -> 0x4164D65A
 */

//Libraries
#include <XBee.h> //XBee library
#include <Adafruit_GPS.h> //Adafruit GPS library

//Variable Definition
int scoutSerials[1][2] = {{0x13A200,0x4164D65A}}; //Serial numbers of all scout devices connected to queen, form of [SH,SL]
uint8_t accumlatedScoutData[83]; //Tablet sends single package of accumulated data
uint8_t requestSX[83]; //Tablet requests SX transmission routine

uint32_t timer = millis();
uint32_t timer1 = millis();
float Pi = 3.14159;
int count = 0; //Counter to track repetitions of searching cycles

//XBee Preamble
#define XBeeSerial Serial1 //Teensy Ports 0/RX1 and 1/TX1
#define SXSerial Serial2   //Teensy Ports 9/RX2 and 10/TX2
XBee xbee = XBee(); //Create XBee object
XBee SXxbee = XBee();
XBeeResponse response = XBeeResponse();

XBeeAddress64 hiveAddr64 = XBeeAddress64(0x13A200,0x41515876);

////GPS Preamble
//#define GPSSerial Serial2 //Teensy Ports 9/RX2 and 10/TX2
//Adafruit_GPS GPS(&GPSSerial); //Conenct to the GPS on the hardware port
//// Set GPSECHO to 'false' to turn off echoing the GPS data to the Serial console
//// Set to 'true' if you want to debug and listen to the raw GPS sentences
//#define GPSECHO false

//Tablet Preamble
#define TabletSerial Serial //USB Serial

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
  XBeeSerial.begin(9600);
  xbee.setSerial(XBeeSerial);
  SXSerial.begin(9600);
  SXxbee.setSerial(SXSerial);
  TabletSerial.begin(9600);
  pinMode(statusLed,OUTPUT);
}

void loop() {
  //***QUERY SCOUTS FOR LOCATION DATA***
  for(int i=0;i<1;i++){
    TabletSerial.println("New Query");
    queryScout(scoutSerials[i][0],scoutSerials[i][1]);  //Pass each serial number of scout into queryScout function
  }
  //***END QUERY***  
  
//  //***SEND DATA TO HIVE OVER SX***
//  if(count == 5){
//    while(1==1){                                  //Maintain loop until broken when request is returned by an empty packet
//      sendTeensy({},0x02);                        //Request SX packet from Tablet
//      //Read SX packet
//      uint8_t *payload;
//      while(TabletSerial.available()<83){
//        delay(5);
//      }
//      if(TabletSerial.read() == 0x7E){            //Start from start byte ***May not work***
//        byte discard = TabletSerial.read();       //Read start byte from serial and discard
//        uint8_t lengthByte = TabletSerial.read(); //Read length byte
//        uint8_t typeByte = TabletSerial.read();   //Read type byte
//        payload = new uint8_t[lengthByte];
//        
//        if(lengthByte==0x01 && typeByte==0x03){
//          break;                                  //Terminates reading loop when tablet passes an empty payload array
//        }
//        
//        if(typeByte == 0x03){
//          for(int i = 0;i<(lengthByte-1);i++){    //Run through all remaining bytes inside of the length
//            payload[i] = TabletSerial.read();
//          }
//        }
//      }
//      ZBTxRequest zbTx = ZBTxRequest(hiveAddr64, payload, sizeof(payload));
//      ZBTxStatusResponse txStatus = ZBTxStatusResponse();
//  
//      SXxbee.send(zbTx);
//  
//        if(SXxbee.readPacket(500)){
//          if(SXxbee.getResponse().getApiId() == ZB_TX_STATUS_RESPONSE){
//            SXxbee.getResponse().getZBTxStatusResponse(txStatus);
//          }
//        }
//      
//    }
//  count = -1;
//  }
//  count += 1;
//  //***END HIVE TRANSMISSION***
  delay(5000);                                 //Delay 30 seconds before querying scouts again
  TabletSerial.println("New Loop");

}

void sendTeensy(uint8_t package[], uint8_t packet, uint8_t packagelength){
  uint8_t toSend[83];                           //Initialize package to be sent 
  for(int i=0;i<83;i++){ 
    toSend[i] = 0x00;                           //Fill package with 0s per communication protocol
  }
  toSend[0] = 0x7E;                             //Set start byte
  toSend[2] = packet;                           //Set packet type byte
  if(packet == 0x02){
    toSend[1] = 0x01;                          //Set length byte to 1 for SX request type
  }
  if(toSend[2] == 0x00 or toSend[2] == 0x01){
    TabletSerial.print("Package Size: ");
    TabletSerial.println(sizeof(package));
    for(int i=0;i<packagelength;i++){
      toSend[i+3] = package[i];                 //Read payload into sending array
      TabletSerial.println(package[i]);
    }
    toSend[1] = (packagelength+1);              //Set length byte
  }
  for(int i=0;i<sizeof(toSend);i++){
//    TabletSerial.print("toSend: ");
//    TabletSerial.println(toSend[i]);
    TabletSerial.write(toSend[i]);              //Write packet to Serial
  }
}

void queryScout(int scoutSH, int scoutSL){
  XBeeAddress64 addr64 = XBeeAddress64(scoutSH, scoutSL);           //Set address of scout
  uint8_t request[5] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF};              //Define request bytes
  ZBTxRequest zbTx = ZBTxRequest(addr64, request, sizeof(request)); //Build request
  ZBTxStatusResponse txStatus = ZBTxStatusResponse();               //Define response
  ZBRxResponse rx = ZBRxResponse();
  uint8_t payload[25];
  
  xbee.send(zbTx);                                                  //Send request for information
//  TabletSerial.println("New Request");
  flashLed(statusLed,1,100);
  if(xbee.readPacket(2000)){    //Wait for 2 seconds to see if we get a response
    if(xbee.getResponse().getApiId() == ZB_TX_STATUS_RESPONSE){     //Check that we got an appropriate response for our request
      xbee.readPacket(2000);                                        //Wait for 2 seconds for an information packet
//      TabletSerial.println("Reply Recieved");
      if(xbee.getResponse().getApiId() == ZB_RX_RESPONSE){          //Check that we have an appropriate response
//        TabletSerial.println("Right Reply Recieved");
        xbee.getResponse().getZBRxResponse(rx);                     //Read response
        flashLed(statusLed,5,50);
//        TabletSerial.println(rx.getDataLength());
//        TabletSerial.println(".");
        for(int i = 0; i < rx.getDataLength(); i++){
          payload[i] = rx.getData()[i];                             //Read payload into array
//          TabletSerial.print("Recieved: ");
//          TabletSerial.println(payload[i]);
        }
        sendTeensy(payload,0x01,rx.getDataLength());                                   //Send payload to Teensy
      }
    }
  }
}

