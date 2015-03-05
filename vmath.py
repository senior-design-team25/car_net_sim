
import math


# Epsilon for nearby comparisons
EPS = 0.0001                     
                       
                 
# Definition of a simple vector type
                 
class vec(tuple):
    # Definition as extention of tuple to reduce memory
    # thrashing, also lets us to upacking directly.
    def __new__(cls, x, y):
        return tuple.__new__(cls, (x, y))
        
    @property
    def x(self): return self[0]
    
    @property
    def y(self): return self[1]
        
    def __repr__(self):
        return 'vec(%r, %r)' % self
        
    
    # Simple math operations
    def __abs__((x,y)):
        return vec(abs(x), abs(y))
        
    def __pos__(v):
        return v
        
    def __neg__((ax,ay)):
        return vec(-ax, -ay)
    
    def __invert__((ax,ay)):
        return vec(-ay, ax)
        
    def __round__((ax,ay), n):
        return vec(round(ax, n), round(ay, n))
        
    def __floor__((ax,ay)):
        return vec(math.floor(ax), math.floor(ay))
        
    def __ceil__((ax,ay)):
        return vec(math.ceil(ax), math.ceil(ay))
        
    def __trunc__((ax,ay)):
        return vec(math.trunc(ax), math.trun(ay))
        
        
    def __add__((ax,ay), b):
        if isinstance(b, vec):
            return vec(ax+b[0], ay+b[1])
        else:
            return vec(ax+b, ay+b)
    
    def __sub__((ax,ay), b):
        if isinstance(b, vec):
            return vec(ax-b[0], ay-b[1])
        else:
            return vec(ax-b, ay-b)
            
    def __mul__(a, b):
        if isinstance(b, vec):
            return a.dot(b)
        else:
            return a.scale(b)

    def __truediv__((ax,ay), b):
        return vec(ax/b, ay/b)
        
    def __floordiv__((ax,ay), b):
        return vec(ax//b, ay//b)
        
    def __mod__((ax,ay), b):
        return vec(ax%b, ay%b)
        
    def __divmod__((ax,ay), b):
        return vec(divmod(ax,b), divmod(ay,b))
        
    def __pow__((ax,ay), b):
        return vec(ax**b, ay**b)
        
        
    # Relationships
    def __lt__(a, b):
        if isinstance(b, vec):
            return a.lensq() < b.lensq()
        else:
            return a.lensq() < b**2
            
    def __gt__(a, b):
        if isinstance(b, vec):
            return a.lensq() > b.lensq()
        else:
            return a.lensq() > b**2
            
    def __le__(a, b):
        return not a > b
        
    def __ge__(a, b):
        return not a < b
        
        
    # Aliases
    __div__ = __truediv__
    
    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    
        

    # Vector properties
    def dot((ax,ay), (bx,by)):
        return ax*bx + ay*by

    def scale((x,y), s):
        return vec(s*x, s*y)
    
    def lensq((x,y)):
        return x*x + y*y
    
    def len(v):
        return math.sqrt(v.lensq())
        
    def iszero(v):
        return abs(v.lensq()) < EPS
        
    def norm(v):
        return v / v.len()
        
    def rotate((x,y), a):
        cos = math.cos(a)
        sin = math.sin(a)
        return vec(cos*x - sin*y, sin*x + cos*y)
        
        

# Vector operations
def distsq(a, b):
    return (b-a).lensq()

def dist(a, b):
    return (b-a).len()
    
def isnear(a, b):
    return (b-a).iszero()
    
def angle(a, b):
    return -math.atan2(~a * b, a * b)
    
def projectunit(a, b):
    return (a*b)*b
    
def project(a, b):
    return b.scale(a*b / b.lensq())
    
def lerp(a, b, r):
    return a.scale(1-r) + a.scale(r)
    
def bezier(a, b, c, d, r):
    m = lerp(b, c, r)
    
    return lerp(lerp(lerp(a,b,r), m, r),
                lerp(m, lerp(c,d,r), r), r)
    
def hermite(a, b, c, d, t):
    return (a.scale(2*t**3 - 3*t**2 + 1) +
            b.scale(t**3 - 2*t**2 + t) +
            c.scale(-2*t**3 + 3*t**2) +
            d.scale(t**3 - t**2))
        
    

