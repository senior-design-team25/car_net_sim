
from vmath import *

CAR_WIDTH = 1
CAR_HEIGHT = 2
LINE_WIDTH = 1 / 8.0

CAR_MASS = 100
CAR_MAX_FORCE = 10
CAR_MAX_SPIN = 20
CAR_MAX_SPEED = 10

# Representation of a car

class Car:
    def __init__(self, world, pos, rot, vel):
        self.pos = pos
        self.rot = rot
        self.vel = vel
        
        self.obj = world.createobj(pos, rot,
            [(vec(0,-LINE_WIDTH), vec(0,CAR_HEIGHT+LINE_WIDTH), CAR_WIDTH + 2*LINE_WIDTH, {'fill':'black'}),
             (vec(0,0), vec(0,CAR_HEIGHT), CAR_WIDTH, {'fill':'yellow'}),
             (vec(-0.5*CAR_WIDTH-LINE_WIDTH,0.25*CAR_HEIGHT), vec(0.5*CAR_WIDTH+LINE_WIDTH,0.25*CAR_HEIGHT), LINE_WIDTH, {'fill':'black'}),
             (vec(-0.5*CAR_WIDTH-LINE_WIDTH,0.625*CAR_HEIGHT), vec(0.5*CAR_WIDTH+LINE_WIDTH,0.625*CAR_HEIGHT), LINE_WIDTH, {'fill':'black'})])
            
    def step(self, world, dt):
        dir = vec(0,0) - self.pos
        force = CAR_MASS/dt * (dir-self.vel)
        
        print self.pos
        
        if force.lensq() > CAR_MAX_FORCE**2:
            force = CAR_MAX_FORCE*force.norm()
            
        vel = self.vel + (dt/CAR_MASS)*force
        
        spin = angle(vel, self.vel)
        
        if spin > dt*CAR_MAX_SPIN:
            vel = project(vel, self.vel.rotate(dt*CAR_MAX_SPIN))
        elif spin < -dt*CAR_MAX_SPIN:
            vel = project(vel, self.vel.rotate(-dt*CAR_MAX_SPIN))
            
        if vel.lensq() > CAR_MAX_SPEED**2:
            vel = CAR_MAX_SPEED*vel.norm()
            
        self.vel = vel
        self.pos += dt*vel
        
        world.moveobj(self.obj, self.pos, angle(self.vel, vec(0,1)))

