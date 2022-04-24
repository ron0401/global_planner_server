"""AAA"""

from folium import Link
from Point import geo_point,LocalPoint,MapPoint
import Point
from typing import List,Dict
import json
import uuid
import pandas as pd

class robomap:
    
    class NodeLink:
        def __init__(self,src = '',tgt = '',cost = 0) -> None:
            self.source = src
            self.target = tgt
            self.cost = cost
    
    def __init__(self,filepath:str = None) -> None:
        self.datum:geo_point
        self.points:Dict[MapPoint] = {}
        self.__filepath = filepath
        if filepath != None:
            f = open(filepath, 'r')
            json_dict = json.load(f)
            for k,v in json_dict['points'].items():
                self.points[k] = MapPoint(float(v['x']),float(v['y']),float(v['z']))
                self.datum = geo_point(float(json_dict['datum']['lat']),float(json_dict['datum']['lon']))
    
    def GenerateLinks(self,th = 1):
        # df = pd.DataFrame(self.points.keys())
        self.Links = []
        df = pd.DataFrame(list(zip(self.points.keys(),self.points.values())),columns=['id','points'])
        for key,val in self.points.items():
            df['dist'] = df['points'].apply(lambda x: Point.get_localpoints_distance(x,val))
            df_temp = df[df['dist'] < th].copy()
            dic = dict(zip(df_temp['id'].to_list(),df_temp['dist'].to_list()))
            for k,v in dic.items():
                link = robomap.NodeLink()
                link.source = key
                link.target = k
                link.cost = v
                self.Links.append(link)
                


    def AddGeoPoints(self,points:List[geo_point]):
        for i in points:
            p = LocalPoint.get_local_point_from_geo(i,self.datum)
            m = LocalPoint(p.x,p.y,p.z)
            self.points[str(uuid.uuid4())] = m

    def Save(self,path):
        obj = {}
        obj['points'] = {}
        for k,v in self.points.items():
            item = dict()
            item['x'] = v.x
            item['y'] = v.y
            item['z'] = v.z
            obj['points'][k] = item
        obj['datum'] = {}
        obj['datum']['lat'] = self.datum.Latitude
        obj['datum']['lon'] = self.datum.Longitude
        j = open(path, "w")
        json.dump(obj,j)

