import pygame, random, geom
from path import Path
from path import squareToTank
from soldier import SoldierAgent
from turret import TurretAgent
from hunter import HunterAgent
from bomber import BomberAgent
from sniper import SniperAgent
from sentry import SentryAgent
from rover import RoverAgent

NULL = 0
WALL = 1
BLOCK = 2
HOLE = 3

wallColour = pygame.Color(130, 61, 30)
blockColour = pygame.Color(91, 36, 0)

class Level:
    pv = [squareToTank((4, 4)), squareToTank((4, 10)), squareToTank((4, 16)), squareToTank((9, 16)),
        squareToTank((9, 9)), squareToTank((9, 4)), squareToTank((18, 4)), squareToTank((26, 4)),
        squareToTank((18, 16)), squareToTank((26, 16)), squareToTank((21, 10))]
    ev = [(pv[0], pv[1], None), (pv[1], pv[2], None), (pv[2], pv[3], None), (pv[3], pv[4], None),
        (pv[4], pv[5], None), (pv[5], pv[6], None), (pv[6], pv[7], None), (pv[6], pv[8], None), 
        (pv[6], pv[10], None), (pv[7], pv[9], None), (pv[8], pv[10], None)]
    p = Path(pv, ev)
    def __init__(self, surface):
        self.walls = []
        self.blocks = []
        self.holes = []
        image = surface
        self.level = []
        self.spawnPoints = []
        self.innerWalls = []
        tr = (30, 30)
        tl = (870, 30)
        br = (870, 570)
        bl = (30, 570)
        self.outerWalls = [geom.Line(tl, tr), geom.Line(bl, br), geom.Line(tr, br), geom.Line(tl, bl)]
        for y in range(0, 20):
            temp = []
            for x in range(0, 30):
                colour = image.get_at((x, y))
                if colour == (255, 127, 0):
                    temp.append(WALL)
                    if x < 29 and x > 0 and y < 19 and y > 0:
                        self.innerWalls.append((x, y))
                    self.walls.append((x, y))
                elif colour == (255, 0, 0):
                    temp.append(BLOCK)
                    if x < 29 and x > 0 and y < 19 and y > 0:
                        self.innerWalls.append((x, y))
                    self.blocks.append((x, y))
                elif colour == (0,0,0):
                    temp.append(HOLE)
                    self.holes.append((x, y))
                else:
                    if colour == (0, 255, 0):
                        self.spawnPoints.append((x, y))
                    elif colour == (0, 0, 255):
                        self.playerSpawn = (x*30+15, y*30+15)
                    temp.append(0)
            self.level.append(temp)
            
    def draw(self, surface):
        y = 0
        for i in self.level:
            x = 0
            for j in i:
                if j == 0:
                    x+=1
                    continue
                elif j == 1:
                    pygame.draw.rect(surface, wallColour, pygame.Rect(x*30, y*30, 30, 30))
                elif j == 2:
                    pygame.draw.rect(surface, blockColour, pygame.Rect(x*30, y*30, 30, 30))
                elif j == 3:
                    pygame.draw.circle(surface, pygame.Color(25,25,25), (x*30+15, y*30+14), 14)
                x += 1
            y += 1

def spawnList(player, level, list):
    j = 0
    for i in list:
        x = level.spawnPoints[j][0]*30 + 15
        y = level.spawnPoints[j][1]*30 + 15
        if i == 1:
            TurretAgent((x, y))
        elif i == 2:
            SoldierAgent((x, y))
        elif i == 3:            
            HunterAgent((x, y))
        elif i == 4:
            BomberAgent((x, y))
        elif i == 5:
            RoverAgent((x, y))
        elif i == 6:
            SniperAgent((x, y))
        elif i == 8:
            SentryAgent((x, y))
        j+=1
        
#All the levels:
game = (
#1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5
(0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0),
(0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0),
(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0),
(0, 0, 2, 0, 0, 0, 1, 0, 0, 1, 0, 0, 2, 0, 0),
(2, 0, 0, 0, 0, 0, 1, 2, 0, 1, 2, 0, 0, 0, 0),
(0, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0),
(0, 0, 0, 0, 0, 3, 1, 0, 3, 1, 0, 0, 0, 0, 0),
(3, 0, 0, 0, 0, 0, 2, 0, 0, 2, 3, 0, 0, 0, 0),
(3, 0, 0, 0, 2, 0, 1, 0, 0, 1, 0, 0, 0, 3, 0),
(4, 3, 0, 0, 0, 0, 0, 0, 0, 1, 4, 0, 0, 0, 0),
(4, 0, 0, 0, 0, 0, 3, 0, 0, 3, 4, 0, 0, 0, 0),
(1, 0, 0, 0, 0, 0, 3, 0, 0, 3, 1, 0, 4, 0, 0),
(0, 0, 0, 0, 0, 3, 4, 0, 0, 4, 0, 0, 0, 0, 4),
(3, 0, 0, 0, 3, 3, 0, 0, 0, 0, 3, 0, 0, 0, 3),
(0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0),
(0, 6, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0),
(0, 6, 0, 3, 0, 0, 6, 0, 0, 0, 4, 0, 0, 0, 0),
(0, 6, 0, 6, 0, 0, 6, 0, 0, 0, 3, 0, 0, 0, 0),
(0, 8, 0, 3, 0, 0, 8, 0, 0, 0, 6, 0, 0, 0, 0),
(0, 8, 0, 0, 0, 0, 6, 6, 0, 0, 0, 0, 0, 0, 0)
)

