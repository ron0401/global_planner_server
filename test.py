
import RoboMap
import Point

# p1 = Point.geo_point(35.681721,139.764431)
# p2 = Point.geo_point(35.681835,139.763942)
# p3 = Point.geo_point(35.681639,139.763943)

# lp1 = Point.LocalPoint.get_local_point_from_geo(p2,p1)
# lp2 = Point.LocalPoint.get_local_point_from_geo(p3,p1)

# n = Point.get_localpoints_distance(lp1,lp2)


import numpy as np
import RoboMap
import Point
import matplotlib.pyplot as plt
geos = Point.get_geo_points_from_kmz('route.kmz')
geos2 = Point.get_geo_points_from_kmz('route2.kmz')


a = Point.complement_geo_points(geos,1) + Point.complement_geo_points(geos2,1)


pass
