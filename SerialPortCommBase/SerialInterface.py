import serial;
import time;
import sys;

#atenbyte = ser.read(9);
#print atenbyte;

try:
#for arg in sys.argv:
    #print arg;
    if len(sys.argv) != 4:
        print "usage: /base.py serial_port sensor sampling_rate";
        print "serial_port   = 'COMX' | '/dev/tty.usbXXXX'";
        print "sensor        = 'FLEX' | 'FORCE'";
        print "sampling rate = '5' | '50'";
    else:
        serial_port = sys.argv[1];
        sensor = sys.argv[2];
        sampling_rate = sys.argv[3];

    if sensor != "FLEX" and sensor != "FORCE":
        print sensor, "is an invalid sensor: sensor =  FLEX | FORCE";
        quit();#check to see about best way to exit system

    ser = serial .Serial(serial_port,57600);
    if sensor == "FLEX":
#        ser.write(b'0');
        print "yay its flex";
    else:
#        ser.write(b'1');
        print "yahoo its force";

#    time.sleep(3)
    while True:
        try:
            print ser.read(1);
            time.sleep(1);
        except: 
            ser.SerialTimeoutException;
            print 'Data could not be read';
        time.sleep(1);
        #print  ser.read();
    #sout = ser.read(2);
    #time.sleep(3);
    #print sout;

except:
    print "unexpected error:", sys.exc_info();
