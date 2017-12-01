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

//Variable Definition
//int scoutSerials[1][2] = {{0x13A200,0x4164D65A}}; //Serial numbers of all scout devices connected to queen, form of [SH,SL]
int scoutSerials[1][2] = {{0x13A200,0x4151A85D}}; //PCB Scout
uint8_t accumlatedScoutData[83]; //Tablet sends single package of accumulated data
uint8_t requestSX[83]; //Tablet requests SX transmission routine

uint32_t timer = millis();
uint32_t timer1 = millis();
float Pi = 3.14159;
int count = 0; //Counter to track repetitions of searching cycles

//XBee Preamble
#define XBeeSerial Serial1 //Teensy Ports 0/RX1 and 1/TX1
#define SXSerial Serial3   //Teensy Ports 9/RX2 and 10/TX2
XBee xbee = XBee(); //Create XBee object
XBee SXxbee = XBee();
XBeeResponse response = XBeeResponse();

XBeeAddress64 hiveAddr64 = XBeeAddress64(0x0013A200,0x414FF2A7);

//Tablet Preamble
#define TabletSerial Serial //USB Serial

int statusLed = 13;
int button1 = 3;
int button2 = 4;

volatile unsigned long last_interrupt;

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

//void buttonPress(){
//  if (millis() - last_interrupt > 1000){
//    uint8_t toSend[83];                           //Initialize package to be sent 
//    for(int i=0;i<83;i++){ 
//      toSend[i] = 0x00;                           //Fill package with 0s per communication protocol
//    }
//    toSend[0] = 0x7E;
//    toSend[1] = 0x01;
//    toSend[2] = 0x01;
//    if(digitalRead(3)==LOW){
//      toSend[3] = 0x00;
//    }
//    else if(digitalRead(4)==LOW){
//      toSend[3] = 0x01;
//    }
//    cli();
//    for(int i=0;i<sizeof(toSend);i++){
//      TabletSerial.write(toSend[i]);              //Write packet to Serial
//    }
//    sei();
//  }
//  last_interrupt = millis();
//}

void setup() {
  XBeeSerial.begin(9600);
  xbee.setSerial(XBeeSerial);
  SXSerial.begin(9600);
  SXxbee.setSerial(SXSerial);
  TabletSerial.begin(9600);
  pinMode(statusLed,OUTPUT);
//  pinMode(button1,INPUT);
//  pinMode(button2,INPUT);
//  digitalWrite(button1,HIGH);
//  digitalWrite(button2,HIGH);
//  attachInterrupt(button1,buttonPress,FALLING);
//  attachInterrupt(button2,buttonPress,FALLING);
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
    for(int i=0;i<packagelength;i++){
      toSend[i+3] = package[i];                 //Read payload into sending array
    }
    toSend[1] = (packagelength+1);              //Set length byte
  }
  cli();
  for(int i=0;i<sizeof(toSend);i++){
    TabletSerial.write(toSend[i]);              //Write packet to Serial
  }
  sei();
}

void queryScout(int scoutSH, int scoutSL){
  XBeeAddress64 addr64 = XBeeAddress64(scoutSH, scoutSL);           //Set address of scout
  uint8_t request[5] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF};              //Define request bytes
  ZBTxRequest zbTx = ZBTxRequest(addr64, request, sizeof(request)); //Build request
  ZBTxStatusResponse txStatus = ZBTxStatusResponse();               //Define response
  ZBRxResponse rx = ZBRxResponse();
  uint8_t payload[25];
  
  xbee.send(zbTx);                                                  //Send request for information
  flashLed(statusLed,1,100);
  if(xbee.readPacket(2000)){    //Wait for 2 seconds to see if we get a response
    if(xbee.getResponse().getApiId() == ZB_TX_STATUS_RESPONSE){     //Check that we got an appropriate response for our request
      xbee.readPacket(2000);                                        //Wait for 2 seconds for an information packet
      if(xbee.getResponse().getApiId() == ZB_RX_RESPONSE){          //Check that we have an appropriate response
        xbee.getResponse().getZBRxResponse(rx);                     //Read response
        flashLed(statusLed,5,50);
        for(int i = 0; i < rx.getDataLength(); i++){
          payload[i] = rx.getData()[i];                             //Read payload into array
        }
        sendTeensy(payload,0x00,rx.getDataLength());                                   //Send payload to Teensy
      }
    }
  }
}

void loop() {
  //***QUERY SCOUTS FOR LOCATION DATA***
  for(int i=0;i<2;i++){
    queryScout(scoutSerials[i][0],scoutSerials[i][1]);  //Pass each serial number of scout into queryScout function
  }
  //***END QUERY***  
  
  //***SEND DATA TO HIVE OVER SX***
  if(count == 5){
    while(1==1){                                  //Maintain loop until broken when request is returned by an empty packet
      //Serial.println("Enter");
      
      sendTeensy({},0x02,0x00);                        //Request SX packet from Tablet
      uint8_t payload[80];
      while(TabletSerial.available()<83){
        //Serial.println(TabletSerial.available());
        delay(5);
      }
        byte discard = TabletSerial.read();       //Read start byte from serial and discard
        uint8_t lengthByte = TabletSerial.read(); //Read length byte
        uint8_t typeByte = TabletSerial.read();   //Read type byte
        
        if(lengthByte==0x01 && typeByte==0x03){
          for(int i=0;i<80;i++){
            byte discard = TabletSerial.read();
          }
          break;                                  //Terminates reading loop when tablet passes an empty payload array
        }
        
        for(int i = 0;i<80;i++){    //Run through all remaining bytes inside of the length
          payload[i] = TabletSerial.read();
        }
      ZBTxRequest zbTx = ZBTxRequest(hiveAddr64, payload, sizeof(payload));
      ZBTxStatusResponse txStatus = ZBTxStatusResponse();
  
      SXxbee.send(zbTx);
      delay(100);
    }
    count = 0;
  }
  count += 1;
  //Serial.println(count);
  //***END HIVE TRANSMISSION***
  delay(2000);                                 //Delay 30 seconds before querying scouts again
}

