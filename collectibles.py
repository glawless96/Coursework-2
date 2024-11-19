import pygame
import random
from static import Color

color = Color()

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
    font = pygame.font.Font(None, 36)  # Customize font size as needed
    for x, y, image, number in collectibles:
        screen.blit(image, (x * cell_size, y * cell_size))
        # Draw the number on top of the image
        text = font.render(str(number), True, color.black)  # Red color for the number
        text_rect = text.get_rect(center=(x * cell_size + cell_size // 2, y * cell_size + cell_size // 2))
        screen.blit(text, text_rect)

def generate_target_number(level):
    if level == 1:
        return random.randint(0, 9)
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