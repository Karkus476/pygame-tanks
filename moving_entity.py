import pygame, math
from entity import Entity

class MovingEntity(Entity):
    def __init__(self, velocity, type, xywh = None, xyr = None):
        self.velocity = velocity
        Entity.__init__(self, type, xywh, xyr)
        
    def tick(self, delta,cx=False, cy=False):
        if not cx:
            self.setX(self.getX() + self.velocity.x * delta)
        if not cy:
            self.setY(self.getY() + self.velocity.y * delta)
        
    def getNextFrame(self, delta):
        return (self.getX() + self.velocity.x * delta, self.getY() + self.velocity.y * delta)
    
    def checkCollision(self, x, y, w,level):
        sqPos = (x%30, y%30)
        square = (math.floor(x/30), math.floor(y/30))
        toCheck = [square]
        if sqPos[0] < w:
            if sqPos[1] < w:
                toCheck.append((square[0] - 1, square[1]-1))
                toCheck.append((square[0], square[1] -1))
            if sqPos[1] > 30 - w:
                toCheck.append((square[0] - 1, square[1]+1))
                toCheck.append((square[0], square[1] + 1))
            toCheck.append((square[0] - 1, square[1]))
        elif sqPos[0] > 30 - w:
            if sqPos[1] < w:
                toCheck.append((square[0] + 1, square[1]-1))
                toCheck.append((square[0], square[1] -1))
            if sqPos[1] > 30 - w:
                toCheck.append((square[0] + 1, square[1]+1))
                toCheck.append((square[0], square[1] + 1))
            toCheck.append((square[0] + 1, square[1]))
        for t in toCheck:
            type= level.level[int(t[1])][int(t[0])]
            if type == 1 or type == 2 or type == 3:
                return True
        return False
