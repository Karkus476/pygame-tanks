import pygame

dir = "Resources/Textures/"
end = "_Body.png"
end2 = "_Turret.png"
images = {"Red":(pygame.image.load(dir + "Red" + end), pygame.image.load(dir+"Red"+end2)),
          "Blue":(pygame.image.load(dir + "Blue" + end), pygame.image.load(dir+"Blue"+end2)),
          "Green":(pygame.image.load(dir + "Green" + end), pygame.image.load(dir+"Green"+end2)),
          "Brown":(pygame.image.load(dir + "Brown" + end),pygame.image.load(dir + "Brown" + end2)),
          "Grey":(pygame.image.load(dir + "Grey" + end),pygame.image.load(dir + "Grey" + end2)),
          "Teal":(pygame.image.load(dir + "Teal" + end),pygame.image.load(dir + "Teal" + end2)),
          "Yellow":(pygame.image.load(dir + "Yellow" + end),pygame.image.load(dir + "Yellow" + end2))}

class Image:
    def __init__(self, surface):
        self.surface = surface
        self.orig = surface
        self.rect = self.surface.get_rect() 

    def draw(self, s, x, y):
        s.blit(self.surface, (x - self.rect.w/2,y - self.rect.h/2))
        
    def rotate(self, angle):
        self.surface = pygame.transform.rotate(self.surface, angle)
        self.rect = self.surface.get_rect()
        
    def scale(self, to):
        self.surface = pygame.transform.scale(self.surface, to)
        self.rect = self.surface.get_rect()
        return self
    
    def norm(self):
        self.surface = self.orig

    @staticmethod
    def getTankImage(colour, no=2):
        if no == 1 or no == 0:
            return images[colour][no]
        else:
            return images[colour][0], images[colour][1]
        
xpImgs = [Image(pygame.image.load(dir + "xpl_1.png")),
          Image(pygame.image.load(dir + "xpl_2.png")),
          Image(pygame.image.load(dir + "xpl_3.png")),
          Image(pygame.image.load(dir + "xpl_4.png")),
          Image(pygame.image.load(dir + "xpl_5.png")),
          Image(pygame.image.load(dir + "xpl_6.png")),
          Image(pygame.image.load(dir + "xpl_7.png"))]