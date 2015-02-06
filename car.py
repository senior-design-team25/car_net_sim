
from vmath import *
import math
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
    def __init__(self, target, lane, pos, head=vec(0,0), vel=None):
        config.use('CAR_MASS', 100.0, self, 'mass')
        config.use('CAR_MAX_FORCE', 2000.0, self, 'max_force')
        config.use('CAR_MAX_SPIN', 1.0, self, 'max_spin')
        config.use('CAR_MAX_SPEED', 35.0, self, 'max_speed')
        
        config.use('LOOKAHEAD_TIME', 1.5, self, 'lookahead_time')
        config.use('LOOKAHEAD_MIN', self.HEIGHT, self, 'lookahead_min')
    
        self.target = target
        self.lane = lane
        self.pos = pos
        self.head = head
        self.vel = vel or self.max_speed*head
        
        self.graphic = CarGraphic(pos, self.head)
        
    def stopdist(self):
        return 0.5*self.mass*(self.max_speed**2) / self.max_force
            
    def step(self, dt):    
        # Find target force
        target = self.target(self)
        
        if not target:
            self.map.remove(self)
            return
        
        targetv = self.max_speed * (target - self.pos).norm()
        
        # Find collision avoiding forces
        sdsq = self.stopdist()**2
        
        for c in self.map.vehicles:
            if c == self:
                continue
        
            cdiff = c.pos - self.pos
            
            if cdiff.lensq() < sdsq and abs(angle(cdiff, self.head)) < 0.1:
                targetv *= cdiff.len() / math.sqrt(sdsq)
        
        # Find total driving force
        force = self.mass/dt * (targetv-self.vel)
        
        # Simulate actual driving
        if force.lensq() > self.max_force**2:
            force = self.max_force*force.norm()
            
        vel = self.vel + (dt/self.mass)*force
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


