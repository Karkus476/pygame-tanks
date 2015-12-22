import math, pygame, geom
from moving_entity import MovingEntity
from vector import Vector
from image import Image
from entity import Entity
from bomb import Explosion
from geom import velocityToAngle

bulletImage = pygame.image.load("Resources/Textures/bullet.png")

class Bullet(MovingEntity):
    def __init__(self,type, loc, ownerId, fireAngle = None, velocity = None):
        self.prevSquare = (-1, -1)
        self.bType = type
        if type == 0:
            self.bounces = 1
            speed = 0.15
        elif type == 1:
            self.bounces = 0
            speed = 0.27
        elif type == 2:
            self.bounces = 1
            speed = 0.27
        elif type == 3:
            self.bounces = 2
            speed = 0.27
        self.ownerId = ownerId
        Entity.entities[ownerId].bulletsFired += 1
        self.image = Image(bulletImage)
        if fireAngle:
            self.image.rotate(-fireAngle)
            MovingEntity.__init__(self,geom.angleToVelocity(fireAngle, speed), 1, xyr = (loc[0], loc[1], 3))
        elif velocity:
            angle = geom.velocityToAngle(velocity)
            self.image.rotate(angle)
            MovingEntity.__init__(self,velocity, 1, xyr = (loc[0], loc[1], 3))
    
    def draw(self, surface):
        self.image.draw(surface, round(self.getX()), round(self.getY()))
        
    def tick(self, level, delta):
        self.check(level, delta)
        MovingEntity.tick(self, delta)
    
    def destroy(self):
        Explosion((self.getX(), self.getY()), 6)
        if Entity.entities[self.ownerId]:
            Entity.entities[self.ownerId].bulletsFired -= 1
        Entity.destroy(self)
        
    def remove(self):
        if Entity.entities[self.ownerId]:
            Entity.entities[self.ownerId].bulletsFired -= 1
        Entity.destroy(self)
        
    def check(self, l, delta):
        pos = self.getNextFrame(delta)
        collCirc = (pos[0], pos[1], self.getR())
        for bId in Entity.bulletIds + [0] + Entity.agentIds:
            b = Entity.entities[bId]
            if not b == self and not b == None:
                if b.collideEntity(self):
                    b.destroy()
                    self.destroy()
        
        sq = (math.floor(pos[0]/30), math.floor(pos[1]/30))
        squareType = l.level[int(sq[1])][int(sq[0])]            

        if squareType == 1 or squareType == 2:
            if self.bounces > 0:
                if abs(sq[0] - self.prevSquare[0]) > 0:
                    self.velocity.x *= -1
                elif abs(sq[1] - self.prevSquare[1]) > 0:
                    self.velocity.y *= -1
                self.image = Image(bulletImage)
                self.image.rotate(geom.velocityToAngle(self.velocity))
                self.bounces -= 1
            else:
                self.destroy()
        
        self.prevSquare = sq
