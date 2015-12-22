import math

class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def zero(self):
        self.x = 0
        self.y = 0

    def isZero(self):
        return self.x == self.y == 0

    def length(self):
        return math.hypot(self.x, self.y)

    def lengthSq(self):
        return self.x*self.x + self.y*self.y

    def norm(self):
        l = self.length()
        if not l == 0:
            self.x /= l
            self.y /= l
            
    def getNorm(self):
        a = self
        l = a.length()
        if not l == 0:
            a.x /= l
            a.y /= l
        return a
    
    def perp(self):
        return Vector(-self.y,self.x)

    def dot(self, v):
        return self.x * v.x + self.y * v.y

    def trunc(self, max):
        if self.length() > max:
            self.norm()

            self.x *= max
            self.y *= max
            
    def setLength(self, length):
        self.norm()

        self.x *= length
        self.y *= length

    def add(self, v):
        self.x += v.x
        self.y += v.y
    
    @staticmethod
    def addV(v, v2):
        return Vector(v.x + v2.x, v.y + v2.y)

    def sub(self, v):
        self.x -= v.x
        self.y -= v.y
        
    @staticmethod
    def subV(v, v2):
        return Vector(v.x - v2.x, v.y - v2.y)

    def mul(self, v):
        self.x *= v.x
        self.y *= v.y
    
    @staticmethod
    def mulVI(v, i):
        return Vector(v.x*i, v.y*i)
            
    def div(self, v):
        self.x /= v.x
        self.y /= v.y
        
    def divI(self, i):
        self.x /= i
        self.y /= i
        
    def reverse(self):
        self.x *= -1
        self.y *= -1

    def printV(self):
        print((self.x, self.y))
