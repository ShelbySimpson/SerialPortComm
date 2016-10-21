import serial;
import time;

ser = serial .Serial('COM5',57600);
ser.write(b'160,');
time.sleep(1);
