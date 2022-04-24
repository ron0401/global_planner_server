import numpy as np
import RoboMap
import Point
import matplotlib.pyplot as plt
m = RoboMap.robomap()
m.datum = Point.geo_point(35.681721,139.764431)
geos = Point.GeoObject('myroute.kmz')
for i in geos.Routes:
    m.AddGeoPoints(Point.complement_geo_points(i.points,0.25))

m.Save('data.json')

m2 = RoboMap.robomap(filepath='data.json')
m2.GenerateLinks(th=0.3)
pass
