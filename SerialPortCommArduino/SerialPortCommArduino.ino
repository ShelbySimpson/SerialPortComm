#include <MsTimer2.h>
#include <Streaming.h>

#define DELAY 100
#define SLOW 500
#define FAST 10

/* valid 'sensor' is a character '1' or '2' */
char sensor = '0';

void setup(){
  Serial.begin(57600);
}

void readSensor(){
  if( sensor == '1' ){
    //Read from first sensor
    //Serial.println(analogRead(0), DEC);
    Serial.println("Reading from sensor '1'");
  }else if( sensor == '2' ){
    //Read from second sensor
    Serial.println("Reading from sensor '2'");
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
