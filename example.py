import pygame
import characters
import enemies 
pygame.init()

# Set up display
screen = pygame.display.set_mode((799, 600))
clock = pygame.time.Clock()

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

player = characters.baseCharacterClass()

enemyGroup = pygame.sprite.Group()

enemy1 = enemies.Enemy1(230, 240)
enemy2 = enemies.Enemy2(730, 70)

enemyGroup.add(enemy1)
enemyGroup.add(enemy2)

all_sprites = pygame.sprite.Group(player)


walls = pygame.sprite.Group()
wall_layout = [
    # Outer walls
    (0, 0, 800, 10),   # Top border
    (0, 590, 800, 10), # Bottom border
    (0, 0, 10, 600),   # Left border
    (790, 0, 10, 600), # Right border

    (100, 180, 10, 340),
    (100, 520, 200, 10),
    (400, 530, 10, 60),
    (400, 520, 150, 10),
    (650, 530, 10, 60),
    (400, 300, 240, 10),
    (640, 200, 10, 110),
    (100, 170, 430, 10),
    (550, 300, 10, 230),
    (100, 10, 10, 80),
    (100, 90, 300, 10),
    (520, 90, 10, 90),
    (400, 420, 250, 10),
    (520, 90, 120, 10),
    (100, 350, 200, 10),
]

for x, y, width, height in wall_layout:
    walls.add(Wall(x, y, width, height))


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update(enemyGroup, walls)
    for monster in enemyGroup:
        monster.update(walls) 

    screen.fill((0, 0, 0))

    all_sprites.draw(screen)       
    player.health.draw(screen)
    enemyGroup.draw(screen)
    walls.draw(screen)

    pygame.display.flip()
    clock.tick(60) 

pygame.quit()
