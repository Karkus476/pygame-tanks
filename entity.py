import pygame, math, geom
from vector import Vector

mp = [0,0]

class Entity:
    entities = []
    bulletIds = []
    bombIds = []
    agentIds = []
    trackIds = []
    nextId = 0
    def __init__(self, type, xywh = None, xyr = None):
        if xywh != None:
            self.rect = pygame.Rect(xywh[0],xywh[1],xywh[2],xywh[3])
            self.isRect = True
        elif xyr != None:
            self.circle = [xyr[0], xyr[1], xyr[2]]
            self.isRect = False
        else:
            print("No location specified for entity")
        self.type = type
            
        self.ID = Entity.nextId
        Entity.nextId += 1
        
        Entity.addEntity(self)
        
    @staticmethod
    def tickAll(keys, mousePos, player, level, delta):
        global mp
        mp = mousePos
        for e in Entity.entities:
            if e == None:
                continue
            if e.type == Entity.PLAYER:
                e.tick(keys, mousePos,level, delta)
            elif e.type == Entity.BULLET or e.type == Entity.BOMB:
                e.tick(level,delta)
            elif e.type == Entity.XPL:
                e.tick(delta)
            elif e.type >= 5:
                e.tick(player, level, delta)
    @staticmethod
    def drawAll(ts, surface, delta):
        Entity.drawBombs(surface)
        for e in Entity.entities:
            if e == None or e.type == Entity.BOMB or e.type == Entity.TRACK:
                continue
            if e.type == 0 or e.type >= 5:
                e.draw(ts, surface, delta)
                continue
            e.draw(surface)
    @staticmethod
    def drawBombs(surface):
        for bId in Entity.bombIds:
            b = Entity.entities[bId]
            b.draw(surface)
            
    @staticmethod
    def drawTracks(surface):
        for tId in Entity.trackIds:
            t = Entity.entities[tId]
            t.draw(surface)
            
    def tick(self, delta):
        pass
    def draw(self, surface):
        pass
    def destroy(self):
        Entity.removeEntity(self) 
             
    def collideEntity(self, e):
        if self.isRect != e.isRect:
            if self.isRect:
                return geom.rectCircCollision(self.rect, e.circle)
            return geom.rectCircCollision(e.rect, self.circle)
        elif self.isRect:
            return self.rect.colliderect(e.rect)
        return geom.circCircCollision(self.circle, e.circle)
            
    @staticmethod
    def addEntity(e):
        if e.type == Entity.BULLET:
            Entity.bulletIds.append(e.ID)
        elif e.type == Entity.BOMB:
            Entity.bombIds.append(e.ID)
        elif e.type == Entity.TRACK:
            Entity.trackIds.append(e.ID)
        elif e.type >= 5:
            Entity.agentIds.append(e.ID)
        Entity.entities.append(e)
            
    @staticmethod
    def removeEntity(e):
        try:
            if e.type == Entity.BULLET:
                Entity.bulletIds.remove(e.ID)
            elif e.type == Entity.BOMB:
                Entity.bombIds.remove(e.ID)
            elif e.type == Entity.TRACK:
                Entity.trackIds.remove(e.ID)
            elif e.type >= 5:
                Entity.agentIds.remove(e.ID)
        except ValueError:
            pass
        Entity.entities[e.ID] = None
    
    def getW(self):
        if self.isRect:
            return self.rect.w
        else:
            return None
    def getH(self):
        if self.isRect:
            return self.rect.h
        else:
            return None
    def setW(self, w):
        if self.isRect:
            self.rect.w = w
    def setH(self, h):
        if self.isRect:
            self.rect.h = h
    def getR(self):
        if self.isRect:
            return None
        else:
            return self.circle[2]
    def setR(self, r):
        if not self.isRect:
            self.circle[2] = r
    def getX(self):
        if self.isRect:
            return self.rect.x
        else:
            return self.circle[0]
    def getY(self):
        if self.isRect:
            return self.rect.y
        else:
            return self.circle[1]
    def setX(self, x):
        if self.isRect:
            self.rect.x = x
        else:
            self.circle[0] = x
    def setY(self, y):
        if self.isRect:
            self.rect.y = y
        else:
            self.circle[1] = y
    def getLoc(self):
        return (self.getX(), self.getY())
    def getLocVect(self):
        return Vector(self.getX(), self.getY())
    def getSquare(self):
        loc = self.getLoc()
        return (math.floor(loc[0]/30), math.floor(loc[1]/30))
    
    @staticmethod
    def clear(l):
        for e in Entity.entities:
            if not e:
                continue
            if e.type == 1 or e.type == 2:
                e.destroy()
            elif e.type == 3:
                e.safeDestroy()
    
    @staticmethod
    def typeToColour(type):
        if type == 0:
            return "Blue"
        elif type == 5:
            return "Brown"
        elif type == 6:
            return "Grey"
        elif type == 7:
            return "Teal"
        elif type == 8:
            return "Yellow"
        elif type == 9:
            return "Red"
        elif type == 10:
            return "Green"
        elif type == 12:
            return "Red"
    
    PLAYER = 0
    BULLET = 1
    TRACK = 2
    BOMB = 3
    XPL = 4
    
    TURRET = 5
    SOLDIER = 6
    HUNTER = 7
    BOMBER = 8
    ROVER = 9#Slightly lighter than player 2
    SNIPER = 10
    WARRIOR = 11
    SENTRY = 12
    SCOUT = 13
    SPY = 14
    ASSASIN = 15
    ELITE = 16
    SPAWNER = 17 #Slightly lighter than player 1 
    TACTICIAN = 18
    GENERAL = 19
    DESTROYER = 20  
    
