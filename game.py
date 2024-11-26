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

while True:
    if current_screen == 'start_screen':
        current_screen = start_screen.start_screen(screen)
    elif current_screen == 'level_1':
        current_level = Level(1, 4)
        current_screen = current_level.start_level(screen)
    elif current_screen == 'level_2':
        current_level = Level(2, 8)
        current_screen = current_level.start_level(screen)
    elif current_screen == 'main_game':
        current_screen = level_selection.main_game(screen)
    else: 
        break
    
pygame.quit()