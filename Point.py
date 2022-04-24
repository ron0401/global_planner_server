import pymap3d
import numpy as np
import uuid
from pykml import parser
import zipfile
from typing import List

class geo_point:
    def __init__(self,lat,lon):
        self.Latitude = lat
        self.Longitude = lon


class LocalPoint:
    def __init__(self,x,y,z) -> None:
        self.x = x
        self.y = y
        self.z = z

    @property
    def vector(self):
        return np.array([self.x,self.y,self.z])

    @staticmethod
    def get_local_point_from_geo(geo:geo_point,datum:geo_point):
        e,n,u = pymap3d.geodetic2enu(geo.Latitude,geo.Longitude,0,datum.Latitude,datum.Longitude,0)
        return LocalPoint(e,n,0)

def get_geopoint_from_localpoint(point:LocalPoint,datum:geo_point):
    lat,lon,h = pymap3d.enu2geodetic(point.x,point.y,point.z,datum.Latitude,datum.Longitude,0)
    return geo_point(lat,lon)

class MapPoint(LocalPoint):
    """AA"""
    def __init__(self, x, y, z) -> None:
        super().__init__(x, y, z)
    


def get_localpoints_distance(p1:LocalPoint,p2:LocalPoint):
    v = p1.vector - p2.vector
    return np.linalg.norm(v,ord=2)

class GeoObject:
    class route:
        def __init__(self) -> None:
            self.points = List[geo_point]
            pass
    def __init__(self,kmzpath) -> None:
        self.Routes = []
        geos = get_geo_points_from_kmz(kmzpath)
        for i in geos:
            g = GeoObject.route()
            g.points = i
            self.Routes.append(g)
        pass

def get_geo_points_from_kmz(path:str):
    with zipfile.ZipFile(path) as zf:
        with zf.open('doc.kml') as f:
            b = f.read()

    root = parser.fromstring(b)
    mark = root.Document.Folder.Placemark

    ret = []
    for m in mark:
        r = []
        corstr = str(m.LineString.coordinates.text)
        corstr = corstr.replace('\t', ' ')
        corstr = corstr.replace('\n', ' ')
        while ('  ' in corstr):
            corstr = corstr.replace('  ', ' ')
        p = corstr.split(' ')
        for i in p:
            try:
                g = geo_point(float(i.split(',')[1]),float(i.split(',')[0]))
                r.append(g)
            except:
                pass
        ret.append(r)
    return ret

def complement_localpoints(points:list,th:float):
    def get_unique_list(seq):
        seen = []
        return [x for x in seq if x not in seen and not seen.append(x)]
    p = points
    if len(p) < 2:
        return None
    ans = []
    for i in range(len(p) - 2):
        dis = get_localpoints_distance(p[i],p[i + 1])
        if dis > th:
            q = dis // th
            x_latent = np.linspace(p[i].x, p[i + 1].x , int(q + 2))
            y_latent = np.linspace(p[i].y, p[i + 1].y , int(q + 2))
            xy = list(map(list, zip(x_latent,y_latent)))
            ans = ans + xy
            h = 1
            pass
        pass
    return get_unique_list(ans)

def complement_geo_points(points:list, th:float):
    p = []
    for i in points:
        p.append(LocalPoint.get_local_point_from_geo(i,points[0]))
    ans = complement_localpoints(p,th)
    lst = []
    for i in ans:
        p = LocalPoint(i[0],i[1],0)
        lst.append(get_geopoint_from_localpoint(p,points[0]))
    return lst
    
def get_localpoints_from_geopoints(geos:list,datum:geo_point):
    i:geo_point
    ret = []
    for i in geos:
        ret.append(LocalPoint.get_local_point_from_geo(i,datum))
    return ret

