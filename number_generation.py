import pygame
import random

pygame.init()
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("number generation")
font = pygame.font.SysFont("Arial", 40)
BLACK = (0, 0, 0)
PINK = (255, 105, 180)
positions = [
    (random.randint(0, screen_width - 100), random.randint(0, screen_height - 50))
    for _ in range(10)
]
random_numbers = [random.randint(0, 60) for _ in range(10)]
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(BLACK)
    for i, num in enumerate(random_numbers):
        text = font.render(str(num), True, PINK)
        x, y = positions[i]
        screen.blit(text, (x, y))
    pygame.display.flip()

pygame.quit()
