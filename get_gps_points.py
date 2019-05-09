#!/usr/bin/env python3

import geopy
import requests
import json

class APIError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "APIError: status={}".format(self.status)

class OSRMrequest:
    def __init__(self,service,version,profile,coordinates,format="",options=[]):
        self.service = service
        self.version = version
        self.profile = profile
        self.coordinates = coordinates
        self.format = format
        self.options = options
    def _url(self,path):
        return 'https://router.project-osrm.org/' + path
    def generate_request(self):
        path = self.service+"/"+self.version+"/"+self.profile+"/"
        string = ""
        for i,coord in enumerate(self.coordinates):
            if i > 0:
                string += ";"
            string += str(coord.latitude)+","+str(coord.longitude)
        path += string
        if self.options:
            path += "?"
            string = ""
            for i,op in enumerate(self.options):
                if i > 0:
                    string += "&"
                string += op+"="+self.options[op]
            path += string
        return self._url(path)

def _Overpass_url(path):
    return 'http://overpass-api.de/api/interpreter' + path

def get_nodes(start_coord, end_coord):
    request = OSRMrequest(
        service = "route",
        version = "v1",
        profile = "driving",
        coordinates = [start_coord,end_coord],
        options = {
            "alternatives": "false",
            "annotations": "nodes"
        })
    route_resp = requests.get(request.generate_request())
    print(route_resp.text)
    if route_resp.status_code != 200:
        raise ApiError('Cannot fetch all tasks: {}'.format(resp.status_code))
    # If route could not be generated, return None
    if route_resp.json().get('message') is not None:
        return None
    nodes = route_resp.json()["routes"][0]["legs"][0]["annotation"]["nodes"]
    return nodes

def build_overpass_post(nodes):
    post = ""
    post += "[out:json];\n"
    post += "(\n"
    for node in nodes:
        post += "   node({});\n".format(node)
    post += ");\n"
    post += "(._;>;);\n"
    post += "out;"
    return post

def get_coordinates(nodes):
    ordered_route = dict.fromkeys(nodes,{})
    post = build_overpass_post(nodes)
    coord_resp = requests.post(_Overpass_url(""), data=post)
    #print(nodes)
    print('Resp:')
    print(coord_resp.text)
    if coord_resp.status_code != 200:
        raise ApiError('Cannot fetch all tasks: {}'.format(resp.status_code))
    for coord in coord_resp.json()["elements"]:
        ordered_route[coord['id']] = geopy.point.Point(latitude = coord["lat"],longitude = coord["lon"])
        #coords.append(geopy.point.Point(latitude = coord["lat"],longitude = coord["lon"]))
    coords = []
    for node in nodes:
        coords.append(ordered_route[node])
    return coords
