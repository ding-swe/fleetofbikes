import requests
import datetime
import numpy
import time
import math
import threading
import pprint
import get_gps_points
import geopy
import pdb

loc_period = 2 #10 seconds between sending GPS coords
info_period = 60 #60 seconds between sending health status

real_time = True

num_bikes = 10

SPEED_MEAN = 10
SPEED_SD = 3

MIN_LAT = 38.979522
MAX_LAT = 39.000471
MIN_LON = -76.954621
MAX_LON = -76.926382

LAT_CON = 69 # Number of miles per degree latitude
LON_CON = 54.6 # Number of miles per degree longitude

status_endpoint = 'http://Fleetofbikes-env.vrqy7xh9wt.us-east-1.elasticbeanstalk.com/bike/status/update/many'
loc_endpoint = 'http://Fleetofbikes-env.vrqy7xh9wt.us-east-1.elasticbeanstalk.com/bike/location/many'
info_endpoint = 'http://Fleetofbikes-env.vrqy7xh9wt.us-east-1.elasticbeanstalk.com/bike/info/update/'

status_list = [{'name': 'Nova_One',
                'flag': 1} for bike in range (0, num_bikes)]

loc_list = [{'name': 'Nova_One',
                'flag': 0,
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

bikes = [{'dest': {'lat': 0.0, 'lon': 0.0},
                'route': [],
                'direction': 0.0} for bike in range (0, num_bikes)]

total_weights = 0
campus_list = [{'name' : 'A. James Clark Hall',
                                    'lat': 38.991620,
                                    'lon': -76.937572,
                                    'weight': 5},       # popularity weight of location, should be between 1-10
                {'name' : 'Computer Science Instructional Center',
                                    'lat': 38.990021,
                                    'lon': -76.936419,
                                    'weight': 5},
                {'name' : 'Adele H. Stamp Student Union',
                                    'lat': 38.987755,
                                    'lon': 76.944206,
                                    'weight': 5},
                {'name' : 'McKeldin Library',
                                    'lat': 38.985849,
                                    'lon': 76.944630,
                                    'weight': 5},
                {'name' : 'South Campus Dining Hall',
                                    'lat': 38.983275,
                                    'lon': -76.943353,
                                    'weight': 5},
                {'name' : 'Reckford Armory',
                                    'lat': 38.986281,
                                    'lon': -76.939132,
                                    'weight': 5},
                {'name' : 'Edward St. John Learning & Teaching Center',
                                    'lat': 38.987127,
                                    'lon': -76.942316,
                                    'weight': 5},
                {'name' : 'The Clarice Smith Performing Arts Center',
                                    'lat': 38.990877,
                                    'lon': -76.950096,
                                    'weight': 5},
                {'name' : '251 North Dining Hall',
                                    'lat': 38.992422,
                                    'lon': -76.949589,
                                    'weight': 5},
                {'name' : 'Eppley Recreation Center',
                                    'lat': 38.993390,
                                    'lon': -76.945069,
                                    'weight': 5},
                {'name' : 'Xfinity Center',
                                    'lat': 38.994791,
                                    'lon': -76.940302,
                                    'weight': 5},
                {'name' : 'Washington Quad',
                                    'lat': 38.982276,
                                    'lon': -76.941349,
                                    'weight': 5},
                {'name' : 'Robert H. Smith School of Business',
                                    'lat': 38.983844,
                                    'lon': -76.947052,
                                    'weight': 5},
                {'name' : 'Glenn L. Martin Hall',
                                    'lat': 38.988601,
                                    'lon': -76.938546,
                                    'weight': 5},
                {'name' : 'Physics Building',
                                    'lat': 38.988979,
                                    'lon': -76.940390,
                                    'weight': 5},
                {'name' : 'Atlantic Building',
                                    'lat': 38.990679,
                                    'lon': -76.942300,
                                    'weight': 5},
                {'name' : 'A.V. Williams Building',
                                    'lat': 38.990782,
                                    'lon': -76.936584,
                                    'weight': 5},
                {'name' : 'J.M. Patterson Building',
                                    'lat': 38.990238,
                                    'lon': -76.94016,
                                    'weight': 5},
                {'name' : 'UMD Memorial Chapel',
                                    'lat': 38.984191,
                                    'lon': -76.940357,
                                    'weight': 5},
                {'name' : 'Bioscience Research Building',
                                    'lat': 38.988896,
                                    'lon': -76.943415,
                                    'weight': 5}
                ]

# print('Start')
# route_test = requests.get('http://router.project-osrm.org/route/v1/driving/13.388860,52.517037;13.397634,52.529407;13.428555,52.523219?overview=false')
# pprint.pprint(route_test.json())
# for row in route_test.json():
#         data = json.loads(row)
#         print json)

def change_bike_status(index):
    status_selector = numpy.random.random_sample()

def choose_location(index):
    weight_idx = numpy.random.random_sample() * total_weights
    i = 0
    j = 0
    while i <= weight_idx and j < len(campus_list):
        i = i + campus_list[j]['weight']
        j = j + 1
    print('Chose location ' + campus_list[j-1]['name'])
    return [campus_list[j-1]['lat'], campus_list[j-1]['lon']]

def choose_destination(index):
    # Set destination in bike's data strucutre
    route_generated = False
    while not route_generated:
        dest = choose_location(index)
        bikes[index]['dest']['lat'] = dest[0]
        bikes[index]['dest']['lon'] = dest[1]
        # Convert to points for route calculation
        start = geopy.point.Point(float(loc_list[index]['lon']), float(loc_list[index]['lat']), 0)
        finish = geopy.point.Point(bikes[index]['dest']['lon'], bikes[index]['dest']['lat'], 0)
        #Calculate route
        nodes = get_gps_points.get_nodes(start,finish)
        if nodes is not None:
            route_generated = True
    coords = get_gps_points.get_coordinates(nodes)
    print('Printing Coords')
    for coord in coords:
        print('{},{}'.format(coord.latitude, coord.longitude))
    bikes[index]['route'] = coords
    # Set the direction of the bike to the next endpoint
    y_dist = bikes[index]['route'][0].latitude - float(loc_list[index]['lat'])
    x_dist = bikes[index]['route'][0].longitude - float(loc_list[index]['lon'])
    bikes[index]['direction'] = math.atan(y_dist/x_dist)

def bike_at_dest(index):
    if (bikes[index]['dest']['lat'] - float(loc_list[index]['lat'])) == 0.0 and \
        (bikes[index]['dest']['lon'] - float(loc_list[index]['lon'])) == 0.0:
        return True
    else:
        return False

def move_bike(index, time_delta):
    # First check that bike is not at destination
    if not bike_at_dest(index):
        # Decide speed of the bike; use normal distribution with mean 10 mph and SD 3. Do abs so no negative
        info_list[index]['speed'] = abs(numpy.random.normal(loc=SPEED_MEAN, scale=SPEED_SD))
        # Calculate distance to travel in time interval based on speed, in miles
        distance = info_list[index]['speed'] * time_delta / 3600.00
        print('Speed: {}'.format(info_list[index]['speed']))
        # We may pass multiple route nodes, so do while loop until distance is 0 or we reach dest
        while distance > 0.0 and not bike_at_dest(index):
            # Update the direction angle
            y_dist = 0.0
            x_dist = 0.0
            # If still nodes in the route, use those
            if len(bikes[index]['route']) > 0:
                y_dist = bikes[index]['route'][0].latitude - float(loc_list[index]['lat'])
                x_dist = bikes[index]['route'][0].longitude - float(loc_list[index]['lon'])
            # Else use the destination and current location
            else:
                y_dist = bikes[index]['dest']['lat'] - float(loc_list[index]['lat'])
                x_dist = bikes[index]['dest']['lon'] - float(loc_list[index]['lon'])
            # Determine direction, accounting for range of inverse tangent
            bikes[index]['direction'] = math.atan2(y_dist, x_dist)

            print('Direction {}'.format(bikes[index]['direction']))
            # Determine if distance to next node or distance traveled by bike is shorter
            # Since angle is already determined, only check latitude, round to 6 decimal points
            if (round(y_dist * LAT_CON, 6) <= round(distance * math.sin(bikes[index]['direction']), 6)):
                # Set the current location to the current node
                loc_list[index]['lat'] = '{:.6f}'.format(float(loc_list[index]['lat']) + y_dist)
                loc_list[index]['lon'] = '{:.6f}'.format(float(loc_list[index]['lon']) + x_dist)
                # Remove the node from the route
                if len(bikes[index]['route']) > 0:
                    bikes[index]['route'].pop(0)
                distance = round(distance - math.hypot(y_dist*LAT_CON,x_dist*LON_CON), 6)
            else:
                # Set the current location to the current node
                loc_list[index]['lat'] = '{:.6f}'.format(float(loc_list[index]['lat']) + (distance * math.sin(bikes[index]['direction']) / LAT_CON))
                loc_list[index]['lon'] = '{:.6f}'.format(float(loc_list[index]['lon']) + (distance * math.cos(bikes[index]['direction']) / LON_CON))
                # We have traveled complete distance
                distance = 0.0

# Get the combined weights, which will be used to select destination with appropiate weight
for dest in campus_list:
    total_weights = total_weights + dest['weight']

for bike in range (0,num_bikes):
    loc_list[bike]['name'] = "Nova_Sim_%d" % (bike)
    info_list[bike]['name'] = "Nova_Sim_%d" % (bike)
    status_list[bike]['name'] = "Nova_Sim_%d" % (bike)
    status_list[bike]['flag'] = 1
    loc_list[bike]['flag'] = 1 # {:1.0f}'.format(numpy.random.random_sample() * 6)
    # Use the existing function to generate a start location
    print('Choosing start...')
    start = choose_location(bike)
    loc_list[bike]['lat'] = str(start[0])
    loc_list[bike]['lon'] = str(start[1])
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
    # Choose destination and generate route
    print('Choosing destination...')
    choose_destination(bike)

print('Sending message to cloud: ' + str(status_list))
# Send the POST request to the server; should use Nova to send data
recv = requests.post(status_endpoint, json=status_list)
print('Response from Cloud: ' + str(recv) + '.')



def location_thread():
    # Schedule thread to run again after loc_period seconds
    #threading.Timer(loc_period, location_thread).start()
    while 1:
        for bike in range (0,num_bikes):
            # speed = numpy.random.random_sample() * MAX_SPEED
            # travel_angle = numpy.random.random_sample() * 2*math.pi
            # loc_list[bike]['lat'] = '{:2.6f}'.format(math.cos(travel_angle) * loc_period * speed/3600.0 /LAT_CON + float(loc_list[bike]['lat']))
            # loc_list[bike]['lon'] = '{:2.6f}'.format(math.sin(travel_angle) * loc_period * speed/3600.0 /LON_CON + float(loc_list[bike]['lon']))
            if loc_list[bike] == 2:
                move_bike(bike, loc_period)
            if real_time:
                curr_time = time.gmtime()
            else:
                pass
            loc_list[bike]['timestamp'] = '{}/{}/{} {:02}:{:02}:{:02}'.format(
                curr_time.tm_mon,   # Grab parts of the time from the
                curr_time.tm_mday,  # struct_time object that holds
                curr_time.tm_year,  # the fix time.  Note you might
                curr_time.tm_hour,  # not get all data like year, day,
                curr_time.tm_min,   # month!
                curr_time.tm_sec)
        print('Sending message to cloud: ' + str(loc_list))
        # Send the POST request to the server; should use Nova to send data
        recv = requests.post(loc_endpoint, json=loc_list)
        print('Response from Cloud: ' + str(recv) + '.')
        if real_time:
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
