import requests
import json
from math import sqrt, pi
import os
import sys

class GeoFence:
    def __init__(self, name, lat, lng):
        self.name = name
        self.lat = lat
        self.lng = lng
        #4000m ~ about 25 miles
        self.radius = 40000

def read_geos():
    #check if coords.txt exists in dir above
    f_coords = os.path.join(os.path.dirname(__file__), '../coords.txt')

    if os.path.isfile(f_coords):
        with open(f_coords, 'r') as f:
            data = f.read().rstrip()
            
            for i in data.split('\n'):
                name, lat, lng = i.split(',')
                geo = GeoFence(name,lat,lng)
                query_yelp(geo)
        f.close()

    else:
        pass
        # if coords doesnt exist run read.py


def query_yelp(geo):
    access_token = '44skPsEBmBM8L3IsIA37vEx9XweIk3KLd7v76bTFob2GYGgoya1GJora7QBtujJ6x6wcY127I-nKfWsUP-mEfWwwIxWL4qvAWL-4biXzNhg_zV7KZQjDqcDAoWklXHYx'

    headers = {'Authorization': 'bearer %s' % access_token}
    payload = {'latitude': float(geo.lat), 'longitude': float(geo.lng),'radius': round(geo.radius), 'attributes': 'hot_and_new', 'sort_by': 'distance'}
    req = requests.get('https://api.yelp.com/v3/businesses/search', params=payload, headers=headers)

    geo_file = os.path.join(os.path.dirname(__file__), '../result/', geo.name + '.txt')
    with open(geo_file, 'w') as out:
        write_to_file(req, out)
    out.close()
    # print(req.text)

def write_to_file(req, out):
    geo_dic = json.loads(req.text)
    try:
        for business in geo_dic['businesses']:
            out.write(business['name'] + '\n')
            for j in business['location']['display_address']:
                out.write(j + ', ')
            out.write('\n')
            out.write(business['phone'] + '\n')
            out.write(business['url'] + '\n')
            out.write('\n')
    except(KeyError):
        print(json.dumps(geo_dic))
