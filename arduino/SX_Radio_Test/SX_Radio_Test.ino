#include <XBee.h>

XBee xbee = XBee();
#define SXSerial Serial3
uint8_t payload[25] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};

XBeeAddress64 addr64 = XBeeAddress64(0x0013A200,0x414FF2A7);
ZBTxRequest zbTx = ZBTxRequest(addr64, payload, sizeof(payload));
ZBTxStatusResponse txStatus = ZBTxStatusResponse();

void setup() {
  // put your setup code here, to run once:
  SXSerial.begin(9600);
  xbee.setSerial(SXSerial);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
//  xbee.send(zbTx);
//  Serial.println("Packet Sent");
//  delay(2000);
  if(SXSerial.available()){
    Serial.print("Byte Recieved");
    Serial.println(SXSerial.read());
    xbee.send(zbTx);
    delay(500);
  }
}
