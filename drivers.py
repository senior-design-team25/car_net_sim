
from vmath import *

# Approximation of a human by deriving position        
def human(car):
    nbors = [(c.pos - car.pos, c.vel - car.vel, car.time()) 
             for c in car.nbors(car.stopdist())]
    car.send(nbors, car.reaction_time)
    recent = car.recent()
    
    if recent:
        return [d + (car.time()-t)*v for d,v,t in recent]
    else:
        return []
        
# Network only vehicles
def network(car):
    for c in car.nbors(car.range):
        c.send(car.pos - c.pos, car.latency)
    
    return [d for _,d in car.pending()]
        
# Human driver augmented by braking updates
def connected(car):
    for c in car.nbors(car.range):
        c.send(('n', car.pos - c.pos, car.vel - c.vel, c.time()), car.latency)
        c.send(('h', car.pos - c.pos, car.vel - c.vel, c.time()), car.reaction_time)
        
    return [(d + (car.time()-t)*v) if t == 'h' else d 
            for _,(t,d,v,t) in car.pending()]

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
    'network': network,
    'connected': connected,
}
    