import requests
import logging
import datetime
import subprocess
from Exceptions.HologramError import HologramError
from Hologram.HologramCloud import HologramCloud
import adafruit_gps
import board
import RPi.GPIO as GPIO
import serial

post_endpoint = 'http://Fleetofbikes-env.vrqy7xh9wt.us-east-1.elasticbeanstalk.com/testPost'

test_data = {'name': 'test_bike',
            'loc': {
                'lat': '12.345678',
                'lon': '-12.345678'},
            'timestamp': '57',
            'speed': '0'}

logging.basicConfig(filename='nova_py.log', level=logging.DEBUG)

# Establish a PPP connection on the Pi if it is not already established
print('Establishing PPP connection')
subprocess.run('sudo', 'python', 'nova_estab_ppp.py')
# Start UART communication with GPS module
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3000)
# Create a GPS module instance.
gps = adafruit_gps.GPS(uart, debug=False)
# Turn on the basic GGA and RMC info
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
# Set update rate to once a second (1hz) which is what you typically want.
gps.send_command(b'PMTK220,1000')
# Acquire single GPS position
gps.update()
while not gps.has_fix:
    # Try again if we don't have a fix yet.
    print('Waiting for fix...')
    gps.update()
    break

# Set the acquired GPS variables
test_data['timestamp'] = str(datetime.datetime.now())
test_data['loc']['lat'] = str(gps.latitude)
test_data['loc']['lon'] = str(gps.longitude)
test_data['speed'] = str(gps.speed_knots)
print('Sending message to cloud: ' + str(test_data))

# Send the POST request to the server; should use Nova to send data
recv = requests.post(post_endpoint, json=test_data)
print('Response from Cloud: ' + str(recv) + '.')
