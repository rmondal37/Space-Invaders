import pygame
import random
import math

#mixer is a class in pygame module for music
from pygame import mixer

# initialize the pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((800,600))

#Background music
mixer.music.load("background.wav")
# -1 means the music plays on loop
mixer.music.play(-1)

#set the caption of the window and logo/icon
pygame.display.set_caption("Space Invaders!")
logo = pygame.image.load("space-invaders.png")
pygame.display.set_icon(logo)

#Player
playerImg = pygame.image.load("player.png")
#playerX and playerY are the x and y coordinates of player image
playerX = 370
playerY = 500
playerX_delta = 0

#Enemy
enemyImg = []
#enemyX and enemyY are the x and y coordinates of enemy image
enemyX = []
enemyY = []
enemyX_delta = []
enemyY_delta = []
num_enemies = 5

for i in range(0,num_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    #enemyX and enemyY are the x and y coordinates of enemy image
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,200))
    enemyX_delta.append(0.7)
    enemyY_delta.append(40)

#Bullet
bulletImg = pygame.image.load("bullet.png")
#bulletX and bulletY are the x and y coordinates of bullet image
bulletX = 0
bulletY = 500
bulletX_delta = 0
bulletY_delta = 1
# ready state: you cannot see the bullet on screen
# fire state: bullet is currently moving
bullet_state = "ready"

def player(x,y):
    screen.blit(playerImg, (x, y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    # we draw the image of the bullet at mid of spaceship
    screen.blit(bulletImg, (x + 16, y + 5))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    X = (enemyX - bulletX) * (enemyX - bulletX)
    Y = (enemyY - bulletY) * (enemyY - bulletY)
    distance  = math.sqrt(X + Y)
    if distance < 30:
        return True
    else:
        return False 

score_value  = 0
font  = pygame.font.Font('freesansbold.ttf', 30)
# textX and textY are the coordinates where we should show the score
textX = 650
textY = 10

gameoverfont = pygame.font.Font('freesansbold.ttf', 64) 

def show_score(x,y):
    score = font.render("Score:" + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

def game_over():
    over = gameoverfont.render("Game Over !!!", True, (255,255,255))
    screen.blit(over , (200, 250))



#implement the game loop with close functionality inside an infinite loop
#anything that we want to be persistent inside the game window goes inside this loop
running  = True
while running:
    #RGB color code for the game window
    screen.fill((0,0,102))

    
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            running = False
        
        if events.type == pygame.KEYDOWN:
            # A key has been pressed
            if events.key == pygame.K_LEFT:
                #The left arrow key is pressed
                playerX_delta = -0.9

            if events.key == pygame.K_RIGHT:
                # The right arrow key is pressed
                playerX_delta = 0.9

            if events.key == pygame.K_SPACE:
                # Bullet has been fired
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("shoot.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if events.type == pygame.KEYUP:
            if events.key == pygame.K_LEFT or events.key == pygame.K_RIGHT:
                # Key has been released
                playerX_delta = 0

    #Player movements and boundaries----------------
    playerX += playerX_delta
    if playerX <=0:
        playerX = 0
    
    if playerX >=736:
        playerX = 736

    #Enemy movements and boundaries-----------------
    #whenever enemyX goes <=0, make the delta positive , and when it goes to 736, then make it negative
    for i in range(0,num_enemies):

        if enemyY[i] >= 450:
            for j in range(0, num_enemies):
                enemy(2000, 2000, j)
            game_over()
            break

        enemyX[i] += enemyX_delta[i]
    
        if enemyX[i] <=0:
            enemyX_delta[i] = 0.7
            enemyY[i] += enemyY_delta[i]
    
        if enemyX[i] >=736:
            enemyX_delta[i] = -0.7
            enemyY[i] += enemyY_delta[i]

        hasCollided = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if hasCollided == True:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            score_value += 1
            bulletY = 500
            bullet_state = "ready"
            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(50,200)

        enemy(enemyX[i], enemyY[i], i)



    #Bullet movements-----------------

    # To ensure multiple bullets can be fired, reset bulletY = 500 as soon as bulletY<=0
    # also reset state of bullet as ready
    if bulletY <=0:
        bulletY = 500
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_delta

    


    player(playerX, playerY)
    show_score(textX, textY)

    #Adding this line is mandatory to keep updating the game window!!
    pygame.display.update()