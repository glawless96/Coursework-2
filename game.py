import pygame
from start_screen import start_screen
from level_selection import main_game
from level import Level
from static import ScreenData

# Game constants
GAMENAME = "Coursework 2 Demo Game"

# Screen dimensions
screen_data = ScreenData()
WIDTH, HEIGHT = screen_data.width, screen_data.height

# Initialize Pygame and screen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAMENAME)

# Game state
current_screen = "start_screen"
level = 1
initial_enemies = 4
<<<<<<< Updated upstream
=======
time_limit = 360 

pygame.mixer.init()
pygame.mixer.music.load('data\\music\\start_level.wav')
pygame.mixer.music.set_volume(0)
pygame.mixer.music.play()
>>>>>>> Stashed changes

# Main game loop
while True:
    if current_screen == "start_screen":
        current_screen = start_screen(screen)

    elif current_screen == "start_game":
        current_level = Level(level, initial_enemies)
        status = current_level.start_level(screen)
        if status == "Next Level":
            level += 1

    elif current_screen == "main_game":
        current_screen = main_game(screen)

pygame.quit()
