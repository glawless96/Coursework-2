#import lib = python, sys
import pygame
import sys

#importing buttons
from button import Button
from static import ScreenData, StartScreenData, ColorData

#Setting rgb colors
color = ColorData()


#Set screen width and height
screen = ScreenData()
WIDTH , HEIGHT = screen.width, screen.height

start_screen_static = StartScreenData()

NEWGAME_BUTTONLABEL = start_screen_static.new_button
CONTINUE_BUTTONLABEL = start_screen_static.contiune_button
QUIT_BUTTONLABEL = start_screen_static.quit_button

#fonts
pygame.font.init()
title_font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

STARTSCREEN_Image = start_screen_static.background_image
 
def start_screen(screen):
    
    #load background image
    start_bgImage = pygame.image.load(STARTSCREEN_Image)
    start_bgImage = pygame.transform.scale(start_bgImage, (WIDTH, HEIGHT))
    
    title_text = title_font.render("", True, color.white)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

    # after hover (199, 193, 110)
    new_game_button = Button(50, 100, 200, 50, shape = 'rect', color = (254, 247, 140), text = NEWGAME_BUTTONLABEL,
                    hover_color=(245, 238, 135), text_color = (0, 0, 0), font_size = 36, alpha = 170, border_radius = 10)
    continue_game_button = Button(50, 160, 200, 50, shape='rect', color = (254, 247, 140), text = CONTINUE_BUTTONLABEL,
                hover_color=(245, 238, 135), text_color = (0, 0, 0), font_size = 36, alpha = 170, border_radius = 10)
    quit_game_button = Button(50, 500, 200, 50, shape = 'rect', color = (254, 247, 140), text = QUIT_BUTTONLABEL,
                hover_color=(245, 238, 135), text_color = (0, 0, 0), font_size = 36, alpha = 170, border_radius = 10)

    buttons = [new_game_button, continue_game_button, quit_game_button]

    running = True

    while running:
        #set screen fill color
        screen.fill(color.black)
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
                            return 'start_game' #start new game
                        elif button == continue_game_button:
                            return 'main_game' #show level selection
                        elif button == quit_game_button:
                            running = False #quit
        pygame.display.flip()  # Update the display

    pygame.quit()