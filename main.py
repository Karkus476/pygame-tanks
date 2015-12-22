import pygame, sys, math, geom, level, time, geom
from pygame.locals import *
from entity import Entity
from player import Player

from bullet import Bullet
from level import Level
from bomb import Bomb
from agent import Agent
from turret import TurretAgent
from soldier import SoldierAgent
from hunter import HunterAgent
from bomber import BomberAgent
from track import Track
from path import Path
from path import squareToTank
from server import Server
from client import Client

pygame.init()
fpsClock = pygame.time.Clock()

surface = pygame.display.set_mode((900, 600))
trackSurface = pygame.Surface((900, 600))
pygame.display.set_caption("Tanks!")

blackColour = pygame.Color(0,0,0)
blueColour = pygame.Color(0,0,255)
beigeColour = pygame.Color(235, 185, 125)

gameLevel = Level(pygame.image.load("Resources/Textures/Levels/level1.png"))
player = Player(gameLevel.playerSpawn)

delta = 0
levelNo = 0

mode = "Normal"
#Ask what mode to set to
i = raw_input("Type something to play mulitplayer. Otherwise press Enter")
if i != "":
    i = raw_input("Type something to start a server. Press enter not to start a server.")
    if i != "":
        s = Server()
        s.start()
        mode = "Server"
    else:
        i = raw_input("Are you going to play as a Client? Type stuff to say yes")
        if i != "":
            i = raw_input("Type the IP Address to which you wish to connect")
            c = Client(i)
            c.start()
            mode = "Client"
else:
    mode = "Normal"
        
def game():
    global levelNo, delta, gameLevel, player, beigeColour, surface
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                Bomb((player.getX(), player.getY()))
        if event.type == MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                player.shoot()
                
    if len(Entity.agentIds) == 0:
        Entity.clear(gameLevel)
        player.setX(gameLevel.playerSpawn[0])
        player.setY(gameLevel.playerSpawn[1])
        level.spawnList(player, gameLevel, level.game[levelNo])
        levelNo += 1
    
    Entity.tickAll(pygame.key.get_pressed(), pygame.mouse.get_pos(), player,gameLevel, delta)
       
    surface.fill(beigeColour)
    trackSurface.blit(surface, (0,0))
    
    gameLevel.draw(surface)
    Entity.drawAll(trackSurface, surface, delta)
    
    pygame.display.flip()
    
    pygame.display.set_caption("Tanks:" + str(len(Entity.agentIds)) + " Level:" + str(levelNo) + " FPS:" + str(math.floor(fpsClock.get_fps())))
    delta = fpsClock.get_time()

def multiplayer():
    global levelNo, delta, gameLevel, player, beigeColour, surface
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                Bomb((player.getX(), player.getY()))
        if event.type == MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                player.shoot()
                
    #if len(Entity.agentIds) == 0:
    #    Entity.clear(gameLevel)
    #    player.setX(gameLevel.playerSpawn[0])
    #    player.setY(gameLevel.playerSpawn[1])
    #    level.spawnList(player, gameLevel, level.game[levelNo])
    #    levelNo += 1
    
    Entity.tickAll(pygame.key.get_pressed(), pygame.mouse.get_pos(), player,gameLevel, delta)
       
    surface.fill(beigeColour)
    trackSurface.blit(surface, (0,0))
    
    gameLevel.draw(surface)
    Entity.drawAll(trackSurface, surface, delta)
    
    pygame.display.flip()
    
    pygame.display.set_caption("Tanks:" + str(len(Entity.agentIds)) + " Level:" + str(levelNo) + " FPS:" + str(math.floor(fpsClock.get_fps())))
    delta = fpsClock.get_time()
    
while True:
    if mode == "Normal":
        game()
    else:
        multiplayer()
    fpsClock.tick(60)
