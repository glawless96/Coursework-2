import pygame
import random
from static import ColorData, MazeData, HeaderData
from LevelMathUtil import LevelMathUtil

maze_static = MazeData()
color = ColorData()
header_static = HeaderData()
math_utils = LevelMathUtil()

CELL_SIZE = maze_static.cell_size

class Collectible():
    def __init__(self, x, y, image_paths, animation_paths=None, label="Collect Me"):
        self.x = x
        self.y = y + header_static.height
        self.image_paths = image_paths
        self.images = [pygame.image.load(image).convert_alpha() for image in image_paths]
        self.images = [pygame.transform.scale( img, (CELL_SIZE, CELL_SIZE)) for img in self.images]
        self.current_image = 0  # Start with the first image
        self.rect = self.images[0].get_rect(topleft=(self.x, self.y))

        self.animation_paths = animation_paths or []
        self.animation_frames = [pygame.image.load(image).convert_alpha() for image in animation_paths] if animation_paths else []
        self.animation_frame = 0  # For the animation
        self.is_collected = False

        # Add text label
        self.label = label
        self.font = pygame.font.Font(None, 30)  # Adjust font size as necessary
        self.text_surface = self.font.render(self.label, True, (0, 0, 0))

        self.offset = header_static.height

    def draw(self, screen):
        if self.is_collected:
            if self.animation_frame < len(self.animation_frames):
                screen.blit(self.animation_frames[self.animation_frame], (self.x, self.y))
                self.animation_frame += 1
            else:
                self.is_collected = False  # Stop animation when done
        else:
            # Draw image of the collectible scaled to fit the cell size
            scaled_image = pygame.transform.scale(self.images[self.current_image], (CELL_SIZE, CELL_SIZE))
            screen.blit(scaled_image, (self.x, self.y))

            # Draw the text label on the collectible
            text_rect = self.text_surface.get_rect(center=(self.x + CELL_SIZE // 2, self.y + CELL_SIZE // 2))
            screen.blit(self.text_surface, text_rect)

    def collect(self):
        self.is_collected = True
        self.animation_frame = 0

    def is_colliding(self, player):
        player_rect = pygame.Rect(player.col * CELL_SIZE, player.row * CELL_SIZE + self.offset, CELL_SIZE, CELL_SIZE)
        return self.rect.colliderect(player_rect)
    
    def generate_target_number(level):
        if level == 1:
            return random.randint(2, 9)
        elif level == 2:
            return random.randint(10, 30)
        elif level == 3:
            return random.randint(30, 50)
        elif level == 4:
            return random.randint(50, 80)
        elif level == 5:
            return random.randint(80, 100)
        else:
            return random.randint(10, 100)
        # return math_utils.get_target_number(level)
        
    def get_addition_solutions_set(number):
        def helper(target, current_combination, start, results):
            if target == 0:
                results.append(current_combination[:])
                return
            for i in range(start, target + 1):
                current_combination.append(i)
                helper(target - i, current_combination, i, results)
                current_combination.pop()
        
        results = []
        helper(number, [], 1, results)

        unique_numbers = sorted({num for combination in results for num in combination})

        return unique_numbers
