
from vmath import *


# Approximation of a human by deriving position
def human(car):
    nbors = [(c.pos - car.pos, c.vel - car.vel, c.accel - car.accel, car.time()) 
             for c in car.nbors(car.stopdist())]
    car.send(nbors, car.reaction_time)
    
    recent = car.recent()
    if recent:
        return [d + (car.time()-t)*v + ((car.time()-t)**2) * a/2 for d,v,a,t in recent]
    else:
        return []

# Only understands the concept of position
def bad(car):
    nbors = [c.pos - car.pos for c in car.nbors(car.stopdist())]
    car.send(nbors, car.reaction_time)
        
    return car.recent() or []
    
# All knowing
def god(car):
    return [c.pos - car.pos for c in car.nbors(car.stopdist())]
    
drivers = {
    'human': human,
    'bad': bad,
    'god': god,
}
    