import api as a
import kml as k
import os
import sys

def run():

    #check to see if there is a kmo file
    #delete coords.txt and everything in result/
    #create coords.txt
    coords = k.parse_kml(os.path.join(os.path.dirname(__file__),'kml/C1Dense.kml'))
    
    #query api
    for i in coords:
        for j in i:
            a.query_yelp(j)

run()