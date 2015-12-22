import math, random, geom
from agent import Agent
from soldier import SoldierAgent
from vector import Vector
from entity import Entity

SHOOT_SPEED = 100
SHOOT_TEST_DIST = 150
SPEED = 0.1

class HunterAgent(Agent):
    def __init__(self, loc):
        self.maxBullets = 1
        self.shootTimer = SHOOT_SPEED
        self.wanderVector = Vector(random.randint(-3, 3), random.randint(-3, 3))
        Agent.__init__(self, 7, loc)
        
    def ai(self, level, player):
        if not random.randint(0, 100):
            for bId in Entity.bulletIds:
                b = Entity.entities[bId]
                if b.ownerId != self.ID and geom.circCircCollision(b.circle, (self.getX(), self.getY(), 100)) and self.onCollisionPath(b):
                    bangle = math.degrees(math.atan2(self.getY()- b.getY(), self.getX()- b.getX()))
                    self.setTurretAngle(bangle)
                    self.shoot(1)
                    break
        
        self.randomWander()
        
        playerAngle = math.degrees(math.atan2(self.getY()- player.getY(), self.getX()- player.getX()))
        self.turnTo(playerAngle)
        
        if self.shootTimer == 0:
            if self.bulletsFired < self.maxBullets and self.safeToShoot(level, player, 50, bounces = 0):
                self.shoot(1)
                self.getRandShootTime(100, 150)
                return 
            self.getRandShootTime(4, 7)
        else:
            self.shootTimer -= 1

    def randomWander(self):
        if self.velocity.length() == 0:
            velocity = Vector(0.1,0.1)
        
        final = self.velocity.getNorm()
        final.mul(Vector(SoldierAgent.wanderDist, SoldierAgent.wanderDist))
          
        self.wanderVector.add(Vector(random.randint(-3, 3), random.randint(-3, 3)))
        self.wanderVector.norm()
        self.wanderVector.mul(Vector(SoldierAgent.wanderRadius, SoldierAgent.wanderRadius))
          
        self.velocity.add(final)
        self.velocity.add(self.wanderVector)
        self.velocity.trunc(SPEED)
