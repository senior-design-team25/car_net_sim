
import Tkinter as tk
from itertools import *
from vmath import *
from Map import Map

# Representation of viewable world

class World:
    width = 100
    height = 100

    _offset = vec(0,0)
    _scale = 1
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.objs = []
        
        self.createobj(vec(self.width/2,0), 0,
            [(vec(0,0), vec(0,self.height), self.width, {'fill':'darkgreen'})])
        
        self.map = Map(self)
                       
        self.update()
        
    def move(self, offset):
        self._offset += offset
        self.update()
        
    def scale(self, offset, scale):
        self._scale *= scale
        self._offset = (self._offset-offset)*scale + offset
        self.update()
        
    def transform(self, v):
        if isiter(v):
            return self._scale*v + self._offset
        else:
            return self._scale*v
        
    def createobj(self, pos, rot, desc):
        obj = []
    
        for s,e,w,d in desc:
            i = self.canvas.create_line(0,0,0,0, width=self.transform(w), **d)
            obj.append((i,s,e,w))
        
        id = len(self.objs)
        self.objs.append((None, None, obj))
        self.moveobj(id, pos, rot)
        
        return id
        
    def moveobj(self, id, pos, rot):
        _,_,obj = self.objs[id]
        
        for (i,s,e,_) in obj:
            sx, sy = self.transform(s.rotate(rot) + pos)
            ex, ey = self.transform(e.rotate(rot) + pos)
            self.canvas.coords(i, sx, sy, ex, ey)
        
        self.objs[id] = (pos, rot, obj)
        
    def update(self):
        for pos,rot,obj in self.objs:
            for (i,s,e,w) in obj:
                sx, sy = self.transform(s.rotate(rot) + pos)
                ex, ey = self.transform(e.rotate(rot) + pos)
                self.canvas.coords(i, sx, sy, ex, ey)
                self.canvas.itemconfig(i, width=self.transform(w))
    
    def step(self, dt):
        self.map.step(self, dt)
        