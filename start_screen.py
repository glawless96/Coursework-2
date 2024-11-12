#import lib = python, sys
import pygame
import sys

#importing buttons
from button import Button

#Setting rgb colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 128)
RED = (255, 0, 0)
DARK_RED = (128, 0, 0)

#Set screen width and height
WIDTH, HEIGHT = 800, 600

NEWGAME_BUTTONLABEL = "New Game"
CONTINUE_BUTTONLABEL = "Continue..."
QUIT_BUTTONLABEL = "Exit"

#fonts
pygame.font.init()
title_font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

STARTSCREEN_Image = 'data\\images\\bg\\StartScreen_Background.jpg'
 
def start_screen(screen):
    
    #load background image
    start_bgImage = pygame.image.load(STARTSCREEN_Image)
    start_bgImage = pygame.transform.scale(start_bgImage, (WIDTH, HEIGHT))
    
    title_text = title_font.render("", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

    # after hover (199, 193, 110)
    new_game_button = Button(50, 100, 200, 50, shape = 'rect', color = (254, 247, 140), text = NEWGAME_BUTTONLABEL,
                    hover_color=(245, 238, 135), text_color = (255, 255, 255), font_size = 36, alpha = 150)
    continue_game_button = Button(50, 160, 200, 50, shape='rect', color = (254, 247, 140), text = CONTINUE_BUTTONLABEL,
                hover_color=(245, 238, 135), text_color = (255, 255, 255), font_size = 36, alpha = 150)
    quit_game_button = Button(50, 500, 100, 50, shape = 'circle', color = (254, 247, 140), text = QUIT_BUTTONLABEL,
                hover_color=(245, 238, 135), text_color = (255, 255, 255), font_size = 15, alpha = 150)

    buttons = [new_game_button, continue_game_button, quit_game_button]

    running = True

    while running:
        #set screen fill color
        screen.fill(BLACK)
        #set background
        screen.blit(start_bgImage, (0, 0))
        screen.blit(title_text, title_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        
        for button in buttons:
            button.update_hover(mouse_pos)
            button.draw(screen)
           
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in  buttons:
                    if button.is_clicked(event.pos):
                        if button == new_game_button:
                            return 'main_game'
                        elif button == continue_game_button:
                            return 'main_game'
                        elif button == quit_game_button:
                            running = False
        pygame.display.flip()  # Update the display

    pygame.quit()