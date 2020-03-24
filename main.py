"""
My take on a space invaders style game, with object oriented programming.
This is my first time learning OOP.
------------------------------------------
Icon & Enemy made by Smashicons from www.flaticon.com
Player made by Freepik from www.flaticon.com
Background image from NASA
"""
# pylint: disable-msg=C0103
import math
import random
import pygame
from pygame import mixer

# initialize screen
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

# background and sounds
background = pygame.Surface(screen.get_size())
background = background.convert()
background = pygame.image.load("background.jpg")
explosion = mixer.Sound('explosion.wav')
laser = mixer.Sound('laser.wav')
mixer.music.load("background.wav")
mixer.music.set_volume(0.15)
mixer.music.play(-1)

# title and Icon
icon = pygame.image.load("space-ship.png")
pygame.display.set_icon(icon)


class MovingObject:
    """Parent class for all moving objects in the game"""
    def __init__(self, image, x, y, SPEED, x_speed, y_speed):
        self.image = pygame.image.load(image)
        self.x = x
        self.y = y
        self.speed = SPEED
        self.x_speed = x_speed
        self.y_speed = y_speed

    def draw(self):
        """draws the object on the screen"""
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        """moves the object"""
        self.x += self.x_speed
        self.y += self.y_speed
        if self.x <= 0:
            self.x = 0
        elif self.x >= 747:
            self.x = 747

class Player(MovingObject):
    """Player subclass"""
    def fire_laser(self):
        """fires the player's laser"""
        laser.play()
        friendly_fire.append(Ammo('player_ammo.png', player.x, 440, 0, 0, -2))

class Enemy(MovingObject):
    """Enemy subclass"""
    def advance(self):
        """advances the object in a predictable fashion"""
        self.move()
        if self.x <= 0 or self.x >= 747:
            self.y_speed = 40
            self.x_speed *= -1
        else:
            self.y_speed = 0

    def drop_bomb(self):
        """drops the enemy's bombs"""
        hostile_fire.append(Ammo('enemy_ammo.png', self.x, self.y - 20, 0, 0, 2))

class Ammo(MovingObject):
    """ammo subclass"""
    def collision(self, target):
        """collision detection"""
        if self == target:
            return False
        distance = math.sqrt(math.pow(self.x - target.x, 2) + math.pow(self.y-target.y, 2))
        if distance <= 40:
            explosion.play()
            return True

# declarations
player = Player('player.png', 370, 480, 3, 0, 0)
enemies = [] #list to hold all the enemies (python doesn't have arrays)
NUM_OF_ENEMIES = 6
for i in range(NUM_OF_ENEMIES):
    enemies.append(Enemy('alien.png', random.randint(0, 800),
                         random.randint(50, 150), 2, 2, 0))
friendly_fire = [] # list to hold all the player's ammo objects
hostile_fire = [] # list to hold all the enemies' ammo objects
score_value = 0
SHIELD_COUNT = 3
font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)
shield_font = pygame.font.Font('freesansbold.ttf', 32)
ENEMY_FIRE = 25
game_is_over = False

pygame.time.set_timer(ENEMY_FIRE, 1500)

def redraw_game_window():
    """puts everything on the screen"""
    screen.blit(background, (0, 0))
    player.draw()
    for alien in enemies:
        alien.draw()
        if alien.y >= 445:
            game_over()
            #break
    for ammo in friendly_fire:
        ammo.draw()
    for bomb in hostile_fire:
        bomb.draw()
    show_score(10, 10)
    show_shields(625, 10)
    pygame.display.update()

def show_score(x, y):
    """displays the score"""
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over():
    """displays the game over screen"""
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    for alien in enemies:
        alien.x_speed = 0
        alien.y_speed = 0.5

def show_shields(x, y):
    """displays the number of shields remaining"""
    shield_text = shield_font.render("Shields: " + str(SHIELD_COUNT), True, (255, 0, 0))
    screen.blit(shield_text, (x, y))

# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                print("left")
                player.x_speed = -player.speed
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.x_speed = player.speed
            if event.key == pygame.K_SPACE:
                player.fire_laser()
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT or event.key == ord('a') or
                    event.key == pygame.K_RIGHT or event.key == ord('d')):
                player.x_speed = 0
        if event.type == ENEMY_FIRE:
            random_enemy = random.randint(0, len(enemies)-1)
            enemies[random_enemy].drop_bomb()
    for enemy in enemies:
        enemy.advance()
    for projectile in friendly_fire:
        projectile.move()
        if projectile.y <= 0:
            friendly_fire.remove(projectile)
            score_value -= 0.5
        for enemy in enemies:
            if projectile.collision(enemy):
                friendly_fire.remove(projectile)
                enemy.x = random.randint(0, 747)
                enemy.y = random.randint(50, 150)
                score_value += 1
    for bombs in hostile_fire:
        bombs.move()
        if bombs.y >= 480:
            hostile_fire.remove(bombs)
            if bombs.collision(player):
                SHIELD_COUNT -= 1
    if SHIELD_COUNT <= 0:
        game_over()
    player.move()
    redraw_game_window()
