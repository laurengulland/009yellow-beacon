# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 16:38:34 2017

@author: Joseph
"""

import requests
from PIL import Image
from io import BytesIO


def make_map_request(clat,clon,zoom=15,szw=640,szh=640,scale=1,frmt='png',maptype='roadmap',):
    clat = str(clat)
    clon = str(clon)
    zoom = str(zoom)
    szw = str(szw)
    szh = str(szh)
    scale = str(scale)
    request_string = "https://maps.googleapis.com/maps/api/staticmap?"
    request_string = request_string+'center='+clat+','+clon
    request_string = request_string+'&zoom='+zoom
    request_string = request_string+'&size='+szw+'x'+szh
    request_string = request_string+'&scale='+scale
    request_string = request_string+'&format='+frmt
    request_string = request_string+'&maptype='+maptype
    request_string = request_string+'&key=AIzaSyCqgtCrKQk0d2SOlpgZEh8miNB0xvP2KrU'
    r=requests.get(request_string)
    i=Image.open(BytesIO(r.content))
    return i
    

#r = requests.get("https://maps.googleapis.com/maps/api/staticmap?center=42.3582,-71.0927&zoom=15&size=640x640&key=AIzaSyCqgtCrKQk0d2SOlpgZEh8miNB0xvP2KrU&scale=2")
#i = Image.open(BytesIO(r.content))
#i.show()

make_map_request(42.3582,-71.0927,20,640,640,2).show()