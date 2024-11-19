import pygame
from static import CharacterData, HealthData, MazeData, HeaderData

maze_static = MazeData()
character_static = CharacterData()
health_static = HealthData()
header_static = HeaderData()

CELL_SIZE = maze_static.cell_size

class Player:
    def __init__(self, start_pos):
        self.row, self.col = start_pos
        self.image = pygame.image.load(character_static.front_image)
        self.health = health_static.maxHealth
        self.health_icon_size = (40, 40)
        self.health_images = [
            pygame.transform.scale(pygame.image.load(health_static.health_image), self.health_icon_size)
            for _ in range(self.health)
        ]
        self.shatter_frames = [pygame.image.load(character_static.front_image) for i in range(5)]
        self.is_blipping = False
        self.blip_timer = 0
        self.inventory = [] #collected Items
        self.offset = header_static.height


    def move(self, maze, direction):
        dr, dc = direction
        new_row, new_col = self.row + dr, self.col + dc
        if maze.layout[new_row][new_col] == 0:  # Check for a valid path
            self.row, self.col = new_row, new_col

    def start_blipping(self):
        self.is_blipping = True
        self.blip_timer = 30  # Blip for 30 frames

    def draw_health(self, screen):
        for i in range(self.health):
            x = 10 + i * (self.health_icon_size[0] + 5)
            y = 10
            screen.blit(self.health_images[i], (x, y))

    def shatter_health(self, screen):
        if self.health > 0:
            x = 10 + (self.health - 1) * (self.health_icon_size[0] + 5)
            y = 10
            for frame in self.shatter_frames:
                screen.blit(frame, (x, y))
                pygame.display.flip()
                pygame.time.delay(50)

    def handle_collision(self, screen):
        if self.health > 0 and not self.is_blipping:
            self.shatter_health(screen)  # Shatter the last health icon
            self.start_blipping()       # Start the blipping effect
            self.health -= 1            # Decrease health

    def draw(self, screen):
        if self.is_blipping:
            # Toggle visibility every 5 frames
            if self.blip_timer % 10 < 5:
                x, y = self.col * CELL_SIZE, self.row * CELL_SIZE + self.offset
                screen.blit(self.image, (x, y))
            self.blip_timer -= 1
            if self.blip_timer <= 0:
                self.is_blipping = False
        else:
            x, y = self.col * CELL_SIZE, self.row * CELL_SIZE + self.offset
            screen.blit(self.image, (x, y))

    def collect(self, collectibles):
        for collectible in collectibles:
            if collectible.is_colliding(self):
                collectible.collect()
                self.inventory.append(collectible)
                # collectibles.remove(collectible)
                print(f"Collected item at ({collectible.x}, {collectible.y})!")
