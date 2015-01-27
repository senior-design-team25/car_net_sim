
from itertools import *
from functools import partial
from random import random
import math
from vmath import *
from Car import Car

from PySide.QtGui import *
from PySide.QtCore import *


MAP_WIDTH = 100
MAP_HEIGHT = 100

LANE_WIDTH = 1
LINE_WIDTH = 0.125

LINE_BYTES = '\xff\xff\xff\xff\x00\x00\x00\x00'
LINE_PATTERN = QImage(LINE_BYTES, 1, 2, QImage.Format_ARGB32_Premultiplied)


# Representation of a single road

class RoadGraphic(QGraphicsItem):
    def __init__(self, start, end, lanes):
        super(RoadGraphic, self).__init__()
        
        self.lanes = lanes
        self.length = dist(start, end)
        self.setPos(start.x, start.y)
        self.setRotation(math.degrees(angle(end-start, vec(0,1))))

    def boundingRect(self):
        width = LANE_WIDTH*sum(self.lanes) + LINE_WIDTH
        
        return QRectF(-width/2, 0, width, self.length)
     
    def paint(self, painter, option, widget):
        width = LANE_WIDTH*sum(self.lanes) + LINE_WIDTH
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.black)
        painter.drawRect(QRectF(-width/2, 0, width, self.length))
        painter.setBrush(Qt.gray)
        painter.drawRect(QRectF(-width/2+LINE_WIDTH, 0, width-2*LINE_WIDTH, self.length))
        painter.setBrush(Qt.yellow)
        painter.drawRect(QRectF(-LINE_WIDTH/2, 0, LINE_WIDTH, self.length))
        
        painter.setBrush(Qt.white)
        painter.setBrush(LINE_PATTERN)
        
        for i in xrange(1, self.lanes[0]):
            painter.drawRect(QRectF(-LANE_WIDTH*i-LINE_WIDTH/2, 0, LINE_WIDTH, self.length))
            
        for i in xrange(1, self.lanes[1]):
            painter.drawRect(QRectF(LANE_WIDTH*i-LINE_WIDTH/2, 0, LINE_WIDTH, self.length))
            
            
class Road:
    def __init__(self, start, end, lanes):
        self.start = start
        self.end = end
        self.lanes = lanes
        
        self.graphic = RoadGraphic(start, end, lanes)
    
    def step(self, dt):
        return True
        
    def target(self, side):
        def target(self, side, start, end, car):
            if isnear(car.pos, end):
                car.target = self.nt[side]
                
            return end
        
        if side:
            return partial(target, self, side, self.end, self.start-vec(10,10))
        else:
            return partial(target, self, side, self.start, self.end+vec(10,10))
        

# Car entry into system
        
class Spawner:
    def __init__(self, chance, pos, head, lanes):
        self.pos = pos
        self.head = head
        self.lanes = lanes
    
        # probability of a car entering every second
        self.chance = chance 
        
    def step(self, dt):    
        if random() < dt*self.chance:
            self.map.add(Car(self.nt[0], 0, self.pos, self.head))
    
    def target(self):
        def target(self, car):
            return None
            
        return partial(target, self)


# Representation of all static world elements

class MapGraphic(QGraphicsItem):
    def boundingRect(self):
        return QRectF(0, 0, MAP_WIDTH, MAP_HEIGHT)
     
    def paint(self, painter, option, widget):
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.black)
        painter.drawRect(-MAP_WIDTH, -MAP_HEIGHT, 3*MAP_WIDTH, 3*MAP_HEIGHT)
        painter.setBrush(Qt.darkGreen)
        painter.drawRect(0, 0, MAP_WIDTH, MAP_HEIGHT)
     
     
class Map:
    def __init__(self):
        self.graphic = MapGraphic()
        self.entities = []
        
        r = Road(vec(0, 0), vec(MAP_WIDTH, MAP_HEIGHT), (2,2))
        s0 = Spawner(2, vec(0, 0), vec(1,1).norm(), (2,2))
        s1 = Spawner(2, vec(100, 100), vec(-1,-1).norm(), (2,2))
        
        r.nt = s0.target(), s1.target()
        s0.nt = r.target(0),
        s1.nt = r.target(1),
        
        self.add(r)
        self.add(s0)
        self.add(s1)
        
             
    def add(self, entry):
        entry.map = self
    
        self.entities.append(entry)
        
        if hasattr(entry, 'graphic'):
            entry.graphic.setParentItem(self.graphic)
            
    def remove(self, entry):
        self.entities.remove(entry)
        
        if hasattr(entry, 'graphic'):
            entry.graphic.setParentItem(None)
             
    def step(self, dt):
        for i in self.entities:
            i.step(dt)