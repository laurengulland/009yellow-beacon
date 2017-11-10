unsigned long latTX;
unsigned long lonTX;

float GPSlat = 42.047843;
float GPSlon = 21.308923;

byte buf[4];

void setup() {
  Serial.begin(9600);
  latTX = (long) GPSlat*10^6;
  lonTX = (long) GPSlon*10^6;
  Serial.println(latTX);
  Serial.println(lonTX);
  buf[0] = latTX & 255;
  buf[1] = (latTX >> 8) & 255;  
  buf[2] = (latTX >> 16) & 255;
  buf[3] = (latTX >> 24) & 255;
  Serial.print(buf[0]);
  Serial.print(buf[1]);
  Serial.print(buf[2]);
  Serial.println(buf[3]);
}

void loop() {
  // put your main code here, to run repeatedly:

}
