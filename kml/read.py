#!/bin/env python3
from fastkml import kml
import re
import os, sys
import traceback

class Point2D:
    def __init__(self,x,y):
        self.x = x
        self.y = y

def in_geo():
    # implement with ray casting algorithm
    return False

def compute_centroid(lst):
    centroid = Point2D(0,0)
    signedArea = 0

    for idx, i in enumerate(lst):
        x0 = i.x
        y0 = i.y
        x1 = lst[(idx + 1) % len(lst)].x
        y1 = lst[(idx + 1) % len(lst)].y
        a = x0*y1 - x1*y0
        signedArea += a
        centroid.x += (x0 + x1)*a
        centroid.y += (y0 + y1)*a

    signedArea = signedArea*0.5
    centroid.x = centroid.x / (6*signedArea)
    centroid.y = centroid.y / (6*signedArea)

    return centroid

def parse_placemark(geos, p):
    """Splits the kml description into name, area, lat, lng"""
    try:
        name = p.name.rstrip().lstrip().replace('/','').replace(',','')
        if p.geometry.geom_type == 'LineString':
            coord_lst = [Point2D(i.x,i.y) for i in p.geometry.geoms]
        elif(p.geometry.geom_type == 'MultiPolygon'):
            for idx,i in enumerate(p.geometry.geoms):
                coord_lst = [Point2D(j[0],j[1]) for j in i.exterior.coords]
                centroid = compute_centroid(coord_lst)
                geos.write(name + str(idx) + ',' + str(centroid.y) + ',' + str(centroid.x) + '\n')
            return
        else:
            coord_lst = [Point2D(i[0],i[1]) for i in p.geometry.exterior.coords]

    except() as err:
        print(err)
        print(name)
        print(p.geometry.geoms)
        sys.exit(0)

    centroid = compute_centroid(coord_lst)
    geos.write(name + ',' + str(centroid.y) + ',' + str(centroid.x) + '\n')

def parse_kml(fname):    
    with open(fname, 'rb') as f:
        """Opens kml file and outputs geos into coords.txt"""
        doc = f.read()
        k = kml.KML()
        k.from_string(doc)

        #new version
        features = list(k.features())
        placemarks = list(features[0].features())

        geos = open(os.path.join(os.path.dirname(__file__), '../coords.txt'), 'w')
        for p in placemarks:
            parse_placemark(geos, p)

        geos.close()
    f.close()
