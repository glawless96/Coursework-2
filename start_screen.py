#import lib = python, sys
import pygame
import sys

#Setting rgb colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 128)
RED = (255, 0, 0)
DARK_RED = (128, 0, 0)

#Set screen width and height
WIDTH, HEIGHT = 800, 600
# Button dimensions and positions
start_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 60)
quit_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 60)

#fonts
pygame.font.init()
title_font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

STARTSCREEN_Image = 'data\\images\\bg\\StartScreen_Background.jpg'

#function to draw buttons
def draw_button(screen, text, rect, color, hover_color, click_color, opacity=255):
    """Draws a button with text and changes color on hover."""
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()[0]
    
    if rect.collidepoint(mouse_pos):
        button_color = hover_color
        if mouse_click:
            button_color = click_color
    else:
        button_color = color


    button_color_with_opacity = (*button_color[:3], opacity)

    button_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(button_surface, button_color_with_opacity,  button_surface.get_rect(), border_radius=10)
    
    pygame.draw.rect(screen, button_color, rect, border_radius=10)

    button_text = button_font.render(text, True, WHITE)
    text_rect = button_text.get_rect(center=rect.center)
    screen.blit(button_text, text_rect)
    
def start_screen(screen):
    
    #load background image
    start_bgImage = pygame.image.load(STARTSCREEN_Image)
    start_bgImage = pygame.transform.scale(start_bgImage, (WIDTH, HEIGHT))
    
    title_text = title_font.render("", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

    while True:
        #set screen fill color
        screen.fill(BLACK)
        #set background
        screen.blit(start_bgImage, (0, 0))
        screen.blit(title_text, title_rect)

        # Draw buttons
        draw_button(screen, "Start Game", start_button_rect, BLUE, DARK_BLUE, (0, 255, 0), 100)
        draw_button(screen, "Quit", quit_button_rect, RED, DARK_RED, (255, 0, 0), 100)

        pygame.display.flip()  # Update the display

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_button_rect.collidepoint(mouse_pos):
                    return  # Start the game
                elif quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()