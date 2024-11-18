import pygame
import random

pygame.init()
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Number Generation")
font = pygame.font.SysFont("Arial", 30)
BLACK = (0, 0, 0)
PINK = (255, 105, 180)
GREEN = (0, 255, 0)  
WHITE = (255, 255, 255)  

backpack_rect = pygame.Rect(0, screen_height - 50, screen_width, 50)  
positions = [
    (random.randint(0, screen_width - 100), random.randint(0, screen_height - 150))  
    for _ in range(10)
]
random_numbers = [random.randint(0, 60) for _ in range(10)]

collected_numbers = []
collected_positions = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for i, num in enumerate(random_numbers):
                num_rect = pygame.Rect(positions[i][0], positions[i][1], 50, 50)
                if num_rect.collidepoint(pos):  
                    collected_numbers.append(num)  
                    collected_positions.append(positions[i])  
                    random_numbers[i] = None  
                    positions[i] = (-100, -100)  
            if backpack_rect.collidepoint(pos):
                for i, collected_num in enumerate(collected_numbers):
                    collected_text_rect = pygame.Rect(130 + i * 50, screen_height - 45, 50, 50)
                    if collected_text_rect.collidepoint(pos): 
                        original_position = collected_positions[i]
                        original_number = collected_num
                        collected_numbers.pop(i)
                        collected_positions.pop(i)
                        random_numbers.append(original_number)  
                        positions.append(original_position) 
    screen.fill(BLACK)
    pygame.draw.rect(screen, (50, 50, 50), backpack_rect)  
    backpack_text = font.render("number:", True, WHITE)
    screen.blit(backpack_text, (10, screen_height - 45))
    for i, num in enumerate(collected_numbers):
        collected_text = font.render(str(num), True, WHITE)
        collected_surface = pygame.Surface((50, 50))
        collected_surface.fill((50, 50, 50))  
        collected_surface.blit(collected_text, (0, 0))
        screen.blit(collected_surface, (130 + i * 50, screen_height - 45))
    for i, num in enumerate(random_numbers):
        if num is not None:  
            text = font.render(str(num), True, PINK)
            x, y = positions[i]
            screen.blit(text, (x, y))
    pygame.display.flip()
pygame.quit()
