import pygame
from pygame.locals import *
import random as rd

pygame.init()
#screen setting
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Tuku the boss")

#backgorund image, enemy iamge, bullet image
background = pygame.image.load('image/space.png')
enemy = pygame.image.load('image/enem.png')
enemy1 = pygame.image.load('image/enem1.png')
bullet = pygame.image.load('image/bullet1.png')
tuku = pygame.image.load('image/tuku g.png')

#axis manipulation
enemyy=20
enemy1y=20
enemy2y=20
enemy3y=20
enemy4y=20
enemy5y=20
enemyx=1
enemyx_change=1

enemy1x=750
enemy1x_change=1

enemy2x=rd.randint(20,750)
enemy2x_change=1
enemy3x=rd.randint(20,750)
enemy3x_change=1
enemy4x=rd.randint(20,750)
enemy4x_change=1
enemy5x=rd.randint(20,750)
enemy5x_change=1

tukux=400
tukuy=520
tuku_change=0

bulletx=tukux-3
bullety=540
bullet_change=5
bullet_state="ready"

#icon image
icon = pygame.image.load('image/foot.png')
pygame.display.set_icon(icon)

def fire_bullet(x , y):
    global bullet_state
    bullet_state ="fire"
    screen.blit(bullet,(x,y))
    
def distance(x1,y1,x2,y2):
    distance = ((((x2-x1))**2+((y2-y1)**2))**0.5)
    return distance
score_no=0
font=pygame.font.Font('freesansbold.ttf',32)
def score():
    scr=font.render("SCORE:-"+str(score_no),True,(255,255,0))
    screen.blit(scr,(10,10))

flag = True  #while running loop flag
while flag:
    screen.blit(background,(0,0))
    screen.blit(enemy,(enemyx,enemyy))
    screen.blit(enemy1,(enemy1x,enemy1y))
    screen.blit(enemy,(enemy2x,enemy2y))
    screen.blit(enemy1,(enemy3x,enemy3y))
    screen.blit(enemy,(enemy4x,enemy4y))
    screen.blit(enemy1,(enemy5x,enemy5y))
    screen.blit(tuku,(tukux,tukuy))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == K_LEFT:
                tuku_change=-2
            if event.key == K_RIGHT:
                tuku_change=2
            if bullet_state is "ready":
                if event.key == K_SPACE:
                    fire_bullet(tukux,bullety)
                    bulletx=tukux-3
        if event.type == pygame.QUIT:
            flag = False
    if bullet_state is "fire":
        fire_bullet(bulletx,bullety)
        bullety-=4
        if distance(bulletx,bullety,enemyx,enemyy) <50:
            bullety=540
            bullet_state="ready"
            enemyy=20
            score_no+=5
        if distance(bulletx,bullety,enemy1x,enemy1y)  <50:
            bullety=540
            bullet_state="ready"
            enemy1y=20
            score_no+=5
        if distance(bulletx,bullety,enemy2x,enemy2y) <50:
            bullety=540
            bullet_state="ready"
            enemy2y=20
            score_no+=5
        if distance(bulletx,bullety,enemy3x,enemy3y) <50:
            bullety=540
            bullet_state="ready"
            enemy3y=20
            score_no+=5
        if distance(bulletx,bullety,enemy4x,enemy4y) <50:
            bullety=540
            bullet_state="ready"
            enemy4y=20
            score_no+=5
        if distance(bulletx,bullety,enemy5x,enemy5y) <50:
            bullety=540
            bullet_state="ready"
            enemy5y=20
            score_no+=5
        if bullety==20:
            bullet_state="ready"
            bullety=540
    tukux+=tuku_change
    if tukux == 750:
        tuku_change=0
    elif tukux == 2:
        tuku_change=0
    if enemyx==770:
        enemyy+=50
        enemyx_change=-1
    elif enemyx==0:
        enemyy+=50
        enemyx_change=1
    if enemy3x==770:
        enemy3y+=50
        enemy3x_change=-1
    elif enemy3x==0:
        enemy3y+=50
        enemy3x_change=1
    if enemy5x==770:
        enemy5y+=50
        enemy5x_change=-1
    elif enemy5x==0:
        enemy5y+=50
        enemy5x_change=1
    if enemy1x==10:
        enemy1y+=50
        enemy1x_change=-1
    elif enemy1x==770:
        enemy1y+=50
        enemy1x_change=1
    if enemy2x==10:
        enemy2y+=50
        enemy2x_change=-1
    elif enemy2x==770:
        enemy2y+=50
        enemy2x_change=1
    if enemy4x==10:
        enemy4y+=50
        enemy4x_change=-1
    elif enemy4x==770:
        enemy4y+=50
        enemy4x_change=1
    enemyx+=enemyx_change
    enemy1x-=enemy1x_change
    enemy2x-=enemy2x_change
    enemy3x+=enemy3x_change
    enemy4x-=enemy4x_change
    enemy5x+=enemy5x_change
    score()
    pygame.display.update()
    
pygame.quit()