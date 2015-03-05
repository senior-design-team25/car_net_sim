
from vmath import *
import math
from random import random
from config import global_config as config

from PySide.QtGui import *
from PySide.QtCore import *


class CarGraphic(QGraphicsItem):
    def __init__(self, pos, head):
        super(CarGraphic, self).__init__()
        self.set(pos, head)
        
    def set(self, (x,y), head):
        self.setPos(x, y)
        self.setRotation(math.degrees(angle(head, vec(0,1))))

    def boundingRect(self):
        return QRectF(-Car.WIDTH/2, -Car.HEIGHT/2, Car.WIDTH, Car.HEIGHT)
     
    def paint(self, painter, option, widget):
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.black)
        painter.drawRect(QRectF(-Car.WIDTH/2, -Car.HEIGHT/2, Car.WIDTH, Car.HEIGHT))
        painter.setBrush(Qt.yellow)
        painter.drawRect(QRectF(-Car.WIDTH/2+CarGraphic.LINE, -Car.HEIGHT/2+CarGraphic.LINE, 
                                Car.WIDTH-2*CarGraphic.LINE, Car.HEIGHT-2*CarGraphic.LINE))
        
        painter.setBrush(Qt.black)
        painter.drawRect(QRectF(-Car.WIDTH/2+CarGraphic.LINE, -Car.HEIGHT/4, 
                                Car.WIDTH-2*CarGraphic.LINE, 0.375*Car.HEIGHT))
        painter.setBrush(Qt.yellow)
        painter.drawRect(QRectF(-Car.WIDTH/2+CarGraphic.LINE, -Car.HEIGHT/4+CarGraphic.LINE, 
                                Car.WIDTH-2*CarGraphic.LINE, 0.375*Car.HEIGHT-2*CarGraphic.LINE))
                                
config.use('LINE_WIDTH', 0.125, CarGraphic, 'LINE', float)

        
# Representation of a car

class Car:
    def __init__(self, target, lane, pos, head=vec(0,0), vel=vec(0,0)):
        config.use('CAR_MASS', 100.0, self, 'mass')
        config.use('CAR_MAX_FORCE', 2000.0, self, 'max_force')
        config.use('CAR_MAX_SPIN', 1.0, self, 'max_spin')
        config.use('CAR_MAX_SPEED', 35.0, self, 'max_speed')
        
        config.use('LOOKAHEAD_TIME', 1.5, self, 'lookahead_time')
        config.use('LOOKAHEAD_MIN', self.HEIGHT, self, 'lookahead_min')
        
        config.use('REACTION_TIME', 1.0, self, 'reaction_time')
        config.use('LANE_CHANGE_CHANCE', 1.0, self, 'lane_change_chance')
    
        self.target = target
        self.lane = lane
        self.pos = pos
        self.head = head
        self.vel = vel
        
        self.graphic = CarGraphic(pos, self.head)
        
    def stopdist(self):
        s = self.vel.len()
        t = self.reaction_time + (s * self.mass)/self.max_force
        d = s*t - (self.max_force * t**2) / (2*self.mass)
        return d + Car.HEIGHT
    
        #return 0.5*self.mass*(self.max_speed**2) / self.max_force
        
    def radius(self):
        return math.sqrt((Car.WIDTH/2)**2 + (Car.HEIGHT/2)**2)
            
    def step(self, dt):    
        # Find target force
        target = self.target
        t = target(self)
        
        if not t:
            self.map.remove(self)
            return
        
        v = self.max_speed * (t - self.pos).norm()
        
        # Find collision avoiding forces
        stopdist = self.stopdist()
        
        nbors = [(c, c.pos - self.pos) for c in self.map.vehicles
                 if c.pos - self.pos < stopdist and c != self]
        
        fnbors = [(c,d) for c,d in nbors
                  if projectunit(d, ~self.head) < Car.WIDTH and
                     d * self.head > 0]
                  
        if fnbors:
            fd = min(d*self.head for _,d in fnbors)
            v *= max((fd - Car.HEIGHT) / stopdist, 0)
            
            # Decide if we want to change lanes
            if random() < dt*self.lane_change_chance and \
               projectunit(t-self.pos, ~target.head) < Car.WIDTH/4:
                rnbors = [(c,d) for c,d in nbors
                          if projectunit(d, ~target.head) < 2*target.width and
                             d * ~target.head > 0]
                        
                lnbors = [(c,d) for c,d in nbors
                          if projectunit(d, ~target.head) < 2*target.width and
                             d * ~target.head < 0]
                      
                rd = min(d*target.head for _,d in rnbors) if rnbors else vec(1e309,1e309)
                ld = min(d*target.head for _,d in lnbors) if lnbors else vec(1e309,1e309)
                
                if rd/3 > fd and self.lane < target.lanes-1:
                        self.lane += 1
                elif ld/3 > fd and self.lane > 0:
                        self.lane -= 1
        
        # Find total driving force
        force = self.mass/dt * (v-self.vel)
        
        # Simulate actual driving
        if force.lensq() > self.max_force**2:
            force = self.max_force*force.norm()
            
        vel = self.vel + (force*dt)/self.mass
        spin = angle(vel, self.head)
        
        if vel.iszero():
            head = self.head
        elif spin > self.max_spin*dt:
            head = self.head.rotate(self.max_spin*dt)
            vel = projectunit(vel, head)
        elif spin < -self.max_spin*dt:
            head = self.head.rotate(-self.max_spin*dt)
            vel = projectunit(vel, head)
        else:
            head = vel.norm()
            
        if vel.lensq() > self.max_speed**2:
            vel = self.max_speed*vel.norm()
            
        self.vel = vel
        self.head = head
        self.pos += dt*vel
        
        self.graphic.set(self.pos, self.head)
        
config.use('CAR_WIDTH', 1.0, Car, 'WIDTH')
config.use('CAR_HEIGHT', 2.0, Car, 'HEIGHT')


