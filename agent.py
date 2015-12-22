import random, geom, pygame, math
from tank import Tank
from vector import Vector
from entity import Entity

class Agent(Tank):
    def __init__(self, type, loc):
        self.turningTo = 0
        Tank.__init__(self, type, loc)
        
    def tick(self, player, level, delta):
        if self.turningTo != 0:
            self.turning = True
            if self.turningTo > 0:
                self.setTurretAngle(self.turretAngle - 1)
                self.turningTo -= 1
            else:
                self.setTurretAngle(self.turretAngle + 1)
                self.turningTo += 1
        else:
            self.turning = False
        
        self.ai(level, player)
        Tank.tick(self,level, delta)
        
    def safeToShoot(self, level, player, iterations,v = None, bounces = 1, xy = None):
        if v == None:
            v = geom.angleToVelocity(self.turretAngle, 1)
        if xy == None:
            x = self.getX()
            y = self.getY()
        else:
            x = xy[0]
            y = xy[1]
        prevSquare = self.getSquare()
        counts = 0
        while counts <= iterations:
            counts += 1
            x += v.x * 10
            y += v.y * 10
            squareType = level.level[int(math.floor(y/30))][int(math.floor(x/30))]
            if squareType == 1 or squareType == 2:
                if bounces < 1:
                    return False
                bounces -= 1
                sq = (math.floor(x/30), math.floor(y/30))
                if abs(sq[0] - prevSquare[0]) > 0:
                    return self.safeToShoot(level, player, counts, Vector(v.x*-1, v.y), bounces, (x,y))
                elif abs(sq[1] - prevSquare[1]) > 0:
                    return self.safeToShoot(level, player, counts, Vector(v.x, v.y*-1), bounces, (x,y))
            prevSquare = (math.floor(x/30),math.floor(y/30))
            for aId in Entity.agentIds:
                a = Entity.entities[aId]
                if a != self and geom.pointInCircle((x, y), a.circle):
                    return False
            if geom.pointInCircle((x,y), player.circle):
                return True
        return None
    
    def safeToShoot2(self, level, player, bounces = 1):
        safe = False
        for l in self.getLines(level, bounces):
            for aId in Entity.agentIds:
                a = Entity.entities[aId]
                if geom.lineCircCollision(l, a.circle):
                    return False
            if geom.lineCircCollision(l, player.circle):
                    safe = True
        return safe 

    def getLines(self, level, bounces, v = None, xy = None):
        lines = []
        colls = []
        found = False
        if not v:
            v = geom.angleToVelocity(self.turretAngle, 1350)
        if not xy:
            xy = self.getLoc()
        line =  geom.Line(self.getLoc(), (self.getX()+v.x, self.getY()+v.y))
        for w in level.innerWalls:
            wRect = pygame.Rect(w[0]*30, w[1]*30, 30, 30)
            bounce = geom.bulletLineRectCollision(self.getLoc(), line, wRect)
            if bounce[0]:
                found = True
                colls.append((bounce[2], bounce[1]))

        if not found:
            k = 0
            for l in level.outerWalls:
                coll = geom.lineLineCollision(l, line)
                if coll[0]:
                    if k < 2:
                        colls.append((coll[1], True))
                    else:
                        colls.append((coll[1], False))
                k += 1
                    
        dists = []
        for c in colls:
            dists.append(geom.pointDistSq(xy, c))
            
        near = min(dists)
        if bounces < 0:
            lines = self.getLines(level, bounces - 1, v, xy)
        lines.append(geom.Line(xy, near))
        return lines
    
    def getRandShootTime(self, min, max):
        self.shootTimer = random.randint(min, max)
    
    def turnBy(self, angle):
        self.turningTo = angle
        
    def turnTo(self, angle):
        self.turnBy(self.turretAngle - angle)
        
    def onCollisionPath(self, b):
        sVect = Vector(self.getX(), self.getY())
        bVect = Vector(b.getX(), b.getY())
        distVect = Vector.subV(sVect, bVect)
        v = Vector(b.velocity.x, b.velocity.y)
        v.setLength(distVect.length())
        v.add(bVect)
        distVect2 = Vector.subV(v, sVect)
        if distVect2.length() < 16:
            return True
        return False
                
