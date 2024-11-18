#import lib = python, sys 
import pygame
import sys

import start_screen
import level_selection

import level_1
import level_2

#Set the name for the window
GAMENAME = 'Coursework 2 Demo Game'

# Screen dimensions and setup
WIDTH, HEIGHT = 800, 600

current_screen = 'start_screen'
# Initialize Pygame and set up the screen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAMENAME)

while True:
    if current_screen == 'start_screen':
        current_screen = start_screen.start_screen(screen)
    elif current_screen == 'level_1':
        current_screen = level_1.start_level_1(screen)
    elif current_screen == 'level_2':
        current_screen = level_2.start_level_2(screen)
    elif current_screen == 'main_game':
        current_screen = level_selection.main_game(screen)
    else: 
        break
    



pygame.quit()