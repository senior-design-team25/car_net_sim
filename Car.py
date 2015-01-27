
from vmath import *
import math

from PySide.QtGui import *
from PySide.QtCore import *


CAR_WIDTH = 1.0
CAR_HEIGHT = 2.0
LINE_WIDTH = 0.125

CAR_MASS = 100
CAR_MAX_FORCE = 2000
CAR_MAX_SPIN = 1
CAR_MAX_SPEED = 35


class CarGraphic(QGraphicsItem):
    def __init__(self, pos, head):
        super(CarGraphic, self).__init__()
        self.set(pos, head)
        
    def set(self, (x,y), head):
        self.setPos(x, y)
        self.setRotation(math.degrees(angle(head, vec(0,1))))

    def boundingRect(self):
        return QRectF(-CAR_WIDTH/2, -CAR_HEIGHT/2, CAR_WIDTH, CAR_HEIGHT)
     
    def paint(self, painter, option, widget):
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.black)
        painter.drawRect(QRectF(-CAR_WIDTH/2, -CAR_HEIGHT/2, CAR_WIDTH, CAR_HEIGHT))
        painter.setBrush(Qt.yellow)
        painter.drawRect(QRectF(-CAR_WIDTH/2+LINE_WIDTH, -CAR_HEIGHT/2+LINE_WIDTH, 
                                CAR_WIDTH-2*LINE_WIDTH, CAR_HEIGHT-2*LINE_WIDTH))
        
        painter.setBrush(Qt.black)
        painter.drawRect(QRectF(-CAR_WIDTH/2+LINE_WIDTH, -CAR_HEIGHT/4, 
                                CAR_WIDTH-2*LINE_WIDTH, 0.375*CAR_HEIGHT))
        painter.setBrush(Qt.yellow)
        painter.drawRect(QRectF(-CAR_WIDTH/2+LINE_WIDTH, -CAR_HEIGHT/4+LINE_WIDTH, 
                                CAR_WIDTH-2*LINE_WIDTH, 0.375*CAR_HEIGHT-2*LINE_WIDTH))
        
# Representation of a car

class Car:
    def __init__(self, target, lane, pos, head=vec(0,0), vel=vec(0,0)):
        self.target = target
        self.lane = lane
        self.pos = pos
        self.head = head
        self.vel = vel
        
        self.graphic = CarGraphic(pos, self.head)
            
    def step(self, dt):
        target = self.target(self)
        
        if not target:
            self.map.remove(self)
            return
        
        dir = target - self.pos # TODO use "driver" input to determine steering    
        force = CAR_MASS/dt * (dir-self.vel)
        
        if force.lensq() > CAR_MAX_FORCE**2:
            force = CAR_MAX_FORCE*force.norm()
            
        vel = self.vel + (dt/CAR_MASS)*force
        spin = angle(vel, self.head)
        
        if vel.iszero():
            head = self.head
        elif spin > CAR_MAX_SPIN*dt:
            head = self.head.rotate(CAR_MAX_SPIN*dt)
            vel = projectunit(vel, head)
        elif spin < -CAR_MAX_SPIN*dt:
            head = self.head.rotate(-CAR_MAX_SPIN*dt)
            vel = projectunit(vel, head)
        else:
            head = vel.norm()
            
        if vel.lensq() > CAR_MAX_SPEED**2:
            vel = CAR_MAX_SPEED*vel.norm()
            
        self.vel = vel
        self.head = head
        self.pos += dt*vel
        
        self.graphic.set(self.pos, self.head)
        
