import random
from soldier import SoldierAgent
from vector import Vector
from bomb import Bomb
from agent import Agent

class BomberAgent(SoldierAgent):
    def __init__(self, loc):
        self.shootTimer = 0
        self.wanderVector = Vector(random.randint(-3, 3), random.randint(-3, 3))
        Agent.__init__(self, 8, loc)
        
    def ai(self, level, player):
        if not random.randint(0, 300):
            Bomb(self.getLoc())
        
        SoldierAgent.ai(self, level, player)