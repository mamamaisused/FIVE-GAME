import os.path

#import basic pygame modules
import pygame
from pygame.locals import *

import numpy
from enum import Enum

gamedata = numpy.zeros((10,10), numpy.int)
MOVESTEP = 50
LEFTBOUND = (50,50)
RIGHTBOUND = (500,500)
SCREENRECT     = Rect(0, 0, 550, 550)
main_dir = os.path.split(os.path.abspath(__file__))[0]
print(gamedata)
print(gamedata[3][5])

class CHASE(Enum):
    none = 0
    black = 1
    white = 2

class position:
    x = 0
    y = 0
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y

def load_image(file):
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert()

class Player_black(pygame.sprite.Sprite):
    pos = position(0,0)
    def __init__(self,img):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect(20,20)
        self.image = load_image(img)

    def move(self, direction):
        if direction: self.facing = direction
        self.rect.move_ip(direction*self.speed, 0)
        self.rect = self.rect.clamp(SCREENRECT)
        self.rect.top = self.origtop - (self.rect.left//self.bounce%2)

def main():
    pygame.init()
    # Set the display mode
    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
    #create the background, tile the bgd image
     
    background = load_image('background.gif')
    #for x in range(0, SCREENRECT.width, bgdtile.get_width()):
    #background.blit(bgdtile, (0, 0))
    screen.blit(background, (0,0))
    pygame.display.flip()

#call the "main" function if running this script
if __name__ == '__main__': main()
