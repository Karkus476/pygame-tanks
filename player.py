import math, pygame, sys, time
from pygame.locals import K_a, K_d, K_w, K_s
from tank import Tank
from entity import Entity
from moving_entity import MovingEntity

class Player(Tank):
    def __init__(self, xy):
        self.speed = 0.085
        Tank.__init__(self, Entity.PLAYER, xy)
        
    def tick(self, keys, mousePos, level, delta):
        self.cursor(mousePos)

        if keys[K_d]:
            self.velocity.x = self.speed
        elif keys[K_a]:
            self.velocity.x = -self.speed
        else:
            self.velocity.x = 0    
            
        if keys[K_w]:
            self.velocity.y = -self.speed
        elif keys[K_s]:
            self.velocity.y = self.speed
        else:
            self.velocity.y = 0
            
        Tank.tick(self,level,  delta)
        
    def cursor(self, mousePos):
        cX = mousePos[0]
        cY = mousePos[1]
        xDiff = self.getX() - cX
        yDiff = self.getY()- cY
        
        angle = math.degrees(math.atan2(yDiff, xDiff))
            
        self.setTurretAngle(angle)
    
    def destroy(self):
        time.sleep(1)
        pygame.quit()
        sys.exit()
    
    def setX(self, x):
        self.circle[0] = round(x)
        
    def setY(self, y):
        self.circle[1] = round(y)
