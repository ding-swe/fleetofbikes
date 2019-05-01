import adafruit_gps
import RPi.GPIO as GPIO
import serial
import sys
import time

gps_fix_attempts = 9 #Max of 10 attempts to acquire GPS location via GNSS before trying CellLocate. Note each attempt takes approximately 1 second
lat = 0.0
lon = 0.0

# Initialize the GPS
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3000)
# Create a GPS module instance.
gps = adafruit_gps.GPS(uart, debug=False)
# Turn on the basic GGA and RMC info
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
# Set update rate to once a second (1hz) which is what you typically want.
gps.send_command(b'PMTK220,1000')

while 1:
    # Get a command from nova.py
    command = sys.stdin.readline().strip()
    if command == 'loc':
        attempts = 0
        # First try to acquire
        gps.update()
        while not gps.has_fix and attempts < gps_fix_attempts:
            # Try again if we don't have a fix yet.
            attempts += 1
            gps.update()

        if not gps.has_fix:
            sys.stdout.write('no_fix\n')
        else:
            sys.stdout.write('{:3.6f}\n'.format(gps.latitude))
            sys.stdout.write('{:3.6f}\n'.format(gps.longitude))
            sys.stdout.write('{}\n'.format(gps.speed_knots))
        sys.stdout.flush()
    elif command == 'kill':
        sys.stdout.write('exiting\n')
        sys.stdout.flush()
        break
    else:
        sys.stdout.write('Unknown command\n')
        sys.stdout.flush()
        sys.exit()
