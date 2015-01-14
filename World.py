
import Tkinter as tk
from itertools import *

# Representation of viewable world

class World:
    x = 0
    y = 0
    s = 1
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.lines = [ canvas.create_line(0,0,0,0),
                       canvas.create_line(0,0,0,0) ]
                       
        self.update()
        
    def t(self, *vargs):
        return (o + s*c for c,(o,s) in 
                izip(vargs, cycle(((self.x, self.s), (self.y, self.s)))))
                
    def move(self, x, y):
        self.x += x
        self.y += y
        self.update()
        
    def scale(self, x, y, s):
        self.s *= s
        self.x = ((self.x-x)*s+x)
        self.y = ((self.y-y)*s+y)
        self.update()
        
    def update(self):
        self.canvas.coords(self.lines[0], *self.t(0, 0, 100, 100))
        self.canvas.coords(self.lines[1], *self.t(0, 100, 100, 0))