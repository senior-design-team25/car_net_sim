
import random
import math

# Definition of a simple gaussian type
                 
class gaussian(tuple):
    def __new__(cls, mu, sigma):
        return tuple.__new__(cls, (mu, sigma))
        
    @property
    def mu(self): return self[0]
    
    @property
    def sigma(self): return self[1]
        
    def __repr__(self):
        return 'gaussian(%r, %r)' % self
        
    
    # Simple math operations
    def __abs__((mu, sigma)):
        return gaussian(abs(mu), sigma)
        
    def __pos__(g):
        return g
        
    def __neg__((mu,sigma)):
        return gaussian(-mu, sigma)
        
    def __float__((mu,sigma)):
        return random.gauss(mu, sigma)
        
    def __int__(g):
        return int(float(g))
        
    def __long__(g):
        return long(float(g))
        
    def __round__(g, n):
        return round(float(g), n)
        
    def __floor__(g):
        return math.floor(float(g))
        
    def __ceil__(g):
        return math.ceil(float(g))
        
    def __trunc__(g):
        return math.trunc(float(g))
        
        
    def __add__((mu,sigma), b):
        if isinstance(b, gaussian):
            return gaussian(mu + b.mu, math.sqrt(sigma**2 + b.sigma**2))
        else:
            return gaussian(mu + b, sigma)
    
    def __sub__((mu,sigma), b):
        if isinstance(b, gaussian):
            return gaussian(mu - b.mu, math.sqrt(sigma**2 + b.sigma**2))
        else:
            return gaussian(mu - b, sigma)
            
    def __mul__((mu,sigma), b):
        return gaussian(b*mu, abs(b)*sigma)

    def __div__((mu,sigma), b):
        return gaussian(mu/b, sigma/abs(b))
        
    def __rdiv__((mu,sigma), b):
        return gaussian(b/mu, abs(b)/sigma)
        
        
    # Aliases
    __truediv__ = __div__
    __rtruediv__ = __rdiv__
    
    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    