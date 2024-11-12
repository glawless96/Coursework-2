import pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((799, 600))
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load the player image and set it as the sprite image
        self.image = pygame.image.load("redman.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (49, 50))
        self.rect = self.image.get_rect()  # Set up rectangle based on image size
        self.rect.center = (50, 550)  # Start player in the center of the screen

    def update(self, enemies, wall):
        original_position = self.rect.topleft
        # Movement controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 4
        if keys[pygame.K_RIGHT]:
            self.rect.x += 4
        if keys[pygame.K_UP]:
            self.rect.y -= 4
        if keys[pygame.K_DOWN]:
            self.rect.y += 4
        
        if pygame.sprite.spritecollide(self, enemies, dokill = False) or pygame.sprite.spritecollide(self, wall, dokill = False):
            self.rect.topleft = original_position

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load the enemy image
        self.image = pygame.image.load("reaper.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (49, 50))
        self.rect = self.image.get_rect()  # Set up rectangle based on image size
        self.rect.center = (x, y)  # Position the enemy at (x, y)

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Initialize player and enemies
player = Player()

enemies = pygame.sprite.Group()
enemy1 = Enemy(130, 240)
enemy2 = Enemy(130, 500)
enemy3 = Enemy(50, 50)
enemy4 = Enemy(760, 50)
enemy5 = Enemy(150, 50)

enemies.add(enemy1)
enemies.add(enemy2)
enemies.add(enemy3)
enemies.add(enemy4)
enemies.add(enemy5)

# Create a group that includes only the player
all_sprites = pygame.sprite.Group(player)


# Create walls
walls = pygame.sprite.Group()
wall_layout = [
    # Outer walls
    (0, 0, 800, 10),   # Top border
    (0, 590, 800, 10), # Bottom border
    (0, 0, 10, 600),   # Left border
    (790, 0, 10, 600), # Right border

    # Maze-like walls to form paths
    (100, 180, 10, 340),    # Vertical wall close to left border 
    (100, 520, 200, 10),    # Horizontal wall close to bottom border, connected to wall above
    (400, 530, 10, 60),     # Small vertical wall in middle of map
    (400, 520, 150, 10),    # Horizontal wall above the small vertical wall
    (650, 530, 10, 60),     # Small vertical wall forming a gap
    (400, 300, 240, 10),    # Horizontal wall near center, creating a dead end
    (640, 200, 10, 110),    # Vertical wall at 640
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

    # Update player position
    player.update(enemies, walls)


    # Draw everything
    screen.fill((0, 0, 0))

    all_sprites.draw(screen)       # Draw the player
    enemies.draw(screen)           # Draw all enemies
    walls.draw(screen)

    pygame.display.flip()
    clock.tick(59)  # 30 FPS

pygame.quit()
