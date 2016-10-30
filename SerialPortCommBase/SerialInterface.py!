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
 
sigHand = True
baud = 56700

#clean up tasks before program exits
def signal_handler(signal, frame):
    global sigHand
    global ser
    sigHand = False
    #wait for current searial read
    while ser.inWaiting() > 0:
      print( "waiting on" + ser.in_waiting )
    #notify arduino that program is done writing,
    ser.write(b'S')
    ser.close()

#read in data and write to list data structure
def handleSensorData(ser):
    sensorDataFileName = time.strftime("%m_%d_%y_%H_%M",time.localtime())
    sensorDataFileName = sensorDataFileName + "_" + sensor + "-" + rate + ".csv"
    sensorDataFile = open( sensorDataFileName, 'w' )
    
    while sigHand == True:
      #print("Writing data to file...")
      try:
        data = ser.read()
        sensorDataFile.write(data)
        sys.stdout.write(data)
        sys.stdout.flush()
      except TypeError:
        #Unfortunate CTRL-C timing
        print( "Connection closed" )
    sensorDataFile.close()

#init signal, waits for keyboard interrupt(Ctrl-Z)
signal.signal(signal.SIGINT, signal_handler)
#check number of arguments
if len(sys.argv) != 4:
  #print usage and exit
  usage()
  os._exit(1)
else:
  #assign user input to variables
  serial_port = sys.argv[1]
  sensor = sys.argv[2]
  rate = sys.argv[3]

#check for invalid user input 
if sensor != "FLEX" and sensor != "FORCE" or rate != 'S' and rate !='F':
  #Print the usage and exit
  usage()
  os._exit(1)

try:  
  global ser
  #create connection with port
  ser = serial.Serial(serial_port, 57600, timeout=0)
except:
  print( "Error initializing serial connection.")
  os._exit(1)

#allow time for arduino to init
sleep(2)
if sensor == "FLEX": 
  initData = 'R2' + rate
  initData = initData.encode('utf-8')
  ser.write(initData)
  handleSensorData(ser)
elif sensor == "FORCE":
  initData = 'R1' + rate
  initData = initData.encode('utf-8')
  ser.write(initData)
  handleSensorData(ser)
else:
    usage()
    os._exit(1)
