import api as a
import kml as k
import os

def run():

    k.parse_kml(os.path.join(os.path.dirname(__file__),'kml/C1Dense.kml'))    # f_coords =     os.path.join(os.path.dirname(__file__), 'coords.txt')
    # if os.path.isfile(f_coords):
    #     a.read_geos()
    # else:
    #     # get coords file
    #     k.parse_kml(os.path.join(os.path.dirname(__file__),'kml/C1Dense.kml'))

run()