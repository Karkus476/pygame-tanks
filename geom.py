import math, pygame
from vector import Vector

def circCircCollision(c, c1):
    xDiffSq = (c[0] - c1[0])*(c[0] - c1[0])
    yDiffSq = (c[1] - c1[1])*(c[1] - c1[1])
    mx = c[2]*c[2] + c1[2]*c1[2]
    return mx > xDiffSq + yDiffSq

def pointAngle(p, p1):
    return math.degrees(math.atan2(p[1] - p1[1], p[0] - p1[0]))

def rectCircCollision(r, c):
    return c[0] + c[2] > r.x and c[0] - c[2] < r.x +  r.w and c[1] + c[2] > r.y and c[1] - c[2] < r.y + r.h

def EOL3(p,p1):
    a = p1[1] - p[1]
    b = p[0] - p1[0]
    c = a*p[0] + b*p[1]
    return (a,b,c)

def EOL2(x, y, angle):
    grad = math.tan(math.radians(angle))
    yint = y - grad*x
    return (grad, yint)

def EOL(x, y, xv, yv):
    return (yv/xv, y - x*(yv/xv))
    
def sideOfLine(xy, gradYint):
    result =(xy[1] - gradYint[1])/gradYint[0]
    if xy[0] > result:
        return "Right"
    return "Left"

def pointInCircle(p, c):
    return pointDistSq(p, c[:2]) < c[2]*c[2]

def angleToVelocity(angle, speed):
    velocity = Vector(0,0)
    velocity.x = math.cos(math.radians(180+angle)) * speed
    velocity.y = math.sin(math.radians(180+angle)) * speed
    return velocity
    
def velocityToAngle(v):
    angle = math.degrees(math.atan2(v.y, v.x))
    return angle

def pointDist(p, p1):
    return math.hypot(p[0] - p1[0], p[1] - p1[1])

def pointDistSq(p, p1):
    return (p[0] - p1[0])*(p[0] - p1[0]) + (p[1] - p1[1])*(p[1] - p1[1])
    
def lineRectCollision(line, rect):
    rectLines = linesFromRect(rect)
    for l in rectLines:
        collision = lineLineCollision(l, line)
        if collision[0] == True:
            break
    if collision[0] == True:
        return (True, collision[1])
    return (False, None)

        
    

def closestPoint(to, p, p1):
    d = pointDistSq(to, p)
    d1 = pointDistSq(to, p1)
    return d < d1

#TOP, LEFT, BOTTOM, RIGHT
def linesFromRect(rect):
    return (Line(rect.topright, rect.topleft),
            Line(rect.topright, rect.bottomright),
            Line(rect.bottomright, rect.bottomleft),
            Line(rect.topleft, rect.bottomleft))
    
def pointingAt(loc, at, angle, size = 1):
    xDiff = loc[0] - at[0]
    yDiff = loc[1] - at[1]
    
    a = math.degrees(math.atan2(yDiff, xDiff))
    if a < angle + size and a > angle - size:
        return True
    return False

def getRect2p(p, p1):
    if p[0] < p1[0]:
        x = p[0]
        x1 = p1[0]
    else:
        x = p1[0]
        x1 = p[0]
    if p[1] < p1[1]:
        y = p[1]
        y1 = p1[1]
    else:
        y = p1[1]
        y1 = p[1]
    return ((x,y), (x1, y1))
    
def lineLineCollision(line, line1):
        det = line.a*line1.b - line1.a*line.b
        if not det == 0:
            x = (line1.b*line.c - line.b*line1.c)/det
            y = (line.a*line1.c - line1.a*line.c)/det
        else:
            return (False, False)
        if (line.rect == None or line.rect.collidepoint(x, y)):
            if (line1.rect == None or line1.rect.collidepoint(x, y)):
                return (True, (x,y))
        return (False, (x,y))

def bulletLineRectCollision(loc, line, rect):
    w1 = rect.w/2
    h1 = rect.h/2
    u = (rect.left - w1, rect.top)
    d = (rect.left - w1, rect.bottom)
    l = (rect.left, rect.top - h1)
    r = (rect.right, rect.top - h1)
    
    if closestPoint(loc, u, d):
        coll = lineLineCollision(Line(rect.topright, rect.topleft), line)
        if coll[0]:
            return (True, True, coll[1])
    else:
        coll = lineLineCollision(Line(rect.bottomright, rect.bottomleft), line)
        if coll[0]:
            return (True, True, coll[1])

    if closestPoint(loc, r, l):
        coll = lineLineCollision(Line(rect.topright, rect.bottomright), line)
        if coll[0]:
            return (True, False, coll[1])
    else:
        coll = lineLineCollision(Line(rect.topleft, rect.bottomleft), line)
        if coll[0]:
            return (True, False, coll[1])
    return (False, None, None)

def lineCircCollision(l, circ):
    pV = Vector(l.p[0], l.p[1])
    qV = Vector(l.q[0], l.q[1])
    cV = Vector(circ[0], circ[1])
    lVect = Vector.subV(pV, qV)
    pcVect = Vector.subV(pV, cV) 
    projLength = pcVect.dot(lVect.getNorm()) 
    if projLength < 0:
        distvect = pcVect
    elif projLength > lVect.length():
        distVect = Vector.subV(qV, cV)
    else:
        projVect = Vector.mulVI(lVect.getNorm(), projLength)
        distVect = Vector.subV(projVect, pcVect)
    if distVect.lengthSq() < circ[2]*circ[2]:
        return True
    return False
        
class Line:
    def __init__(self, p0, p1, infinite = False):
        self.a = p1[1] - p0[1]
        self.b = p0[0] - p1[0]
        self.c = self.a*p0[0] + self.b*p0[1]
        self.p = p0
        self.q = p1
        if not infinite:
            w = abs(p0[0]- p1[0])
            h = abs(p0[1]- p1[1])
            if p0[0] < p1[0] and p0[1] > p0[1]:
                self.rect = pygame.Rect(p0[0] - w, p0[1] - h, w, h)
            else:
                self.rect = pygame.Rect(p0[0], p0[1], w, h)
        else:
            self.rect = None
        
        
    
    
    
    
    