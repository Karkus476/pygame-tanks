import math, random, geom
from agent import Agent
from entity import Entity

class SentryAgent(Agent):
    def __init__(self, loc):
        self.maxBullets = 7
        self.getRandShootTime(20, 30)
        Agent.__init__(self, 12, loc)
        
    def ai(self,level,  player):
        if not random.randint(0, 7):
            for bId in Entity.bulletIds:
                b = Entity.entities[bId]
                if b.ownerId != self.ID and geom.circCircCollision(b.circle, (self.getX(), self.getY(), 100)) and self.onCollisionPath(b):
                    bangle = math.degrees(math.atan2(self.getY()- b.getY(), self.getX()- b.getX()))
                    self.setTurretAngle(bangle)
                    self.shoot(1)
                    break
        
        self.setTurretAngle(math.degrees(math.atan2(self.getY() - player.getY(), self.getX() - player.getX())))

        if self.shootTimer == 0:
            if self.bulletsFired < self.maxBullets - 1 and self.safeToShoot(level, player, 130, bounces = 2):
                self.shoot(1)
                self.getRandShootTime(20, 30)
                return
            self.getRandShootTime(1, 2)
        else:
            self.shootTimer -= 1