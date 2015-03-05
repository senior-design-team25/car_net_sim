
from itertools import *
from random import *
import math
from vmath import *
from config import global_config as config
from car import Car

from PySide.QtGui import *
from PySide.QtCore import *


MAP_WIDTH = 100
MAP_HEIGHT = 100

LANE_WIDTH = 1
LINE_WIDTH = 0.125




# Representation of a single road

class RoadGraphic(QGraphicsItem):
    LINE_BYTES = '\xff\xff\xff\xff\x00\x00\x00\x00'
    LINE_PATTERN = QImage(LINE_BYTES, 1, 2, QImage.Format_ARGB32_Premultiplied)

    def __init__(self, start, end, lanes):
        super(RoadGraphic, self).__init__()
        
        self.lanes = lanes
        self.length = dist(start, end)
        self.setPos(start.x, start.y)
        self.setRotation(math.degrees(angle(end-start, vec(0,1))))

    def boundingRect(self):
        width = Road.LANE*sum(self.lanes) + RoadGraphic.LINE
        
        return QRectF(-width/2, 0, width, self.length)
     
    def paint(self, painter, option, widget):
        width = Road.LANE*sum(self.lanes) + RoadGraphic.LINE
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.black)
        painter.drawRect(QRectF(-width/2, 0, width, self.length))
        painter.setBrush(Qt.gray)
        painter.drawRect(QRectF(-width/2+RoadGraphic.LINE, 0, width-2*RoadGraphic.LINE, self.length))
        painter.setBrush(Qt.yellow)
        painter.drawRect(QRectF(-RoadGraphic.LINE/2, 0, RoadGraphic.LINE, self.length))
        
        painter.setBrush(Qt.white)
        painter.setBrush(RoadGraphic.LINE_PATTERN)
        
        for i in xrange(1, self.lanes[0]):
            painter.drawRect(QRectF(-Road.LANE*i-RoadGraphic.LINE/2, 0, RoadGraphic.LINE, self.length))
            
        for i in xrange(1, self.lanes[1]):
            painter.drawRect(QRectF(Road.LANE*i-RoadGraphic.LINE/2, 0, RoadGraphic.LINE, self.length))
            
config.use('LINE_WIDTH', 0.125, RoadGraphic, 'LINE', float)
            
            
class Road:
    def __init__(self, start, end, lanes):
        self.start = start
        self.end = end
        self.lanes = lanes
        
        self.graphic = RoadGraphic(start, end, lanes)
    
    def step(self, dt):
        pass
        
    def target(self, side):
        start = self.end if side else self.start
        end = self.start if side else self.end
        head = (end - start).norm()
    
        def target(car):
            if head * (car.pos - end) > 0:
                car.target = self.nt[side]
                return car.target(car)
                
            lookahead = car.lookahead_time*abs(car.vel*head)
            lookahead = max(lookahead, car.lookahead_min) * head
            
            offset = car.lane*Road.LANE + Road.LANE/2.0
            lstart = start + (offset * ~head)
            target = projectunit(car.pos - lstart, head) + lstart
                
            return target + lookahead
            
        target.lanes = self.lanes[side]
        target.width = Road.LANE
        target.head = head
            
        return target 

config.use('LANE_WIDTH', 1.0, Road, 'LANE', float)
        

# Car entry into system
        
class Spawner:
    def __init__(self, pos, head, lanes):
        self.pos = pos
        self.head = head
        self.lanes = lanes
        
        config.use('SPAWN_CHANCE', 10.0, self, 'spawn_chance')
        
    def step(self, dt):
        lane = randint(0, self.lanes[0]-1)
        
        offset = lane*Road.LANE + Road.LANE/2.0
        offset = (offset * ~self.head) + self.pos
    
        if random() < dt*self.spawn_chance:
            self.map.add(Car(self.nt[0], lane, offset, self.head))
    
    def target(self):
        return lambda car: None


# Representation of all static world elements

class MapGraphic(QGraphicsItem):
    def boundingRect(self):
        return QRectF(0, 0, Map.WIDTH, Map.HEIGHT)
     
    def paint(self, painter, option, widget):
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.black)
        painter.drawRect(-Map.WIDTH, -Map.HEIGHT, 3*Map.WIDTH, 3*Map.HEIGHT)
        painter.setBrush(Qt.darkGreen)
        painter.drawRect(0, 0, Map.WIDTH, Map.HEIGHT)
     
     
class Map:
    def __init__(self):
        self.graphic = MapGraphic()
        self.entities = []
        self.vehicles = []
        
        #r = Road(vec(0, 0), vec(Map.WIDTH, Map.HEIGHT), (2,2))
        #s0 = Spawner(vec(0, 0), vec(1,1).norm(), (2,2))
        #s1 = Spawner(vec(100, 100), vec(-1,-1).norm(), (2,2))
        r = Road(vec(0, 50), vec(100, 50), (5,5))
        s0 = Spawner(vec(0, 50), vec(1,0).norm(), (5,5))
        s1 = Spawner(vec(100, 50), vec(-1,0).norm(), (5,5))
        
        r.nt = s0.target(), s1.target()
        s0.nt = r.target(0),
        s1.nt = r.target(1),
        
        self.add(r)
        self.add(s0)
        self.add(s1)
             
    def add(self, entry):
        entry.map = self
    
        if isinstance(entry, Car):
            self.vehicles.append(entry)
        else:
            self.entities.append(entry)
        
        if hasattr(entry, 'graphic'):
            entry.graphic.setParentItem(self.graphic)
            
    def remove(self, entry):
        try:
            self.vehicles.remove(entry)
        except:
            self.entities.remove(entry)
        
        if hasattr(entry, 'graphic'):
            entry.graphic.setParentItem(None)
             
    def step(self, dt):
        for i in self.vehicles:
            i.step(dt)
        for i in self.entities:
            i.step(dt)
    
config.use('MAP_WIDTH', 100, Map, 'WIDTH', int)
config.use('MAP_HEIGHT', 100, Map, 'HEIGHT', int)

            
