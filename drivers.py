
from vmath import *

# Only understands the concept of position
def bad(car):
    nbors = [c.pos - car.pos for c in car.nbors(car.stopdist())]
    car.send(nbors, car.reaction_time)
        
    return car.recent() or []
    
# All knowing
def god(car):
    return [c.pos - car.pos for c in car.nbors(car.stopdist())]
    
drivers = {
    'bad': bad,
    'god': god,
}
    