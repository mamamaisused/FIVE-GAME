import os.path
import copy

#import basic pygame modules
import pygame
from pygame.locals import *

import numpy
from enum import Enum

gamedata = numpy.zeros((10,10), numpy.int)
MOVESTEP = 50
LEFTBOUND = (50,50)
RIGHTBOUND = (500,500)
SCREENRECT = Rect(0, 0, 550, 600)
PLAYERSIZE = 20
INIT_VIR_POS = (9,0)#line 10,row 0
main_dir = os.path.split(os.path.abspath(__file__))[0]
#print(gamedata)
global WINNUM
WINNUM = 0


class chess(Enum):
    none = -1
    black = 1
    blue = 0

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
    pos = position(0,0)
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        #self.image = self.images[0]
        self.rect = pygame.Rect(MOVESTEP - PLAYERSIZE/2,RIGHTBOUND[0]-PLAYERSIZE/2,20,20)
        #virtual position
        self.pos.x = INIT_VIR_POS[0]
        self.pos.y = INIT_VIR_POS[1]
        self.pixelpos = position(MOVESTEP - PLAYERSIZE/2,RIGHTBOUND[0]-PLAYERSIZE/2)
        self.speed = MOVESTEP   
        self.origtop = self.rect.top 
        #print(self.rect)
        self.bounce = 24   

    def move(self, direction):
        if direction<2:
            self.rect.move_ip(direction*self.speed, 0)
            self.pixelpos.x += direction*self.speed
            self.pos.y += direction
        else:
            self.rect.move_ip(0,(direction-3)*self.speed)#2--up,4--down
            self.pixelpos.y += (direction-3)*self.speed
            self.pos.x += (direction-3)
    def resetpos(self):
        self.rect.move_ip((MOVESTEP - PLAYERSIZE/2)-self.pixelpos.x, (RIGHTBOUND[0]-PLAYERSIZE/2)-self.pixelpos.y)
        self.pos.x = INIT_VIR_POS[0]
        self.pos.y = INIT_VIR_POS[1]
        self.pixelpos.x =  MOVESTEP - PLAYERSIZE/2
        self.pixelpos.y =  RIGHTBOUND[0]-PLAYERSIZE/2
    
    

class chess_player(Player):
    image = pygame.surface
    def __init__(self):
        Player.__init__(self)
        self.role = chess.black
    def init_img(self,imgs=[]):
        Player.images = imgs
        self.image = imgs[0]
    def switchplayer(self):
        if(self.role == chess.black):
            self.role = chess.blue
            self.image = Player.images[1]
        elif(self.role == chess.blue):
            self.role = chess.black
            self.image = Player.images[0]        
    def chessdone(self):
        if(self.role == chess.black):
            gamedata[Player.pos.x][Player.pos.y] = 1
        else:
            gamedata[Player.pos.x][Player.pos.y] = -1
        #print(gamedata)
    



def main():   
    global WINNUM 
    pygame.init()
    clock = pygame.time.Clock()
    # Set the display mode
    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size)
    #create the background, tile the bgd image    
    background = load_image('background.gif')
    #for x in range(0, SCREENRECT.width, bgdtile.get_width()):
    #background.blit(bgdtile, (0, 0))
    screen.blit(background, (0,0))
    pygame.display.flip()

    all = pygame.sprite.RenderUpdates()
    #要先加入containers不然会说self没有container，不知道为什么
    chess_player.containers = all

    pblack= chess_player()
    pblack.init_img([load_image("black.png"),load_image("blue.png")])

    INFO = "PLAYING ..."
    myfont = pygame.font.Font(None,60)
    white = 255,255,255
    textImage = myfont.render(INFO,True,white)
     

    while True:
        screen.blit(textImage,(200,550)) 
        all.clear(screen,background)
        #关于显示与刷新需要再研究
        #get input
        for event in pygame.event.get():
            if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return
            keystate = pygame.key.get_pressed()
            if keystate[K_RIGHT] == 1:
                pblack.move(1) 
            if keystate[K_LEFT] == 1:
                pblack.move(-1)
            if keystate[K_UP] == 1:
                pblack.move(2)
            if keystate[K_DOWN] == 1:
                pblack.move(4) 
            if keystate[K_SPACE] == 1:
                screen.blit(pblack.image,(pblack.pixelpos.x,pblack.pixelpos.y))
                background.blit(pblack.image,(pblack.pixelpos.x,pblack.pixelpos.y))
                pblack.chessdone()
                pblack.switchplayer() 
                #pblack.resetpos() 
                win_test(1)
                win_test(-1)
                if WINNUM != 0:
                    print (WINNUM)
                if WINNUM == 1:
                    print ("black win")
                else:
                    print ("blue win")
        '''
        clock.tick(40)
        #all.update()
        #draw the scene
        #all.draw(screen)
        pygame.display.flip()


def win_test(no):
    winflag1 = 0
    winflag2 = 0
    winflag3 = 0
    winflag4 = 0
    for i in range(0,10):
        for j in range(0,10):
            #print(winflag,i,j)
            if winflag1 != 0:
                if gamedata[i][j] == no:
                    winflag1 += 1
                else:
                    winflag1 = 0
            else:
                if gamedata[i][j] == no:
                    winflag1 = 1
            if winflag1 == 5:
                WINNUM = no
    for i in range(0,10):
        for j in range(0,10):
            #print(winflag,i,j)
            if winflag2 != 0:
                if gamedata[j][i] == no:
                    winflag2 += 1
                else:
                    winflag2 = 0
            else:
                if gamedata[j][i] == no:
                    winflag2 = 1
            if winflag2 == 5:
                WINNUM = no
    j = 0
    k = 0
    for i in range(0,19):
        #print("------")
        for j,k in zip(range(0,i+1),range(i,-1,-1)):
            if k<10 and j<10:
                #print (j,k,end=' ')
                if winflag3 != 0:
                    if gamedata[j][k] == no:
                        winflag3 += 1
                    else:
                        winflag3 = 0
                else:
                    if gamedata[j][k] == no:
                        winflag3 = 1
                if winflag3 == 5:
                    WINNUM = no
    for i in range(-9,10):
        #print("------")
        for j,k in zip(range(i,10),range(0,10)):
            if k>=0 and j>=0: 
                #print (j,k,end=' ')
                if winflag4 != 0:
                    if gamedata[j][k] == no:
                        winflag4 += 1
                    else:
                        winflag4 = 0
                else:
                    if gamedata[j][k] == no:
                        winflag4 = 1
                if winflag4 == 5:
                    WINNUM = no


            
            
                

#call the "main" function if running this script
if __name__ == '__main__': main()
