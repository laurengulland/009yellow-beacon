uint8_t payload[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int size_of_payload=80;

void setup() {
  Serial.begin(9600);
//Hexidecimal Latitude Digit Representation
  payload[0] = 0x0B; //_ _ _ _ _ X X
  payload[1] = 0x59; //_ _ _ X X _ _
  payload[2] = 0x86; //_ X X _ _ _ _
  payload[3] = 0x02;  //X _ _ _ _ _ _
  payload[4] = 0x01;  //1 -> North 2-> South
  //hex digits go into hex number, then convert
//Longitude
  payload[5] = 0x7C; //_ _ _ _ _ X X
  payload[6] = 0xC4; //_ _ _ X X _ _
  payload[7] = 0x3C; //_ X X _ _ _ _
  payload[8] = 0x04;  //X _ _ _ _ _ _
  payload[9] = 0x02;  //1 -> East 2-> West
//Information
  payload[10] = 0x01; //Scout identifier number 0-9 (May go up in number of scouts)
  payload[11] = 0x01; //Point-of-interest marker 0 -> Regular Update, 1-4 -> POI Levels
//We may add sending a time-stamp here if needed but it would come after this in the payload array. So we'll call these first 12 spots finalized
}

void loop() {
  //Serial.println("Scout GPS"); //Some sort of marker to identify what kind of input we are passing. We can talk more about what we want later.
  Serial.write(0x7e);
  Serial.write(0x0d);
  Serial.write(0x00);
  for(int i = 0; i < size_of_payload; i++)
  {
    Serial.write(payload[i]);
  }
  delay(5000);
}
