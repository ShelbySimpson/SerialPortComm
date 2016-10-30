#! /bin/python2
import serial
import time
import sys
from time import sleep
import os
import signal
import string

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
    #empty out whats left in serial and save to data list
    while ser.inWaiting(): 
        sData = ser.readline().strip();
        data.append(sData);
        sys.stdout.flush()

    #create a timestamp name for file
    sensorDataName = time.strftime("%m_%d_%y_%H_%M",time.localtime());
    #add rate sensor details to filename
    sensorDataName = sensorDataName + "_" + sensor + "-" + rate + ".csv";
    #write data list to file,close file
    sensorDataFile = open(sensorDataName,'w');
    #write data to file
    print("Writing data to file...");
    for item in data:
        item = str(item,'utf-8');#convert from bytes to String
        sensorDataFile.write(item + '\n');#add newline
        print(item);#allow user to see what has being written to file.
    sensorDataFile.close();
    print("Done writing data");
    
    sigHand = False
    #notify arduino that program is done writing, exit
    ser.write(b'S')
    ser.close()
    os._exit(0)

#read in data and write to list data structure
def handleSensorData(ser):
    #while user hasn't interrupted data collection process 
    #save data to list
    while sigHand:
        while ser.inWaiting(): 
            #read in line and strip \r\n, for csv formatting purposes
            #newline is added when written to file.
            sData = ser.readline().strip();
            data.append(sData);
            print(sData);#let user see bytes, will eventually be saved to csv
            sleep(.5);#allow time to handle data before reading again
            sys.stdout.flush();#flush

#init signal, waits for keyboard interrupt(Ctrl-Z)
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
      initData = 'R2' + rate;#add rate to output data
      initData = initData.encode('utf-8');#encode data,bytes for serial port
      ser.write(initData);#write
      handleSensorData(ser);#handle incoming data
    elif sensor == "FORCE":
      initData = 'R1' + rate;#add rate to ouptut data
      initData = initData.encode('utf-8');#encode data,bytes for serial port
      ser.write(initData);#write
      handleSensorData(ser)#handle incoming data
    else:
        usage();#invalid input, notify user
        os._exit(1);#exit program

except:
    print( "unexpected error:", sys.exc_info());
