int redPin = 21;
int bluePin = 22;
int greenPin = 23;

void setup() {
  // put your setup code here, to run once:
  pinMode(redPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  digitalWrite(redPin, HIGH);
}

void loop() {
  flashLed(redPin,5,50);
  flashLed(greenPin,5,50);
  flashLed(bluePin,5,50);
  delay(200);
}

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
