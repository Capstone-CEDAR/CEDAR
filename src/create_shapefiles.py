import json
import shapefile
from pyproj import Proj

RESOLUTION = 100  # in meters
BOUND_DISTANCE = RESOLUTION / 2  # distance from middle utm point to edge of bounding polygon
GEOJSON_FILE = '../out/all_data_' + str(RESOLUTION) + '.geojson'
SHAPEFILE_PATH = '../out/shapefiles/' + str(RESOLUTION) + '/'
UTM_10_PROJ = Proj("+proj=utm +zone=10N, +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")

'''
Given a pair of utm coordinates, calculate the bounding rectangle
around them for a resolution of RESOLUTION

x: the utm x coordinate of the middle of the rectangle
y: the utm y coordinate of the middle of the rectangle

return: a polygon
'''
def get_polygon_from_middle(x, y):
    top_x = x + BOUND_DISTANCE
    bottom_x = x - BOUND_DISTANCE
    top_y = y + BOUND_DISTANCE
    bottom_y = y - BOUND_DISTANCE

    top_lon, top_lat = UTM_10_PROJ(top_x, top_y, inverse=True)
    bottom_lon, bottom_lat = UTM_10_PROJ(bottom_x, bottom_y, inverse=True)

    return [[[top_lon, top_lat], [top_lon, bottom_lat],
             [bottom_lon, bottom_lat], [bottom_lon, top_lat],
             [top_lon, top_lat]]]


'''
Given utm coordinates, create three files in the SHAPEFILE_PATH directory:
    (x_y).shp
    (x_y).dbz
    (x_y).shx

The .shp file can be used with iTree Canopy or ArcGIS. It contains a 
single rectangular polygon with (x,y) as the middle utm coordinate.

x: the utm x coordinate of the middle of the rectangle
y: the utm y coordinate of the middle of the rectangle
'''
def create_shapefile_from_middle(x, y):
    location = '(' + str(x) + '_' + str(y) + ')'
    writer = shapefile.Writer(SHAPEFILE_PATH + location)
    writer.shapeType = shapefile.POLYGON
    writer.autoBalance = 1
    writer.field('field1', 'C')
    writer.poly(get_polygon_from_middle(x, y))
    writer.close()

########################################

# TODO: add command line arguments so that you can specify which shapefile to create
# because the current number of files is ridiculous


geojson_data = json.load(open(GEOJSON_FILE))
features = geojson_data['features']

for feature in features:
    utm_10_x = feature['properties']['utm_10_x']
    utm_10_y = feature['properties']['utm_10_y']
    create_shapefile_from_middle(utm_10_x, utm_10_y)
