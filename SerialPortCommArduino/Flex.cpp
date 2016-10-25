#include "Flex.h"

Flex::Flex(short pin){
  _pin = pin;
}

short Flex::getData(){
  return analogRead(_pin);//read in data
}

