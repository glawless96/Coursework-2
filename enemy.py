import pygame   # type: ignore
import random
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Enemies")

WHITE = (255, 255, 255)

clock = pygame.time.Clock()

ENEMY_WIDTH = 150
ENEMY_HEIGHT = 150
ENEMY_SPEED = 2

ENEMY_IMAGES = [
    "1_en.png",
    "2_en.png",
    "3_en.png",
    "4_en.png",
    "5_en.png",
    "6_en.png",
    "7_en.png"

]

class NumberSnatcher:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT - ENEMY_HEIGHT)
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.speed_x = ENEMY_SPEED * random.choice([-1, 1])
        self.speed_y = ENEMY_SPEED * random.choice([-1, 1])
        
        image_path = random.choice(ENEMY_IMAGES)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
            self.speed_x *= -1  
        if self.y <= 0 or self.y >= SCREEN_HEIGHT - self.height:
            self.speed_y *= -1  

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

def game_loop():
    enemies = [NumberSnatcher() for _ in range(3)]  

    running = True
    while running:
        screen.fill(WHITE)  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for enemy in enemies:
            enemy.move()
            enemy.draw()

        pygame.display.flip()
        clock.tick(30)  

    pygame.quit()
    sys.exit()

game_loop()
