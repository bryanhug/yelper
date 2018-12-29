#!/bin/env python3
from fastkml import kml
import re
import os

def parse_description(geos, description):
    """Splits the kml description into name, area, lat, lng"""
    # Splits the Placemark description into 25 parts
    split = re.split(r'<br>', description)
    #split[3]=area, split[4]=lat, split[5]=lng
    name = split[0].split(':')[2].rstrip().lstrip().replace('/','')

    area = split[3].split()[1]
    lat = split[4].split()[1]
    lng = split[5].split()[1]
    geos.write(name + ',' + area + ',' + lat + ',' + lng + '\n')

with open('C5Dense.kml', 'rb') as f:
    """Opens kml file and outputs geos into coords.txt"""
    doc = f.read()
    k = kml.KML()
    k.from_string(doc)

    #new version
    features = list(k.features())
    placemarks = list(features[0].features())

    geos = open(os.path.join(os.path.dirname(__file__), '../coords.txt'), 'w')
    for p in placemarks:
        parse_description(geos, p.description)

    geos.close()
f.close()
