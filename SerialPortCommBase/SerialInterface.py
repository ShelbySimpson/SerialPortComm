import serial;
import time;

ser = serial .Serial('COM5',57600);
#ser.write(b'160,');
atenbyte = ser.read(9);
time.sleep(3);
print atenbyte;
