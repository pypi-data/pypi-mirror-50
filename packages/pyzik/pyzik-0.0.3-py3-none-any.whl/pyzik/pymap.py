# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 23:38:07 2019

@author: jazzn
"""

import plotly.graph_objects as go

class Map:
    def __init__(self,lat,lon,access_token):
        self.access_token = access_token
        self.lon0 = lon
        self.lat0 = lat
        self.fig = go.Figure(go.Scattermapbox(lat=[str(lat)],lon=[str(lon)],mode='markers',marker=go.scattermapbox.Marker(size=1)))
        self.lon=[]
        self.lat=[]
        self.colors = []
        self.texts = []
        
    def set_circle(self,lat,lon,size=9,color='magenta',text=''):
        lat = str(lat)
        lon = str(lon)
        self.lon.append(lon)
        self.lat.append(lat)
        self.colors.append(color)
        self.texts.append(text)
        self.fig = go.Figure(go.Scattermapbox(lat=self.lat,lon=self.lon,mode='markers',marker=go.scattermapbox.Marker(size=size,color=self.colors),text=self.texts))

    def show(self,zoom=5,style=None):
        self.fig.update_layout(autosize=True,hovermode='closest',mapbox=go.layout.Mapbox(accesstoken=self.access_token,bearing=0,center=go.layout.mapbox.Center(
            lat=self.lat0,lon=self.lon0),pitch=0,zoom=zoom,style=style))
        return self.fig.show()