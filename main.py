import api as a
import kml as k
import os

def run():

    #check to see if there is a kmo file
    #delete coords.txt
    #create coords.txt
    k.parse_kml(os.path.join(os.path.dirname(__file__),'kml/C1Dense.kml'))
    
    #query api
    a.read_geos()
    # if os.path.isfile(f_coords):
    #     a.read_geos()
    # else:
    #     # get coords file
    #     k.parse_kml(os.path.join(os.path.dirname(__file__),'kml/C1Dense.kml'))

run()