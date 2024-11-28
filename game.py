#import lib = python, sys 
import pygame
import sys

from static import ScreenData
from level import Level

import start_screen
import level_selection

#Set the name for the window
GAMENAME = 'Coursework 2 Demo Game'

# Screen dimensions and setup
screen = ScreenData()
WIDTH , HEIGHT = screen.width, screen.height

current_screen = 'start_screen'
# Initialize Pygame and set up the screen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAMENAME)
level = 1
initial_enemies = 4
while True:
    if current_screen == 'start_screen':
        current_screen = start_screen.start_screen(screen)
        
    if current_screen == 'start_game':
        current_level = Level(level, initial_enemies)
        status = current_level.start_level(screen)
        if status == 'Next Level':
            level = level + 1

    elif current_screen == 'main_game':
        current_screen = level_selection.main_game(screen)

    
pygame.quit()