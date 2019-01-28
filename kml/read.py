#!/bin/env python3
from fastkml import kml
import re
import os, sys
import traceback
import json

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class GeoFence:
    def __init__(self, name, lat, lng, coord_lst):
        self.name = name
        self.lat = lat
        self.lng = lng
        #4000m ~ about 25 miles
        self.radius = 40000
        #list of Point objects
        self.coord_lst = coord_lst
        self.edges = self.get_edges()
        self.restaurants = []

    def get_edges(self):
        ''' Returns a list of tuples that each contain 2 points of an edge '''
        edge_list = []
        for i,p in enumerate(self.coord_lst):
            p1 = p
            p2 = self.coord_lst[(i+1) % len(self.coord_lst)]
            edge_list.append((p1,p2))
        return edge_list

    def in_geo(self, point):
        # implement with ray casting algorithm
        # _huge is used to act as infinity if we divide by 0
        _huge = sys.float_info.max
        # _eps is used to make sure points are not on the same line as vertexes
        _eps = 0.00001

        # We start on the outside of the polygon
        inside = False
        for edge in self.edges:
            # Make sure A is the lower point of the edge
            A, B = edge[0], edge[1]
            if A.y > B.y:
                A, B = B, A

            # Make sure point is not at same height as vertex
            if point.y == A.y or point.y == B.y:
                point.y += _eps

            if (point.y > B.y or point.y < A.y or point.x > max(A.x, B.x)):
                # The horizontal ray does not intersect with the edge
                continue

            if point.x < min(A.x, B.x): # The ray intersects with the edge inside = not inside continue try: m_edge = (B.y - A.y) / (B.x - A.x) except ZeroDivisionError: m_edge = _huge try: m_point = (point.y - A.y) / (point.x - A.x) except ZeroDivisionError: m_point = _huge if m_point >= m_edge:
                # The ray intersects with the edge
                inside = not inside
                continue

        return inside

    def write_to_file(self, business, out):
        out.write(business['name'] + '\n')
        for j in business['location']['display_address']:
            out.write(j + ', ')
        out.write('\n')
        out.write(business['phone'] + '\n')
        out.write(business['url'] + '\n')
        out.write(str(business['coordinates']['latitude'])+',')
        out.write(str(business['coordinates']['longitude'])+ '\n')
        out.write('\n')

def compute_centroid(lst):
    centroid = Point(0,0)
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

def get_coords(p):
    try:
        name = p.name.rstrip().lstrip().replace('/','').replace(',','')

        if p.geometry.geom_type == 'LineString':
            coord_lst = [Point(i.x,i.y) for i in p.geometry.geoms]
        elif (p.geometry.geom_type == 'MultiPolygon'):
            lst = []
            for idx,i in enumerate(p.geometry.geoms):
                coord_lst = [Point(j[0],j[1]) for j in i.exterior.coords]
                centroid = compute_centroid(coord_lst)
                lst.append(GeoFence(name + str(idx), centroid.y,centroid.x, coord_lst))
            return lst
        else:
            coord_lst = [Point(i[0],i[1]) for i in p.geometry.exterior.coords]

    except() as err:
        print(err)
        print(name)
        print(p.geometry.geoms)
        sys.exit(0)

    centroid = compute_centroid(coord_lst)
    return [GeoFence(name,centroid.y, centroid.x,coord_lst)]


def parse_kml(fname):    
    with open(fname, 'rb') as f:
        doc = f.read()
        k = kml.KML()
        k.from_string(doc)

        features = list(k.features())
        placemarks = list(features[0].features())

        coord_lst = [get_coords(p) for p in placemarks]
        # print(coord_lst)
    f.close()
    return coord_lst