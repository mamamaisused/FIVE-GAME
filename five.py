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
SCREENRECT = Rect(0, 0, 550, 550)
PLAYERSIZE = 20
INIT_VIR_POS = (9,4)#line 10,row 5
main_dir = os.path.split(os.path.abspath(__file__))[0]
gamedata[INIT_VIR_POS[0]][INIT_VIR_POS[1]] = 1
print(gamedata)

class chess(Enum):
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

class Player(pygame.sprite.Sprite):
    images = []    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = pygame.Rect(RIGHTBOUND[0]/2 - PLAYERSIZE/2,RIGHTBOUND[0]-PLAYERSIZE/2,20,20)
        #virtual position
        self.pos = position(INIT_VIR_POS[0],INIT_VIR_POS[1])
        self.speed = MOVESTEP   
        self.origtop = self.rect.top 
        #print(self.rect)
        self.bounce = 24   

    def move(self, direction):
        if direction<2:
            self.rect.move_ip(direction*self.speed, 0)
        else:
            self.rect.move_ip(0,(direction-3)*self.speed)#2--up,4--down
        #dont let player out of the screen
        #self.rect = self.rect.clamp(SCREENRECT)
        #self.rect.top = (self.origtop - (self.rect.left//self.bounce%2))
    def chessdone(self):
        pass

class black_player(Player):
    def __init__(self):
        self.role = chess.black
    def init_img(self,imgs=[]):
        Player.images = imgs

def main():    
    pygame.init()
    clock = pygame.time.Clock()
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

    blacks = pygame.sprite.Group()
    blues = pygame.sprite.Group()
    all = pygame.sprite.RenderUpdates()
    #要先加入containers不然会说self没有container，不知道为什么
    black_player.containers = all
    #black_player.init_img([load_image("black.png")])

    bplay = black_player()
    bplay.init_img([load_image("black.png")])

    while True:
        all.clear(screen, background)

        #get input
        for event in pygame.event.get():
            if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return
            keystate = pygame.key.get_pressed()
            if keystate[K_RIGHT] == 1:
                bplay.move(1) 
            if keystate[K_LEFT] == 1:
                bplay.move(-1)
            if keystate[K_UP] == 1:
                bplay.move(2)
            if keystate[K_DOWN] == 1:
                bplay.move(4)        
        clock.tick(40)
        all.update()
        #draw the scene
        dirty = all.draw(screen)
        pygame.display.flip()
                

#call the "main" function if running this script
if __name__ == '__main__': main()
