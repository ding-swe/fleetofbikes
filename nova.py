import requests
from requests import Request, Session
import logging
import datetime
from Exceptions.HologramError import HologramError
from Hologram.HologramCloud import HologramCloud
from Hologram.CustomCloud import CustomCloud

USE_NOVA = 0
DEFAULT_TIMEOUT = 5
post_endpoint = 'http://Fleetofbikes-env.vrqy7xh9wt.us-east-1.elasticbeanstalk.com/testPost'
post_endpoint_ip = '3.94.25.131'
post_port = 80
post_header = ''
get_endpoint = ''
get_port = 80

fake_data = {'name': 'dick2',
            'loc': {
                'lat': '12.345678',
                'lon': '-12.345678'},
            'timestamp': '57',
            'speed': '0'}

logging.basicConfig(filename='nova_py.log', level=logging.DEBUG)

customCloud = CustomCloud(None,
                          send_host=post_endpoint_ip,
                          send_port=post_port,
                          network='cellular')
fake_data['timestamp'] = str(datetime.datetime.now())

recv = ''
print('Sending message to cloud: ' + str(fake_data))
if USE_NOVA == 0:
    print('Using WiFi to send POST')
    # req = Request('POST', post_endpoint, json=fake_data)
    # print(str(req.prepare()))
    recv = requests.post(post_endpoint, json=fake_data)
else:
    print('Using Nova to send POST')
    # recv = customCloud.sendMessage(str(fake_data))
    hologram = HologramCloud(dict(),network='cellular')
    res = hologram.network.connect()
    print(str(res))
    recv = requests.post(post_endpoint, json=fake_data)

print('Response from Cloud: ' + str(recv) + '.')
