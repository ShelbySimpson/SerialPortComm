#ifndef Flex_h
#define Flex_h
#include "Arduino.h"

using namespace std;

class Flex{
  private:
    short _pin;//sensor pin
  public:
    Flex(short pin);//set sensor _pin
    short getData();//return current sensor data

};
#endif
