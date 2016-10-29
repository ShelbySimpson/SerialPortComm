#! /bin/python2
import serial
import time
import sys
from time import sleep
import os
import signal
import csv
import string
from msvcrt import getch

#explain command line inputs
def usage():
  print( "usage: /base.py serial_port sensor rate")
  print( "    serial_port   = 'COMX' | '/dev/tty.usbXXXX'")
  print( "    sensor        = 'FLEX' | 'FORCE'")
  print( "    sampling rate = 'S' | 'F'")
 
sigHand = True;#signal Handler

data = [];#list to store sensor data
baud = 56700;

#clean up tasks before program exits
def signal_handler(signal, frame):
    #while ser.inWaiting():
        #strData = str(ser.read(5),'utf-8');#convert bytes
        #strData = strData.rstrip();#strip newlines
        #data.append(strData);#add to list
        #data.append("\r");#newline
        #sys.stdout.flush()
        #print(strData);
    #create a timestamp name for file
    sensorDataName = time.strftime("%m_%d_%y_%H_%M",time.localtime());
    sensorDataName = sensorDataName + "_" + sensor + "-" + rate + ".csv";
    #write data list to file,close file
    sensorDataFile = open(sensorDataName,'w');
    for item in data:
        sensorDataFile.write(item);
    sensorDataFile.close();
    
    sigHand = False
    #notify arduino that program is done writing, exit
    ser.write(b'S')
    ser.close()
    os._exit(0)

#write data to list
def serPrint(ser):
    #while user still wants data,save
    while sigHand:
        #makeList();
        #print(ser.read(5));
        strData = str(ser.read(4),'utf-8');
        sleep(.5);
        strData = strData.rstrip();#strip newlines
        data.append(strData);#add to list
        data.append("\r");#newline
        sys.stdout.flush()
        print(strData);

#init signal
signal.signal(signal.SIGINT, signal_handler)
try:
    #check num arguments
    if len(sys.argv) != 4:
        usage()#not enough, inform user
        os._exit(1)#exit program
    else:
        serial_port = sys.argv[1];#save serial port
        sensor = sys.argv[2];#save sensor
        rate = sys.argv[3];#save rate

    #check if valid sensor argument was given
    if sensor != "FLEX" and sensor != "FORCE" or rate != 'S' and rate !='F':
        usage();#inform user
        os._exit(1)#exit program
    
    #create connection with port
    ser = serial.Serial(serial_port, 57600, timeout=0);
    sleep(2);#allow time to create serial object
    if sensor == "FLEX": 
      initData = 'R2' + rate;
      initData = initData.encode('utf-8');
      ser.write(initData);
      serPrint(ser)
    elif sensor == "FORCE":
      initData = 'R1' + rate;
      initData = initData.encode('utf-8');
      ser.write(initData);
      serPrint(ser)
    else:
        usage()
        os._exit(1)

except:
    print( "unexpected error:", sys.exc_info());
