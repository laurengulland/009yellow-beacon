const int ledPin = 13;

void setup()
{
  //Begin serial monitor port
  Serial.begin(9600);
  //Begin HW serial
  Serial1.begin(9600);
  pinMode(ledPin, OUTPUT);

}

void loop()
{
  // Take data received from the serial monitor and pass it to the HW UART
  if(Serial.available())
  {
    Serial1.print(Serial.read(), BYTE);
    Serial1.print("Memes");
    Serial1.print(2, BYTE);
  }

 // Take data received from the HW UART and pass it to the serial monitor
  if(Serial1.available())
  {
    Serial.print(Serial1.read(), BYTE);
  }

 digitalWrite(ledPin, HIGH);   // set the LED on               

 //Wait to reduce serial load
  delay(5);
}
