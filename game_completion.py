# success_screen.py
import pygame
import sys

def show_success_screen(screen, width, height):
    # Fill the screen with a background color
    screen.fill((0, 128, 0))  # Dark green background

    # Set up fonts
    font = pygame.font.SysFont(None, 48)
    text = font.render("Congratulations! You've completed the level!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(width // 2, height // 2 - 50))
    
    # Display the text
    screen.blit(text, text_rect)

    # Display "Press any key to continue"
    continue_font = pygame.font.SysFont(None, 32)
    continue_text = continue_font.render("Press any key to continue...", True, (255, 255, 255))
    continue_text_rect = continue_text.get_rect(center=(width // 2, height // 2 + 50))
    screen.blit(continue_text, continue_text_rect)

    pygame.display.flip()

    # Wait for any key press to continue
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return  # Exit the function to go back to main game or exit the level
