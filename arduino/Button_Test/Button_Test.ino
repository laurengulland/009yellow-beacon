int buttonPin1 = 3;
int buttonPin2 = 4;
int joyX = 14;
int joyY = 15;

void setup() {
  pinMode(buttonPin1,INPUT);
  pinMode(buttonPin2,INPUT);
  pinMode(joyX,INPUT);
  pinMode(joyY,INPUT);
  digitalWrite(buttonPin1,HIGH);
  digitalWrite(buttonPin2,HIGH);
//  analogWrite(joyX,HIGH);
//  analogWrite(joyY,HIGH);
  Serial.begin(9600);
}

void loop() {
  Serial.print("Button 1: ");
  Serial.println(digitalRead(buttonPin1));
  Serial.print("Button 2: ");
  Serial.println(digitalRead(buttonPin2));
  Serial.print("X: ");
  Serial.print(analogRead(joyX));
  Serial.print(" Y: ");
  Serial.println(analogRead(joyY));
  delay(500);
}
