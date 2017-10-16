// An example demonstrating the multiceiver capability of the NRF24L01+
// in a star network with one PRX hub and up to six PTX nodes

//This sketch is a modification from a video on the ForceTronics YouTube Channel,

//which code was leveraged from http://maniacbug.github.io/RF24/starping_8pde-example.html

//This sketch is free to the public to use and modify at your own risk


#include <SPI.h> //Call SPI library so you can communicate with the nRF24L01+

#include <nRF24L01.h> //nRF2401 libarary found at https://github.com/tmrh20/RF24/

#include <RF24.h> //nRF2401 libarary found at https://github.com/tmrh20/RF24/

const int pinCE = 7; //This pin is used to set the nRF24 to standby (0) or active mode (1)

const int pinCSN = 8; //This pin is used to tell the nRF24 whether the SPI communication is a command or message to send out


RF24 radio(pinCE, pinCSN); // Create your nRF24 object or wireless SPI connection

#define WHICH_NODE 2     // must be a number from 1 - 6 identifying the PTX node

const uint64_t wAddress[] = {0x7878787878LL, 0xB3B4B5B6F1LL, 0xB3B4B5B6CDLL, 0xB3B4B5B6A3LL, 0xB3B4B5B60FLL, 0xB3B4B5B605LL};

const uint64_t PTXpipe = wAddress[ WHICH_NODE - 1 ];   // Pulls the address from the above array for this node's pipe

byte counter = 1; //used to count the packets sent

bool done = false; //used to know when to stop sending packets


// GPS Header

#include <Adafruit_GPS.h>

// what's the name of the hardware serial port?
SoftwareSerial Serial1(2,3);

#define GPSSerial Serial1

// Connect to the GPS on the hardware port
Adafruit_GPS GPS(&GPSSerial);
     
// Set GPSECHO to 'false' to turn off echoing the GPS data to the Serial console
// Set to 'true' if you want to debug and listen to the raw GPS sentences
#define GPSECHO false

uint32_t timer = millis();

String currLatLong;


void setup()  

{
  //while (!Serial);  // uncomment to have the sketch wait until Serial is ready
  
  // connect at 115200 so we can read the GPS fast enough and echo without dropping chars
  // also spit it out
  Serial.begin(115200);
  Serial.println("Adafruit GPS library basic test!");
     
  // 9600 NMEA is the default baud rate for Adafruit MTK GPS's- some use 4800
  GPS.begin(9600);
  // uncomment this line to turn on RMC (recommended minimum) and GGA (fix data) including altitude
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  // uncomment this line to turn on only the "minimum recommended" data
  //GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY);
  // For parsing data, we don't suggest using anything but either RMC only or RMC+GGA since
  // the parser doesn't care about other sentences at this time
  // Set the update rate
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ); // 1 Hz update rate
  // For the parsing code to work nicely and have time to sort thru the data, and
  // print it out we don't suggest using anything higher than 1 Hz
     
  // Request updates on antenna status, comment out to keep quiet
  GPS.sendCommand(PGCMD_ANTENNA);

  delay(1000);
  
  // Ask for firmware version
  GPSSerial.println(PMTK_Q_RELEASE);

  currLatLong = "null";

  //Serial.begin(115200);   //start serial to communicate process

  randomSeed(analogRead(0)); //create unique seed value for random number generation

  radio.begin();            //Start the nRF24 module

  radio.setPALevel(RF24_PA_MAX);  // "short range setting" - increase if you want more range AND have a good power supply
  radio.setChannel(120);          // the higher channels tend to be more "open"

  radio.openReadingPipe(0,PTXpipe);  //open reading or receive pipe

  radio.stopListening(); //go into transmit mode

}

void loop()  

{

  // read data from the GPS in the 'main loop'
  char c = GPS.read();
  // if you want to debug, this is a good time to do it!
  if (GPSECHO)
    if (c) Serial.print(c);
  // if a sentence is received, we can check the checksum, parse it...
  if (GPS.newNMEAreceived()) {
    // a tricky thing here is if we print the NMEA sentence, or data
    // we end up not listening and catching other sentences!
    // so be very wary if using OUTPUT_ALLDATA and trytng to print out data
    Serial.println(GPS.lastNMEA()); // this also sets the newNMEAreceived() flag to false
    if (!GPS.parse(GPS.lastNMEA())) // this also sets the newNMEAreceived() flag to false
      return; // we can fail to parse a sentence in which case we should just wait for another
  }
  // if millis() or timer wraps around, we'll just reset it
  if (timer > millis()) timer = millis();

   if(millis() - timer > 1000) { // approximately every 1 second or so, print out the current stats

     if(GPS.fix){
      currLatLong = String(fabs(GPS.latitudeDegrees), 6) + GPS.lat + ", " + String(fabs(GPS.longitudeDegrees), 6) + GPS.lon;
      }
     else{
      currLatLong = "null";
      }
      

     //byte randNumber = (byte)random(11); //generate random guess between 0 and 10
     char charBuf[currLatLong.length()+1];
     currLatLong.toCharArray(charBuf, currLatLong.length()+1);

     radio.openWritingPipe(PTXpipe);        //open writing or transmit pipe

     if (!radio.write( &charBuf, sizeof(charBuf) )){  //if the write fails let the user know over serial monitor

         Serial.println("Location delivery failed");      

     }

     else { //if the write was successful 

          Serial.print("Success sending location: ");

          Serial.println(charBuf);

       

        radio.startListening(); //switch to receive mode to see if the guess was right

        unsigned long startTimer = millis(); //start timer, we will wait 200ms 

        bool timeout = false; 

        while ( !radio.available() && !timeout ) { //run while no receive data and not timed out

          if (millis() - startTimer > 200 ) timeout = true; //timed out

        }

    

        if (timeout) Serial.println("Data not received"); //no data to receive guess must have been wrong

        else  { //we received something so guess must have been right

          char charRecieve[currLatLong.length()+1]; //variable to store received value

          radio.read( &charRecieve,currLatLong.length()+1); //read value

          if(strcmp(charRecieve,charBuf)) { //make sure it equals value we just sent, if so we are done

            Serial.println("Data transmitted correctly");

            //done = true; //signal to loop that we are done guessing

          }

          else Serial.println("Data transmitted incorrectly"); //this should never be true, but just in case

        }

        radio.stopListening(); //go back to transmit mode

     }

   }

    //delay(1000);

}
