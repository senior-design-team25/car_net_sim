
from vmath import *
import math
from itertools import *
from random import random
from queue import queue
from config import global_config as config
from drivers import drivers

from PySide.QtGui import *
from PySide.QtCore import *


class CarGraphic(QGraphicsItem):
    def __init__(self, pos, head):
        super(CarGraphic, self).__init__()
        self.color = Qt.yellow
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
        painter.setBrush(self.color)
        painter.drawRect(QRectF(-Car.WIDTH/2+CarGraphic.LINE, -Car.HEIGHT/2+CarGraphic.LINE, 
                                Car.WIDTH-2*CarGraphic.LINE, Car.HEIGHT-2*CarGraphic.LINE))
        
        painter.setBrush(Qt.black)
        painter.drawRect(QRectF(-Car.WIDTH/2+CarGraphic.LINE, -Car.HEIGHT/4, 
                                Car.WIDTH-2*CarGraphic.LINE, 0.375*Car.HEIGHT))
        painter.setBrush(self.color)
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
        config.use('REMOVAL_DELAY', 1.0, self, 'removal_delay')
        config.use('LANE_CHANGE_CHANCE', 1.0, self, 'lane_change_chance')
        
        config.use('DRIVER', 'god', self, 'driver')
        
        self.target = target
        self.lane = lane
        self.pos = pos
        self.head = head
        self.vel = vel
        self.accel = vec(0,0)
        self.dead = False
        
        self.messages = queue()
        
        self.graphic = CarGraphic(pos, self.head)
        
    # Mark as dead
    def die(self):
        self.graphic.color = Qt.red
        self.dead = True
        
        time = self.map.time + self.removal_delay
        
        def dead(car):
            if car.map.time > time:
                return None
            else:
                return car.pos
                
        self.target = dead
            
        
    # Predicted distance to complete stop from current velocity
    def stopdist(self):
        s = self.vel.len()
        t = (s * self.mass)/self.max_force
        d = s*t - (self.max_force * t**2) / (2*self.mass)
        return d + Car.HEIGHT + t*self.reaction_time
        
    # Estimated radius of car
    def radius(self):
        return math.sqrt((Car.WIDTH/2)**2 + (Car.HEIGHT/2)**2)
        
    # Finds neighbors within distance of car
    def nbors(self, dist):
        return [c for c in self.map.vehicles
                if c != self and c.pos - self.pos < dist]
                
    # Finds cars that are in collision with this car
    def collisions(self):
        return [v for v in self.nbors(2*self.radius())
                if self.graphic.collidesWithItem(v.graphic)]
                
    # Get car's current time
    def time(self):
        return self.map.time
        
    # Sends a message to this car
    def send(self, message, delay=0):
        self.messages.push((self.time() + delay, message))
        
    # Obtains all pending messages
    def pending(self):
        pending = []
        
        while True:
            next = self.messages.peak()
        
            if next and next[0] < self.time():
                pending.append(self.messages.pop())
            else:
                break
                
        return pending
        
    # Obtains the most recent message
    def recent(self):
        pending = self.pending()
        
        return max(pending)[1] if pending else None
        
    # Calculate wanted driving forces        
    def drive(self, dt):
        # Find target force
        target = self.target
        t = target(self)
        
        if not t:
            self.map.remove(self)
            return vec(0,0)
        
        if t != self.pos:
            v = self.max_speed * (t - self.pos).norm()
        else:
            v = vec(0,0)
        
        # Find collision avoiding forces
        stopdist = self.stopdist()
        
        nbors = drivers[self.driver](self)
        
        fnbors = [d for d in nbors
                  if d < stopdist and
                     d * self.head > 0 and
                     projectunit(d, ~self.head) < Car.WIDTH]
                  
        if hasattr(target, 'lanes') and fnbors:
            fd = min(d*self.head for d in fnbors)
            v *= max((fd - Car.HEIGHT) / stopdist, 0)
            
            # Decide if we want to change lanes
            if random() < dt*self.lane_change_chance and \
               projectunit(t-self.pos, ~target.head) < Car.WIDTH/4:
                rnbors = [d for d in nbors
                          if d * ~target.head > 0 and
                             projectunit(d, ~target.head) < 2*target.width]
                        
                lnbors = [d for d in nbors
                          if d * ~target.head < 0 and
                             projectunit(d, ~target.head) < 2*target.width]
                      
                rd = min(d*target.head for d in rnbors) if rnbors else vec(1e309,1e309)
                ld = min(d*target.head for d in lnbors) if lnbors else vec(1e309,1e309)
                
                if rd/3 > fd and self.lane < target.lanes-1:
                        self.lane += 1
                elif ld/3 > fd and self.lane > 0:
                        self.lane -= 1
        
        # Return the total driving force
        return self.mass/dt * (v-self.vel)
            
    def step(self, dt):
        # Find the driving force
        force = self.drive(dt)
        
        # Simulate physical driving
        if force > self.max_force:
            force = self.max_force*force.norm()
           
        accel = force / self.mass
        vel = self.vel + dt*accel
        spin = angle(vel, self.head)
        
        if vel.lensq() == 0:
            head = self.head
        elif spin > self.max_spin*dt:
            head = self.head.rotate(self.max_spin*dt)
            vel = projectunit(vel, head)
        elif spin < -self.max_spin*dt:
            head = self.head.rotate(-self.max_spin*dt)
            vel = projectunit(vel, head)
        else:
            head = vel.norm()
            
        if vel > self.max_speed:
            vel = self.max_speed*vel.norm()
            accel = 0
            
        self.vel = vel
        self.accel = accel
        self.head = head
        self.pos += dt*vel
        
        # Update graphic
        self.graphic.set(self.pos, self.head)
        
        # Check for collisions
        if not self.dead:
            collisions = self.collisions()
            
            if collisions:
                self.map.collisions += 1
                self.die()
                
                for v in collisions:
                    v.die()
            
        
        
config.use('CAR_WIDTH', 1.0, Car, 'WIDTH')
config.use('CAR_HEIGHT', 2.0, Car, 'HEIGHT')


