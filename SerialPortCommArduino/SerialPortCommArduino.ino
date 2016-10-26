#include <MsTimer2.h>
#include <Streaming.h>
#include <Arduino.h>

#define DELAY 100
#define SLOW 500
#define FAST 10
#define FLEX_PIN A1
#define PIEZO_PIN A0

/* valid 'sensor' is a character '1' or '2' */
//force == 1, flex == 2
char sensor = '0';

void setup(){
  Serial.begin(57600);
  pinMode(FLEX_PIN, INPUT);
}

void readSensor(){
  if( sensor == '1' ){
    //Read from first sensor
    Serial << analogRead(PIEZO_PIN) << endl;
  }else if( sensor == '2' ){
    //Read from second sensor
    Serial << analogRead(FLEX_PIN) << endl;
  }
}

void loop(){
  char cmd = '0';
  char rateChar = '0';
  int rate = 0;

    cmd = Serial.read();
    if( cmd  == 'R' ){
      delay(DELAY);
      sensor = Serial.read();
      delay(DELAY);
      rateChar = Serial.read();
      if( (rateChar == 'S' || rateChar == 'F') &&
          (sensor == '1' || sensor == '2') ){
        if(rateChar == 'S'){
          rate = SLOW;
        }else if( rateChar == 'F' ){
          rate = FAST;
        }
        //start reading;
        MsTimer2::stop();
        MsTimer2::set( rate, readSensor );
        MsTimer2::start();
      }
      
    }else if( cmd == 'S' ){
      //stop reading
      MsTimer2::stop();
    }
    delay(DELAY);
}
