import pygame
import random
import math
from pygame import mixer


# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('Rocket.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('Background.png')

# Background sound
#mixer.music.load('background.wav')
#mixer.music.play(-1)

# Player
playerImg = pygame.image.load('rocket-ship.png')
PlayerX = 370
PlayerY = 480
PlayerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('ufo.png'))
    enemyX.append(random.randint(0, 767))
    enemyY.append(random.randint(50, 100))
    enemyX_change.append(10)
    enemyY_change.append(20)

# Bullet
# Ready state means you cant see bullet on screeen
# Fire - Bullet currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = "ready"

# Scoring system
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

#Game Over Font
over_font = pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    score = font.render ("Score :" + str(score_value),True, (255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200,250 ))

# Drawing the player (blit = draw)
def player(x, y):
    screen.blit(playerImg, (x, y))


# Drawing the enemy (blit = draw)
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# Drawing the bullet (blit+draw)
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow((enemyY - bulletY), 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # Background colour - RGB
    screen.fill((255, 255, 255))

    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():

        # if keystroke is pressed, check whether its left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                PlayerX_change = -5
            if event.key == pygame.K_RIGHT:
                PlayerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    # Get current coordinates of spaceship
                    bulletX = PlayerX
                    fire_bullet(bulletX, PlayerY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                PlayerX_change = 0

        if event.type == pygame.QUIT:
            running = False

    PlayerX += PlayerX_change
    # Player algorithm boundaries (so it doesnt go out of bound
    if PlayerX <= 0:
        PlayerX = 0
    elif PlayerX >= 768:
        PlayerX = 768


    # Enemy algorithm movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 450:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 10
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 768:
            enemyX_change[i] = -10
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 100

            enemyX[i] = random.randint(0, 767)
            enemyY[i] = random.randint(50, 100)

        # Bring in enemy
        enemy(enemyX[i], enemyY[i],i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change



        # Bring in player
    player(PlayerX, PlayerY)

    show_score(textX,textY)

    # Game window keeps updating every round
    pygame.display.update()
