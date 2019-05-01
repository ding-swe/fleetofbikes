import requests
import logging
import warnings
import time
import sys
import threading
import subprocess

from Exceptions.HologramError import HologramError
from Hologram.HologramCloud import HologramCloud


loc_period = 5 #60 seconds between sending GPS coords
info_period = 300 #300 seconds between sending health status

cell_loc_attempts = 3 #Max of 3 attempts to use CellLocate to get position

gps = subprocess.Popen(['python3','nova_gps.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

status_endpoint = 'http://Fleetofbikes-env.vrqy7xh9wt.us-east-1.elasticbeanstalk.com/bike/status/update/'
loc_endpoint = 'http://Fleetofbikes-env.vrqy7xh9wt.us-east-1.elasticbeanstalk.com/bike/location/'
info_endpoint = 'http://Fleetofbikes-env.vrqy7xh9wt.us-east-1.elasticbeanstalk.com/bike/info/update/'

status_data = {'name': 'Nova_One',
                'flag': 1}

loc_data = {'name': 'Nova_One',
                'lat': '0.0',
                'lon': '0.0',
                'timestamp': 'Unk'}

info_data = {'name': 'Nova_One',
                'speed': 0,
                'timestamp': 'Unk',
                'break_status': 1,
                'chain_status': 1,
                'battery_level': 100,
                'tire_pressure': 1}

logging.basicConfig(filename='nova_py.log', level=logging.DEBUG)

#Establish a PPP connection on the Pi if it is not already established
print('Establishing PPP connection')
hologram = HologramCloud(dict(),network='cellular')
if hologram._networkManager.networkConnected():
    print('Network already connected')
else:
    print("Network not yet connected, connecting")
    res = hologram.network.connect()

def location_thread():
    # Schedule thread to run again after loc_period seconds
    threading.Timer(loc_period, location_thread).start()
    # Try to get GPS location first as it is considered more accurate
    gps.stdin.write("loc\n")
    gps.stdin.flush()
    recv = gps.stdout.readline().strip()
    if recv == 'no_fix':
        print('No GPS fix')
    else:
        loc_data['lat'] = recv
        loc_data['lon'] = gps.stdout.readline().strip()
        info_data['speed'] = gps.stdout.readline().strip()
        curr_time = time.gmtime()
        loc_data['timestamp'] = '{}/{}/{} {:02}:{:02}:{:02}'.format(
            curr_time.tm_mon,   # Grab parts of the time from the
            curr_time.tm_mday,  # struct_time object that holds
            curr_time.tm_year,  # the fix time.  Note you might
            curr_time.tm_hour,  # not get all data like year, day,
            curr_time.tm_min,   # month!
            curr_time.tm_sec)
    print('Sending message to cloud: ' + str(loc_data))
    # Send the POST request to the server; should use Nova to send data
    recv = requests.post(loc_endpoint, json=loc_data)
    print('Response from Cloud: ' + str(recv) + '.')


def info_thread():
    threading.Timer(info_period, info_thread).start()
    curr_time = time.gmtime()
    info_data['timestamp'] = '{}/{}/{} {:02}:{:02}:{:02}\n'.format(
        curr_time.tm_mon,   # Grab parts of the time from the
        curr_time.tm_mday,  # struct_time object that holds
        curr_time.tm_year,  # the fix time.  Note you might
        curr_time.tm_hour,  # not get all data like year, day,
        curr_time.tm_min,   # month!
        curr_time.tm_sec)
    print('Sending message to cloud: ' + str(info_data))
    # Send the POST request to the server; should use Nova to send data
    recv = requests.post(info_endpoint, json=info_data)
    print('Response from Cloud: ' + str(recv) + '.')


print('Sending message to cloud: ' + str(status_data))
# Send the POST request to the server; should use Nova to send data
recv = requests.post(status_endpoint, json=status_data)
print('Response from Cloud: ' + str(recv) + '.')

# Start main thread that listens to incoming
loc_th = threading.Thread(target = location_thread)
loc_th.start()
info_th = threading.Thread(target = info_thread)
info_th.start()

dummy = 0
while 1:
    try:
        dummy += 1
        time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupt received, exiting...")
        break

recv = gps.communicate('kill\n')[0]
print('nova_gps: {}'.format(recv))
sys.exit()
