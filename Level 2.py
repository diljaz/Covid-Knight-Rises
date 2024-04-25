import mysql.connector
mydb = mysql.connector.connect(
      host="127.0.0.1",
      user="root",
      passwd="diljaz@123",
      database="game")
cursor=mydb.cursor()
import math,random, sys
import pygame
from pygame.locals import *

# exit the program
def events():
      for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                  pygame.quit()
                  sys.exit()

# define display surface                  
W, H = 1280, 720
HW, HH = W / 2, H / 2
AREA = W * H

# initialise display
pygame.init()
CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((W, H))
pygame.display.set_caption("LEVEL 2")
FPS = 60

walkRight = [pygame.image.load(r'C:\Users\DIL\Desktop\Pygame\Game\Right\R1.png'),pygame.image.load(r'C:\Users\DIL\Desktop\Pygame\Game\Right\R2.png'), pygame.image.load(r'C:\Users\DIL\Desktop\Pygame\Game\Right\R3.png'), pygame.image.load(r'C:\Users\DIL\Desktop\Pygame\Game\Right\R4.png'), pygame.image.load(r'C:\Users\DIL\Desktop\Pygame\Game\Right\R5.png'), pygame.image.load(r'C:\Users\DIL\Desktop\Pygame\Game\Right\R6.png'), pygame.image.load(r'C:\Users\DIL\Desktop\Pygame\Game\Right\R7.png'), pygame.image.load(r'C:\Users\DIL\Desktop\Pygame\Game\Right\R8.png'), pygame.image.load(r'C:\Users\DIL\Desktop\Pygame\Game\Right\R9.png')]
walkLeft = [pygame.image.load(r'C:\Users\DIL\Desktop\Pygame\Game\Left\L1.png'), pygame.image.load(r'C:\Users\DIL\Desktop\Pygame\Game\Left\L2.png'), pygame.image.load(r'C:\Users\DIL\Desktop\Pygame\Game\Left\L3.png'), pygame.image.load(r'C:\Users\DIL\Desktop\Pygame\Game\Left\L4.png'), pygame.image.load(r'C:\Users\DIL\Desktop\Pygame\Game\Left\L5.png'), pygame.image.load(r'C:\Users\DIL\Desktop\Pygame\Game\Left\L6.png'), pygame.image.load(r'C:\Users\DIL\Desktop\Pygame\Game\Left\L7.png'), pygame.image.load(r'C:\Users\DIL\Desktop\Pygame\Game\Left\L8.png'), pygame.image.load(r'C:\Users\DIL\Desktop\Pygame\Game\Left\L9.png')]


bg = pygame.image.load(r"Backgrounds_2.png").convert()
bgWidth, bgHeight = bg.get_rect().size

score=0
health=10
x=input("Enter Name:")
cursor.execute("Insert into LEVELTWO values(""\'"+ x +"\',""\'"+ str(score) +"\',""\'"+ str(health) +"\','no')")
mydb.commit()

stageWidth=bgWidth*2
stagePosX = 0
startScrollingPosX = HW


class player(object):
    def __init__(self, x,y, width ,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.v=4
        self.health=10
        self.visible=True
        self.isjump=False
        self.left=False
        self.right=False
        self.jumpcount=10
        self.walkcount=0
        self.standing=True
        self.hitbox=(self.x + 17, self.y + 11, 29,52)

    def draw(self,screen):
        if self.visible:
              if self.walkcount + 1 >= 27:
                  self.walkcount = 0
              
              if not self.standing:
                  if self.left:  
                      DS.blit(walkLeft[self.walkcount//3], (self.x,self.y))  
                      self.walkcount += 1                           
                  elif self.right:
                      DS.blit(walkRight[self.walkcount//3], (self.x,self.y))
                      self.walkcount += 1
              else:
                  if self.right:
                      DS.blit(walkRight[0], (self.x,self.y)) 
                  else:
                      DS.blit(walkLeft[0],(self.x,self.y))
              self.hitbox=(self.x + 17, self.y+11, 29,52)
              pygame.draw.rect(screen,(255,0,0),(self.hitbox[0],self.hitbox[1]-20,50,10))
              pygame.draw.rect(screen,(0,255,0),(self.hitbox[0],self.hitbox[1]-20,50 - (5*(10-self.health)),10))
        
    def hit(self):
        if self.health>0:
            self.health-=2
        elif self.health==0:
            self.visible=False
        self.isjump=False
        self.jumpcount=10
        self.x=32
        self.y=520
        self.walkcount=0
        font1=pygame.font.SysFont('bahnschrift',100)
        text=font1.render('-1',1,(250,250,250))
        DS.blit(text,(500,100))
        pygame.display.update()
        i=0
        while i<100:
            pygame.time.delay(5)
            i+=1
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    i=301
                    pg.quit()
                    
class hand(object):
    hand = pygame.image.load(r'hand sanitizer.png')
    
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.hitbox=(self.x + 17, self.y+2, 31,57)
        self.visible=True
        
    def draw(self,screen): 
          if self.visible==True:
                DS.blit(self.hand,(self.x,self.y))
                self.hitbox=(self.x + 15, self.y +2, 31,57)

    def hit(self):
          self.visible=False

class enemy(object):
    corona = pygame.image.load(r'corona21.png')
    
    def __init__(self,x,y,width,height,end):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.end=end
        self.path= [self.x,self.end]
        self.vel=6
        self.hitbox=(self.x + 17, self.y+2, 31,57)
        self.health=3
        self.visible=True

    def draw(self,screen):
        self.move()
        if self.visible==True:
            DS.blit(self.corona,(self.x,self.y))
            self.hitbox=(self.x + 14, self.y , 31,57)
            
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1] :
                self.x +=self.vel
            else:
                self.vel = self.vel * -1
                self.x+=self.vel
                self.walkcount=0
        else:
            if self.x - self.vel > self.path[0]:
                self.x+=self.vel
            else:
                self.vel=self.vel*-1
                self.x +=self.vel
                self.walkcount=0

    def hit(self):
        if self.health>0:
            self.health-=1
        elif self.health<=0:
            self.visible=False
            
class projectile(object):
    def __init__(self,x,y,radius,colour,facing):
        self.x=x
        self.y=y
        self.radius=radius
        self.colour=colour
        self.facing=facing
        self.vel=8*facing
        
    def draw(self,screen):
        pygame.draw.circle(DS,(0,240,255), (self.x,self.y), self.radius)
    

# main loop
Collectible='No'
font=pygame.font.SysFont("bahnschrift",30,True)
man=player(32,520,80,80)
h=hand(1200,535,64,64)
enemies=[]
maxenemies=2
for i in range(maxenemies):
      enemies.append(enemy(random.randint(100,500), random.randint(480,530), 64, 64,1216))
manRadius = 32
manPosX = manRadius
shootloop=0
bullets=[]
while True:
      events()
      for i in range(maxenemies):
            if enemies[i].visible==True:
                  if man.hitbox[1] < enemies[i].hitbox[1]+enemies[i].hitbox[3] and man.hitbox[1] + man.hitbox[3] > enemies[i].hitbox[1]:
                        if man.hitbox[0] + man.hitbox[2]> enemies[i].hitbox[0] and man.hitbox[0]< enemies[i].hitbox[0] + enemies[i].hitbox[2]:
                              man.hit()
                              score-=1
                              health-=2
                          
            for bullet in bullets:
                 if enemies[i].visible==True:     
                        if bullet.y - bullet.radius< enemies[i].hitbox[1]+ enemies[i].hitbox[3] and bullet.y + bullet.radius > enemies[i].hitbox[1]:
                              if bullet.x + bullet.radius> enemies[i].hitbox[0] and bullet.x - bullet.radius< enemies[i].hitbox[0] + enemies[i].hitbox[2]:
                                    enemies[i].hit()
                                    score+=1
                                    bullets.pop(bullets.index(bullet))

      if h.visible==True:
            if man.hitbox[1] < h.hitbox[1]+ h.hitbox[3] and man.hitbox[1] + man.hitbox[3] > h.hitbox[1]:      
                  if man.hitbox[0] + man.hitbox[2]> h.hitbox[0] and man.hitbox[0]< h.hitbox[0] + h.hitbox[2]:    
                        h.hit()
                        score+=5
                        Collectible='Yes'

      keys=pygame.key.get_pressed()
      
      if shootloop>0:
            shootloop+=1

      if shootloop>3:
            shootloop=0

      for bullet in bullets:
            if bullet.x<1280 and bullet.x>0:
                  bullet.x += bullet.vel
            else:
                  bullets.pop(bullets.index(bullet))
            
      if keys[pygame.K_SPACE] and shootloop==0:
            if man.left:
                  facing = -1
            else:
                  facing = 1
                  
            if len(bullets) < maxenemies:
                  bullets.append(projectile(round(man.x + man.width//2), round(man.y + man.height//2), 5, (0,0,0),facing))
                        
            shootloop=1

      if keys[pygame.K_LEFT]:
            man.x-=man.v
            man.left=True
            man.right=False
            man.standing=False
      elif keys[pygame.K_RIGHT]:
            man.x+=man.v
            man.left=False
            man.right=True
            man.standing=False
      else:
            man.walkcount = 0
            man.standing=True
      if not man.isjump :
            if keys[pygame.K_UP]:
                  man.isjump=True
                  man.right=False
                  man.left=False
                  man.walkcount=0
      else:
            if man.jumpcount >= -10:
                  neg=1
                  if man.jumpcount<0:
                        neg=-1
                  man.y-=(man.jumpcount**2) * 0.5 * neg
                  man.jumpcount-=1
            else:
                  man.isjump=False
                  man.jumpcount=10
                                                                                                                                                                                                       
      if man.x > bgWidth-64:
            man.x = bgWidth-64
      if man.x < 0:
            man.x = 0
            
      if man.x < startScrollingPosX:
            manPosX = man.x
      elif man.x > stageWidth - startScrollingPosX:
            manPosX = man.x - stageWidth + W
      else:
            manPosX = startScrollingPosX
            stagePosX+= -1
      
      rel_x = stagePosX % bgWidth
      DS.blit(bg, (rel_x - bgWidth, 0))
      if rel_x < W:
            DS.blit(bg, (rel_x, 0))
    
      text=font.render("Score:" + str(score),1,(255,255,255))
      DS.blit(text,(640,10))
      man.draw(DS)
      h.draw(DS)
      for i in range(maxenemies):
            enemies[i].draw(DS)
      for bullet in bullets:
            bullet.draw(DS)
      pygame.display.update()
      if Collectible=='Yes':
            cursor.execute("Update LEVELTWO set Score=""\'"+ str(score) +"\', Health=""\'"+ str(health) +"\', Collectible='Yes' where Name=""\'"+ x +"\'")
            mydb.commit()
            pygame.quit()
            sys.exit()
      if man.health==0:
            cursor.execute("Update LEVELTWO set Score=""\'"+ str(score) +"\', Health=""\'"+ str(health) +"\', Collectible='No' where Name=""\'"+ x +"\'")
            mydb.commit()
            pygame.quit()
            sys.exit()
      if Collectible=="No":
            cursor.execute("Update LEVELTWO set Score=""\'"+ str(score) +"\', Health=""\'"+ str(health) +"\', Collectible='No' where Name=""\'"+ x +"\'")
            mydb.commit()
      CLOCK.tick(FPS)   
