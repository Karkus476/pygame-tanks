import random, geom, math, entity
from agent import Agent

SHOOT_SPEED = 100
SHOOT_TEST_DIST = 100

class TurretAgent(Agent):
    def __init__(self, loc):
        self.shootTimer = SHOOT_SPEED
        Agent.__init__(self, 5, loc)
    
    def ai(self, level,player):
        if not self.turning:
            if random.randint(0, 3):
                playerAngle = math.degrees(math.atan2(self.getY()- player.getY(), self.getX()- player.getX()))
                self.turnTo(round(playerAngle))
            else:
                self.turnBy(random.randint(-60, 60))
            
        if self.shootTimer == 0:
            if self.bulletsFired < self.maxBullets and self.safeToShoot(level, player, 70):
                self.shoot()
                self.getRandShootTime(75, 100)
                return
            self.getRandShootTime(5, 10)
        else:
            self.shootTimer -= 1