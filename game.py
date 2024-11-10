#import lib = python, sys 
import pygame
import sys
from start_screen import start_screen
from main_game import main_game

#Set the name for the window
GAMENAME = 'Coursework 2 Demo Game'

# Screen dimensions and setup
WIDTH, HEIGHT = 800, 600

def main():
    # Initialize Pygame and set up the screen
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(GAMENAME)

    # Run the start screen first
    start_screen(screen)

    # After the start screen, run the main game
    main_game(screen)

if __name__ == "__main__":
    main()

