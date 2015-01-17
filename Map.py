
from itertools import *
from vmath import *
from Car import Car


LANE_WIDTH = 1.25
LINE_WIDTH = 1 / 8.0


# Representation of a single road

class Road:
    def __init__(self, world, start, end, lanes):
        self.start = start
        self.end = end
        self.lanes = lanes
        
        d = dist(start, end)
        a = angle(end-start, vec(0,1))
        
        world.createobj(start, a,
            [(vec(0,0), vec(0,d), LANE_WIDTH*sum(lanes) + 2*LINE_WIDTH, {'fill':'black'}),
             (vec(0,0), vec(0,d), LANE_WIDTH*sum(lanes), {'fill':'gray'}),
             (vec(0,0), vec(0,d), LINE_WIDTH, {'fill':'yellow'})] +
            [(vec(-LANE_WIDTH*i, 0), vec(-LANE_WIDTH*i, d), LINE_WIDTH, {'fill':'white', 'dash':True})
             for i in xrange(1, lanes[0])] +
            [(vec(LANE_WIDTH*i, 0), vec(LANE_WIDTH*i, d), LINE_WIDTH, {'fill':'white','dash':True})
             for i in xrange(1, lanes[1])])
        
        

# Representation of all static world elements
        
class Map:
    def __init__(self, world):
        self.roads = \
            [Road(world, vec(0, 0), vec(world.width, world.height), (2,2)),
             Road(world, vec(0, world.height), vec(world.width, 0), (2,2))]
            
        self.cars = \
            [Car(world, vec(10,10), 0, vec(0,0))]
             
    def step(self, world, dt):
        for c in self.cars:
            c.step(world, dt)