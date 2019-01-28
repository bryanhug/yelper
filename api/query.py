import requests
import json
from math import sqrt, pi
import os
import sys

def get_restaurants(req,g):
    '''Gets restaurants that are in the geo-fence.'''
    geo_file = os.path.join(os.path.dirname(__file__), '../all_result/',g.name + '.txt')
    geo_dic = json.loads(req.text)

    try:
        with open(geo_file, 'w') as out:
            for business in geo_dic['businesses']:
                # if g.in_geo(business['coordinates']['latitude'], business['coordinates']['longitude']):
                g.write_to_file(business,out)
        out.close()
    except:
        print(req.text)

def query_yelp(geo):
    '''Queries yelp with centroid lat and lng'''
    access_token = '44skPsEBmBM8L3IsIA37vEx9XweIk3KLd7v76bTFob2GYGgoya1GJora7QBtujJ6x6wcY127I-nKfWsUP-mEfWwwIxWL4qvAWL-4biXzNhg_zV7KZQjDqcDAoWklXHYx'

    headers = {'Authorization': 'bearer %s' % access_token}
    payload = {'latitude': float(geo.lat), 'longitude': float(geo.lng),'radius': round(geo.radius), 'attributes': 'hot_and_new', 'sort_by': 'distance'}
    req = requests.get('https://api.yelp.com/v3/businesses/search', params=payload, headers=headers)
    get_restaurants(req,geo)

