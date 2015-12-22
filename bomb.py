import pygame, math, image, geom
from entity import Entity

class Bomb(Entity):
    def __init__(self, pos):
        self.timer = 10000
        Entity.__init__(self, Entity.BOMB, xyr=(pos[0], pos[1], 15))
        
    def tick(self, level, delta):
        self.timer -= delta
                  
        for bId in Entity.bulletIds:
            b = Entity.entities[bId]
            if self.collideEntity(b):
                b.destroy()
                self.timer = 0
                break
        
        if self.timer <= 0:
            self.destroy(level)
            
    def destroy(self, level):
        Entity.destroy(self)
        Explosion((self.getX(), self.getY()), 45, level = level, boom = True)
    
    def safeDestroy(self):
        Entity.destroy(self)
        
    def draw(self, surface):
        pygame.draw.circle(surface, pygame.Color(255,255,0), (round(self.getX()), round(self.getY())), 10)

class Explosion(Entity):
    def __init__(self, pos, size, level = None, boom = False):
        self.size = size
        self.frame = 0
        self.delay = 100
        self.count = self.delay
        Entity.__init__(self, Entity.XPL, xyr=(pos[0], pos[1], size))
        if boom:
            for bId in Entity.bombIds + Entity.bulletIds + Entity.agentIds + [0]:
                b = Entity.entities[bId]
                if self.collideEntity(b):
                    if b.type == Entity.BOMB:
                        b.destroy(level)
                    else:
                        b.destroy()
                    break
            for w in level.walls:
                if geom.circCircCollision((w[0]*30+15, w[1]*30+15, 15), self.circle):
                    level.level[w[1]][w[0]] = 0
                    level.walls.remove(w)
        
    def tick(self, delta):            
        self.count -= delta
        
        if self.count <= 0:
            self.frame += 1
            self.count = self.delay
            
        if self.frame == 7:
            self.destroy()
            
    def draw(self, surface):
        image.xpImgs[self.frame].scale((self.size*2, self.size*2)).draw(surface, round(self.getX()), round(self.getY()))
        image.xpImgs[self.frame].norm()
        