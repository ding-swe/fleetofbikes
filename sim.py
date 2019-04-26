import requests
import datetime
import numpy
import time
import math
import threading

loc_period = 2 #10 seconds between sending GPS coords
info_period = 60 #60 seconds between sending health status

num_bikes = 1

MAX_SPEED = 20
MIN_LAT = 38.979522
MAX_LAT = 39.000471
MIN_LON = -76.954621
MAX_LON = -76.926382

LAT_CON = 69 # Number of miles per degree latitude
LON_CON = 54.6 # Number of miles per degree longitude

status_endpoint = 'http://Fleetofbikes-env.vrqy7xh9wt.us-east-1.elasticbeanstalk.com/bike/status/update/'
loc_endpoint = 'http://Fleetofbikes-env.vrqy7xh9wt.us-east-1.elasticbeanstalk.com/bike/location/'
info_endpoint = 'http://Fleetofbikes-env.vrqy7xh9wt.us-east-1.elasticbeanstalk.com/bike/info/update/'

status_data = {'name': 'Nova_One',
                'flag': 1}

loc_list = [{'name': 'Nova_One',
                'lat': '0.0',
                'lon': '0.0',
                'timestamp': 'Unk'} for bike in range (0, num_bikes)]

info_list = [{'name': 'Nova_One',
                'speed': 0,
                'timestamp': 'Unk',
                'break_status': 1,
                'chain_status': 1,
                'battery_level': 100,
                'tire_pressure': 1} for bike in range (0, num_bikes)]

print('Start')

for bike in range (0,num_bikes):
    loc_list[bike]['name'] = "Nova_Sim_%d" % (bike)
    info_list[bike]['name'] = "Nova_Sim_%d" % (bike)
    status_data['name'] = "Nova_Sim_%d" % (bike)
    loc_list[bike]['lat'] = '{:2.6f}'.format(numpy.random.random_sample() * (MAX_LAT - MIN_LAT) + MIN_LAT)
    loc_list[bike]['lon'] = '{:2.6f}'.format(numpy.random.random_sample() * (MAX_LON - MIN_LON) + MIN_LON)
    curr_time = time.gmtime()
    loc_list[bike]['timestamp'] = '{}/{}/{} {:02}:{:02}:{:02}'.format(
        curr_time.tm_mon,   # Grab parts of the time from the
        curr_time.tm_mday,  # struct_time object that holds
        curr_time.tm_year,  # the fix time.  Note you might
        curr_time.tm_hour,  # not get all data like year, day,
        curr_time.tm_min,   # month!
        curr_time.tm_sec)
    info_list[bike]['timestamp'] = '{}/{}/{} {:02}:{:02}:{:02}'.format(
        curr_time.tm_mon,   # Grab parts of the time from the
        curr_time.tm_mday,  # struct_time object that holds
        curr_time.tm_year,  # the fix time.  Note you might
        curr_time.tm_hour,  # not get all data like year, day,
        curr_time.tm_min,   # month!
        curr_time.tm_sec)

    print('Sending message to cloud: ' + str(status_data))
    # Send the POST request to the server; should use Nova to send data
    recv = requests.post(status_endpoint, json=status_data)
    print('Response from Cloud: ' + str(recv) + '.')



def location_thread():
    # Schedule thread to run again after loc_period seconds
    #threading.Timer(loc_period, location_thread).start()
    while 1:
        for bike in range (0,num_bikes):
            speed = numpy.random.random_sample() * MAX_SPEED
            travel_angle = numpy.random.random_sample() * 2*math.pi
            loc_list[bike]['lat'] = '{:2.6f}'.format(math.cos(travel_angle) * loc_period * speed/3600.0 /LAT_CON + float(loc_list[bike]['lat']))
            loc_list[bike]['lon'] = '{:2.6f}'.format(math.sin(travel_angle) * loc_period * speed/3600.0 /LON_CON + float(loc_list[bike]['lon']))
            curr_time = time.gmtime()
            loc_list[bike]['timestamp'] = '{}/{}/{} {:02}:{:02}:{:02}'.format(
                curr_time.tm_mon,   # Grab parts of the time from the
                curr_time.tm_mday,  # struct_time object that holds
                curr_time.tm_year,  # the fix time.  Note you might
                curr_time.tm_hour,  # not get all data like year, day,
                curr_time.tm_min,   # month!
                curr_time.tm_sec)
            print('Sending message to cloud: ' + str(loc_list[bike]))
            # Send the POST request to the server; should use Nova to send data
            recv = requests.post(loc_endpoint, json=loc_list[bike])
            print('Response from Cloud: ' + str(recv) + '.')
        time.sleep(loc_period)


# def info_thread():
#     threading.Timer(info_period, info_thread).start()
#     curr_time = time.gmtime()
#     info_data['timestamp'] = '{}/{}/{} {:02}:{:02}:{:02}\n'.format(
#         curr_time.tm_mon,   # Grab parts of the time from the
#         curr_time.tm_mday,  # struct_time object that holds
#         curr_time.tm_year,  # the fix time.  Note you might
#         curr_time.tm_hour,  # not get all data like year, day,
#         curr_time.tm_min,   # month!
#         curr_time.tm_sec)
#     print('Sending message to cloud: ' + str(info_data))
#     # Send the POST request to the server; should use Nova to send data
#     recv = requests.post(info_endpoint, json=info_data)
#     print('Response from Cloud: ' + str(recv) + '.')


# Start main thread that listens to incoming
# loc_th = threading.Thread(target = location_thread)
# loc_th.start()
# info_th = threading.Thread(target = info_thread)
# info_th.start()
location_thread()
