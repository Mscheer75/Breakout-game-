#!/usr/bin/python3.7
import pygame
from pygame import *
import random
pygame.font.init()
WIDTH = 800
HEIGHT = 600
WIDTHMIN = 0
HEIGHTMIN = 0
scr_size = (width,height) = (WIDTH, HEIGHT)
FPS = 60
black = (0,0,0,)
white = (255, 255, 255)

__color__ = [red, orange, yellow, green, blue, magenta] = [(255,0,0,),(255,165,0),(255,255,0),(0,255,0),(0,0,255),(255,0,255)]
clock = pygame.time.Clock()
screen = pygame.display.set_mode(scr_size)
pygame.display.set_caption('Breakout')


class Paddle():
    def __init__(self,x,y,sizex,sizey,color):
        self.image = pygame.Surface((sizex,sizey),SRCALPHA,32)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.length = sizex
        self.height = sizey

        self.image.fill(white)

        self.movement = [0,0]
        self.speed = 8
    def draw(self):
        self.checkBounds()
        screen.blit(self.image,self.rect)
        #print("drawing paddle")

    def update(self):
        self.rect = self.rect.move(self.movement)
    def checkBounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

class brick():
    def __init__(self, x,y,sizex, sizey, color):
        self.image = pygame.Surface((sizex,sizey),SRCALPHA,32)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.length = sizex
        self.height = sizey


        self.image.fill(color)
        self.hit = False

    def draw(self):
        if not self.hit:
            screen.blit(self.image,self.rect)
    def update(self):
        self.hit = True
class ball():
    def __init__(self, color, x, y, rad):
        self.ypos = y
        self.xpos = x
        self.color = color
        self.rad = rad
        self.Lspeed = random.randrange(5)
        self.Vspeed = random.randrange(5)
        self.leftmove = False
        self.downmove = True
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.xpos, self.ypos), self.rad)

    def reset(self):
        if self.ypos >= HEIGHT-10:
            print("reset")
            return True

    def update(self, hieght, width, minimumx, minimumy):

        if self.xpos <= width and self.leftmove == False:
            self.xpos = self.xpos + self.Lspeed 
            if self.xpos >= width:
                self.xpos = width
                self.leftmove = True
                self.vChange(hieght, width, minimumx, minimumy)

        if self.ypos  <= hieght and self.downmove == True:
            self.ypos = self.ypos + self.Vspeed
            if self.ypos >= hieght:
                self.ypos = hieght
                self.downmove = False
                self.vChange(hieght, width, minimumx, minimumy)
        if self.ypos >= minimumy and self.downmove == False:
            self.ypos = self.ypos - self.Vspeed
            if self.ypos <= minimumy:
                self.ypos = minimumy
                self.downmove = True
                self.vChange(hieght, width, minimumx, minimumy)
        if self.xpos >= minimumx and self.leftmove == True:
            self.xpos = self.xpos - self.Lspeed
            if self.xpos <= minimumx:
                self.xpos = minimumx
                self.leftmove = False
                self.vChange(hieght, width, minimumx, minimumy)



    def vChange(self, h, w, mx, my):
        #print("vchange")
        if self.ypos == h or self.ypos == my:
            self.Vspeed = random.randrange(4,7)
        if self.xpos == w or self.xpos == mx:
            self.Lspeed = random.randrange(3,8)

    def collision(self, otherBody):



        if type(otherBody) is Paddle and otherBody.rect.left <=  self.xpos and (otherBody.rect.left + otherBody.length/2) >= self.xpos and otherBody.rect.top +5>= self.ypos and otherBody.rect.top -1 <= self.ypos:

            #print("left")

            self.update(otherBody.rect.left, otherBody.rect.top, otherBody.length, otherBody.height)



            if self.downmove == True:
                self.downmove = False
            if self.leftmove == False:
                self.leftmove = True
            self.vChange(otherBody.height, otherBody.length, otherBody.rect.left, otherBody.rect.top)


        if type(otherBody) is Paddle and otherBody.rect.left + otherBody.length/2 <=  self.xpos and (otherBody.rect.left + otherBody.length ) >= self.xpos and otherBody.rect.top +5>= self.ypos and otherBody.rect.top -1 <= self.ypos:

            #print("right")
            self.update(otherBody.rect.left, otherBody.rect.top, otherBody.length, otherBody.height)



            if self.downmove == True:
                self.downmove = False
            self.leftmove = False
            #elif self.leftmove == False:
            #    self.leftmove = True
            self.vChange(otherBody.height, otherBody.length, otherBody.rect.left, otherBody.rect.top)



        if type(otherBody) is brick:
            if otherBody.rect.left <=  self.xpos and(otherBody.rect.left + otherBody.length ) >= self.xpos  and self.downmove == False: 
                if otherBody.rect.top + (otherBody.height + 2) >= self.ypos and otherBody.rect.top + ((otherBody.height /2)+1)  <= self.ypos:
                    otherBody.hit = True
                    self.update(otherBody.rect.left, otherBody.rect.top, otherBody.length, otherBody.height)
                    if self.downmove == False:
                        self.downmove = True
                    self.vChange(otherBody.height, otherBody.length, otherBody.rect.left, otherBody.rect.top)
                    print("top")

            elif otherBody.rect.left <=  self.xpos and (otherBody.rect.left + otherBody.length ) >= self.xpos and self.downmove == True: 
                if otherBody.rect.top - 2 <= self.ypos and otherBody.rect.top + ((otherBody.height /2)-1)  >= self.ypos:
                    otherBody.hit = True
                    self.update(otherBody.rect.left, otherBody.rect.top, otherBody.length, otherBody.height)
                    if self.downmove == True:
                        self.downmove = False
                    self.vChange(otherBody.height, otherBody.length, otherBody.rect.left, otherBody.rect.top)
                    print("bottom")
            elif otherBody.rect.left - 1 <=  self.xpos and(otherBody.rect.left + otherBody.length/6) - 1 >= self.xpos and self.leftmove == False: 
                if otherBody.rect.top <= self.ypos and otherBody.rect.top + (otherBody.height) >= self.ypos:
                    otherBody.hit = True
                    self.update(otherBody.rect.left, otherBody.rect.top, otherBody.length, otherBody.height)
                    if self.leftmove == False:
                        self.leftmove = True
                    self.vChange(otherBody.height, otherBody.length, otherBody.rect.left, otherBody.rect.top)
                    print("left")

            elif (otherBody.rect.left +  otherBody.length) - ((otherBody.length/6) +1) <=  self.xpos and (otherBody.rect.left + otherBody.length) + 1 >= self.xpos and self.leftmove == True: 
                if otherBody.rect.top  <= self.ypos and otherBody.rect.top + (otherBody.height) >= self.ypos:
                    otherBody.hit = True
                    self.update(otherBody.rect.left, otherBody.rect.top, otherBody.length, otherBody.height)
                    if self.leftmove == True:
                        self.leftmove = False
                    self.vChange(otherBody.height, otherBody.length, otherBody.rect.left, otherBody.rect.top)
                    print("right")







def main():
    exit = False

    gameOver = False
    myPaddle = Paddle(width/2, height - height/10,80,15, white)
    myBall =  ball(white, 300, 300, 5)
    bricks = []
    lives = 3
    for y in range(6):
        for x in range(19):
            bricks.append(brick((41*x + 10), (12*y) + 10, 40, 12, __color__[y])) 
    livesFont = pygame.font.SysFont('Comic Sans MS', 30)
    gameOverFont = pygame.font.SysFont('Comic Sans MS', 100)

    while not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    myPaddle.movement[0] = -1*myPaddle.speed
                    #print(myPaddle.rect.left)
                    myPaddle.checkBounds()
                if event.key == pygame.K_RIGHT:
                    myPaddle.movement[0] = 1*myPaddle.speed
                        #print(myPaddle.rect.left)
                    myPaddle.checkBounds()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        myPaddle.movement[0] = -1*myPaddle.speed
                        #print(myPaddle.rect.left)
                if event.key == pygame.K_RIGHT:
                    myPaddle.movement[0] = 1*myPaddle.speed
                        #print(myPaddle.rect.left)


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    myPaddle.movement[0] = 0

        screen.fill(black)
        textsurface = livesFont.render('Lives: ' +str(lives), False, white)
        screen.blit(textsurface,(0, 580))
        myPaddle.update()
        myPaddle.draw()
        myBall.update(HEIGHT,WIDTH, HEIGHTMIN, WIDTHMIN)
        myBall.collision(myPaddle)
        myBall.draw()

        if myBall.reset():
            myBall =  ball(white, 300, 300, 5)
            lives = lives -1
        if lives ==0:
                gameOver = True


        for x in range(len(bricks)):
            if bricks[x].hit is not True:
                myBall.collision(bricks[x])
            bricks[x].draw()
            #print(x)
        pygame.display.update()
            
        clock.tick(FPS)
    



exit = False
while not exit:
    main()
    exit = True

    
pygame.quit()
quit()

