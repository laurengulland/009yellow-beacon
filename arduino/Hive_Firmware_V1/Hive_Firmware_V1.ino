//Libraries
#include <XBee.h> //XBee library

//XBee Preamble - Intialize XBee information
#define SXSerial Serial3                                          //Teensy Ports 9/RX2 and 10/TX2
XBee SXxbee = XBee();
XBeeResponse response = XBeeResponse();
ZBRxResponse rx = ZBRxResponse();

//Tablet Preamble
#define TabletSerial Serial                                       //USB Serial

int statusLed = 13;

void setup() {
  // put your setup code here, to run once:
  SXSerial.begin(9600);
  SXxbee.setSerial(SXSerial);
  TabletSerial.begin(9600);
  pinMode(statusLed,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  SXxbee.readPacket();
  if(xbee.getResponse().getApiId() == ZB_RX_RESPONSE){          //Check that we have an appropriate response
    xbee.getResponse().getZBRxResponse(rx);                     //Read response
    flashLed(statusLed,5,50);
    for(int i = 0; i < rx.getDataLength(); i++){
      TabletSerial.write(rx.getData()[i]);                             //Read payload into array
    }
  }
  
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
