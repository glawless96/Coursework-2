#import lib = python, sys 
import pygame
import sys

import start_screen
import main_game

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
    elif current_screen == 'main_game':
        current_screen = main_game.main_game(screen)
    else: 
        break
    
pygame.quit()