#! /bin/python2

import serial
from time import sleep
import sys
import os
import signal

def usage():
  print( "usage: /base.py serial_port sensor rate")
  print( "    serial_port   = 'COMX' | '/dev/tty.usbXXXX'")
  print( "    sensor        = 'FLEX' | 'FORCE'")
  print( "    sampling rate = 'S' | 'F'")
 
sigHand = True;

def signal_handler(signal, frame):
  sigHand = False
  ser.write(b'S')
  ser.close()
  os._exit(0)

def serPrint(ser):
  while sigHand:
    #python's print() sucks
    sys.stdout.write( ser.read() )
    sys.stdout.flush()

signal.signal(signal.SIGINT, signal_handler)
try:
    if len(sys.argv) != 4:
        usage()
        os._exit(1)
    else:
        serial_port = sys.argv[1];
        sensor = sys.argv[2];
        rate = sys.argv[3];

    if sensor != "FLEX" and sensor != "FORCE" or rate != 'S' and rate !='F':
        usage()
        os._exit(1)

    ser = serial.Serial(serial_port, 57600, timeout=0);
    sleep(2)
    if sensor == "FLEX":
      ser.write(b'R2S')
      serPrint(ser)
    elif sensor == "FORCE":
      ser.write('R1S');
      serPrint(ser)
    else:
        usage()
        os._exit(1)

except:
    print( "unexpected error:"), sys.exc_info();
