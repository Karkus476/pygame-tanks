import random, math, geom
from agent import Agent
from entity import Entity
from vector import Vector

SPEED = 0.1

class RoverAgent(Agent):
    def __init__(self, loc):
        self.maxBullets = 3
        self.getRandShootTime(20, 30)
        self.path = None
        self.pvIndex = None
        self.pIndex = 0
        self.restartPath = True
        self.targetLoc = None
        Agent.__init__(self, 9, loc)
        
    def ai(self, level, player):
        if not random.randint(0, 15):
            for bId in Entity.bulletIds:
                b = Entity.entities[bId]
                if b.ownerId != self.ID and geom.circCircCollision(b.circle, (self.getX(), self.getY(), 60)) and self.onCollisionPath(b):
                    bangle = math.degrees(math.atan2(self.getY()- b.getY(), self.getX()- b.getX()))
                    self.setTurretAngle(bangle)
                    self.shoot(3)
                    
        if self.targetLoc == None:
            if self.restartPath:
                self.targetLoc = level.p.getClosestNode(self.getLoc())
                self.setX(self.targetLoc.x)
                self.setY(self.targetLoc.y)
                self.restartPath = False
                self.path = None
            if self.path != None and self.pIndex >= len(self.path)-1:
                self.path = None
            if self.path == None:
                self.path = level.p.findPath(level.pv[self.pvIndex], player.getClosestNode(player.getLoc()))
                self.pIndex = 0
            self.targetLoc = self.path[self.pIndex]
            self.pIndex += 1
                
        else:
            #self.targetLoc.printV()
            loc = self.getLocVect()
            v = Vector.subV(self.targetLoc, loc)
            if v.lengthSq() < 1:
                self.setX(self.targetLoc.x)
                self.setY(self.targetLoc.y)
                self.targetLoc = None
            v.trunc(SPEED)
            self.velocity = v
    
