#include <Servo.h>

Servo myservo;
int angle = 0;
int newAngle = 0;
const int MaxChars = 4;
char strValue[MaxChars+1];
int index = 0;

void serialEvent()
{
   while(Serial.available()) 
   {
      char ch = Serial.read();
      Serial.write(ch);
      if(index < MaxChars && isDigit(ch)){
          strValue[index++] = ch;              
          }else{
            strValue[index] = 0;                    
            newAngle = atoi(strValue);                    
            if(newAngle > 0 && newAngle <180){
            if(newAngle < angle)                                
              for(; angle > newAngle; angle -= 1) {
                   myservo.write(angle);
               }  
            else 
               for(; angle < newAngle; angle += 1){
                   myservo.write(angle);
                } 
         }
         index = 0;
         angle = newAngle;
      }  
   }
}


void setup()
{
  Serial.begin(57600);
  myservo.attach(10);
  angle = 90;  
}

void loop()
{
    
}
