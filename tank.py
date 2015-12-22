import pygame, math, geom
from moving_entity import MovingEntity
from vector import Vector
from entity import Entity
from image import Image
from bullet import Bullet
from bomb import Explosion
from track import Track

class Tank(MovingEntity):
    def __init__(self, type, xy):
        self.trackCounter = 100
        if type == Entity.PLAYER:
            self.maxBullets = 5
        elif type == Entity.TURRET:
            self.maxBullets = 3
        elif type == Entity.SOLDIER:
            self.maxBullets = 2
        elif type == Entity.BOMBER:
            self.maxBullets = 1
        self.bulletsFired = 0
        self.turretAngle = 0
        self.bodyAngle = 0
        colour = Entity.typeToColour(type)
        MovingEntity.__init__(self, Vector(0,0), type, xyr=(xy[0], xy[1], 16))
        self.oBodyImage, self.oTurretImage = Image.getTankImage(colour)
        self.bodyImage = Image(self.oBodyImage)
        self.turretImage = Image(self.oTurretImage)
        
    def destroy(self):
        Explosion(self.getLoc(), 30)
        MovingEntity.destroy(self)
        
    def shoot(self, bulletType = 0):
        if self.bulletsFired < self.maxBullets:
            loc = (self.getX()+math.cos(math.radians(180+self.turretAngle))*20, self.getY()+math.sin(math.radians(180+self.turretAngle))*20)
            Bullet(bulletType,loc, self.ID, fireAngle=self.turretAngle)
            
    def tick(self, level, delta):
        x, y = MovingEntity.getNextFrame(self, delta)
        collision = self.checkCollision(x, y, 15, level)
        MovingEntity.tick(self, delta, cx=collision, cy=collision)
        
    def setBodyAngle(self, angle):
        self.bodyImage = Image(self.oBodyImage)
        self.bodyImage.rotate(-angle)
        self.bodyAngle = angle

    def setTurretAngle(self, angle):
        self.turretImage = Image(self.oTurretImage)
        self.turretImage.rotate(-angle)
        self.turretAngle = angle
    
    def draw(self, ts, surface, delta):
        if self.trackCounter <= 0:
            self.drawTracks(surface)
            self.trackCounter = 100
        self.trackCounter -= delta
        a = geom.velocityToAngle(self.velocity)
        self.setBodyAngle(a)
        self.bodyImage.draw(surface, round(self.getX()), round(self.getY()))
        self.turretImage.draw(surface, round(self.getX()), round(self.getY()))
        
    def drawTracks(self, surface):
        l = self.getLocVect()
        v = Vector(self.velocity.x, self.velocity.y)
        v.setLength(7)
        a = Vector(-v.y, v.x)
        b = Vector(v.y, -v.x)
        a.add(l)
        b.add(l)
        Track(surface, (a.x, a.y))
        Track(surface, (b.x, b.y))
        
        
        
    