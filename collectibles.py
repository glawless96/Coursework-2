import pygame
import random

def place_images_randomly(maze, collectible_images, cell_size):
    rows = len(maze)
    cols = len(maze[0])
    empty_cells = [(y, x) for y in range(1, rows - 1) for x in range(1, cols - 1) if maze[y][x] == 0]
    
    collectibles = []
    for i, image in enumerate(collectible_images):
        if empty_cells:
            y, x = random.choice(empty_cells)
            empty_cells.remove((y, x))
            collectibles.append((x, y, image, i + 1))  # Add a number associated with the collectible

    return collectibles

def draw_collectibles(screen, collectibles, cell_size):
    font = pygame.font.Font(None, 24)  # Customize font size as needed
    for x, y, image, number in collectibles:
        screen.blit(image, (x * cell_size, y * cell_size))
        # Draw the number on top of the image
        text = font.render(str(number), True, (255, 0, 0))  # Red color for the number
        text_rect = text.get_rect(center=(x * cell_size + cell_size // 2, y * cell_size + cell_size // 2))
        screen.blit(text, text_rect)
