# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 10:16:42 2019

@author: jazzn
"""
import plotly.graph_objs as go
from plotly.offline import  iplot
import numpy as np

class PLT:
    def __init__(self):
        self.scatter = []
        self.layout = go.Layout()
        
    def plot(self,*args, scalex=True, scaley=True, data=None, **kwargs):
        courbe = go.Scatter()
        if len(args)==1:
            courbe = go.Scatter(x = np.arange(0,len(args[0])),y= args[0])
        elif len(args)==2:
            courbe = go.Scatter(x=args[0],y=args[1])
        try:
            if args[2] in locals():
                courbe['marker'] = dict(size=4)
        except:
            pass
        if kwargs.get('label',None) != None:
            courbe['name'] = kwargs['label']
        self.scatter.append(courbe)
    
    def title(self,s):
        self.layout['title'] = s
        
    def xlabel(self,s):
        self.layout['xaxis']['title'] = s
        
    def ylabel(self,s):
        self.layout['yaxis']['title'] = s    
    
    def show(self):
        fig = go.Figure(data=self.scatter, layout=self.layout)
        self.__init__()
        return iplot(fig,filename="titre")