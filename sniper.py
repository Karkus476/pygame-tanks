import random, math, geom
from agent import Agent
from vector import Vector
from tank import Tank
from entity import Entity

SHOOT_SPEED = 100
SHOOT_TEST_DIST = 500
TURN_SPEED = 2

class SniperAgent(Agent):
    def __init__(self, loc):
        self.maxBullets = 2
        self.getRandShootTime(50, 75)
        Agent.__init__(self, 10, loc)
        
    def tick(self, player, level, delta):
        if self.turningTo > TURN_SPEED or self.turningTo < -TURN_SPEED:
            self.turning = True
            if self.turningTo > 0:
                self.setTurretAngle(self.turretAngle - TURN_SPEED)
                self.turningTo -= TURN_SPEED
            else:
                self.setTurretAngle(self.turretAngle + TURN_SPEED)
                self.turningTo += TURN_SPEED
        else:
            if self.turningTo > 0:
                self.setTurretAngle(self.turretAngle - self.turningTo)
                self.turningTo = 0
            else:
                self.setTurretAngle(self.turretAngle + self.turningTo)
                self.turningTo = 0
            self.turning = False
        
        self.ai(level, player)
        Tank.tick(self,level, delta)
        
    def ai(self,level, player):
        if not random.randint(0, 15):
            for bId in Entity.bulletIds:
                b = Entity.entities[bId]
                if b.ownerId != self.ID and geom.circCircCollision(b.circle, (self.getX(), self.getY(), 100)) and self.onCollisionPath(b):
                    bangle = math.degrees(math.atan2(self.getY()- b.getY(), self.getX()- b.getX()))
                    self.setTurretAngle(bangle)
                    self.shoot(3)
                    break
        if not self.turning:
            if not random.randint(0, 3):
                playerAngle = math.degrees(math.atan2(self.getY()- player.getY(), self.getX()- player.getX()))
                self.turnTo(round(playerAngle))
            else:
                self.turnBy(random.randint(-60, 60))
            
        if self.shootTimer == 0:
            if self.bulletsFired < self.maxBullets - 1 and self.safeToShoot(level, player, 130, bounces = 2):
                self.shoot(3)
                self.getRandShootTime(20, 50)
                return
            self.getRandShootTime(1, 2)
        else:
            self.shootTimer -= 1
        