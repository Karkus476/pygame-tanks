import random, geom
from agent import Agent
from turret import TurretAgent
from vector import Vector
from geom import velocityToAngle

SPEED = 0.1

class SoldierAgent(TurretAgent):
    wanderDist = 50
    wanderJitter = 0.1
    wanderRadius = 5
    def __init__(self, loc):
        self.shootTimer = 0
        self.wanderVector = Vector(random.randint(-3, 3), random.randint(-3, 3))
        Agent.__init__(self, 6, loc)
        
    def ai(self, level, player):
        self.randomWander()
            
        TurretAgent.ai(self, level, player)

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