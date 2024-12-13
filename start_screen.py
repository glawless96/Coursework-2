#import lib = python, sys
import pygame
import sys

#importing buttons
from button import Button
from static import ScreenData, StartScreenData, ColorData
from login_popup import LoginPopup

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
    user = {}

    #load background image
    start_bgImage = pygame.image.load(STARTSCREEN_Image)
    start_bgImage = pygame.transform.scale(start_bgImage, (WIDTH, HEIGHT))
    
    title_text = title_font.render("", True, color.white)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

    # after hover (199, 193, 110)
    new_game_button = Button(100, 100, 200, 50, shape = 'rect', color = (254, 247, 140), text = NEWGAME_BUTTONLABEL,
                    hover_color=(245, 238, 135), text_color = (0, 0, 0), font_size = 36, alpha = 170, border_radius = 10)
    continue_game_button = Button(100, 160, 200, 50, shape='rect', color = (254, 247, 140), text = CONTINUE_BUTTONLABEL,
                hover_color=(245, 238, 135), text_color = (0, 0, 0), font_size = 36, alpha = 170, border_radius = 10)
    quit_game_button = Button(100, 500, 200, 50, shape = 'rect', color = (254, 247, 140), text = QUIT_BUTTONLABEL,
                hover_color=(245, 238, 135), text_color = (0, 0, 0), font_size = 36, alpha = 170, border_radius = 10)

    login_game_button = Button(100, 430, 200, 50, shape = 'rect', color = (254, 247, 140), text = "Login",
                hover_color=(245, 238, 135), text_color = (0, 0, 0), font_size = 36, alpha = 170, border_radius = 10)

    buttons = [new_game_button, continue_game_button, quit_game_button, login_game_button]

    running = True
    login_popup_instance = None  # Track if login popup is open

    # Create a translucent rectangle surface
    overlay_rect = pygame.Surface((300, 620))  # Adjust size for buttons
    overlay_rect.set_alpha(170)  # Set transparency
    overlay_rect.fill((50, 50, 50))  # Dark gray color

    howtoplay_rect = pygame.Surface(( 500 ,235)) 
    howtoplay_rect.set_alpha(170)
    howtoplay_rect.fill((50, 50, 50))

    feedback_rect = pygame.Surface(( 500 ,285)) 
    feedback_rect.set_alpha(170)
    feedback_rect.fill((50, 50, 50))

    while running:
        screen.fill(color.black)  # Set background color
        screen.blit(start_bgImage, (0, 0))  # Draw background
        screen.blit(title_text, title_rect)

        screen.blit(overlay_rect, (50, 50))  # Center overlay
        screen.blit(howtoplay_rect, (730, 50))  # Right panel

        stat_font = pygame.font.Font(None, 36)

        # Instructions
        user_stats = [
            "How to Play:",
            "1. Click 'New Game' to start.",
            "2. Answer questions correctly.",
            "3. Track your progress!",
            "Login to save your stats."
        ]

        y_offset = 70
        for stat in user_stats:
            stat_text = stat_font.render(stat, True, color.white)
            screen.blit(stat_text, (780, y_offset))
            y_offset += 40

        user = {
            "level": 1,
            'right_answers' : 10,
            'wrong_answers': 2,
            'total_questions': 12
        }
        if user:
            screen.blit(feedback_rect, (730, 355))  # Right panel
            feedback_stats = [ f"Level: {user['level']}",
                               f"Right Answers: {user['right_answers']}",
                               f"Wrong Answers: {user['wrong_answers']}",
                               f"Total Questions: {user['total_questions']}"
                            ]
            y_offset = 365
            user_name_header = stat_font.render("Welcome Test User", True, color.white)
            screen.blit(user_name_header, (780, y_offset))
            y_offset += 60
            for stat in feedback_stats:
                stat_text = stat_font.render(stat, True, color.white)
                screen.blit(stat_text, (780, y_offset))
                y_offset += 40

        mouse_pos = pygame.mouse.get_pos()

        # Draw buttons only if no popup is open
        if not login_popup_instance:
            for button in buttons:
                button.update_hover(mouse_pos)
                button.draw(screen)

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif login_popup_instance:
                # If popup is open, pass events to the popup
                action = login_popup_instance.handle_event(event)
                if action == "login":
                    print("Login successful!")
                    login_popup_instance = None  # Close popup
                    return "start_screen"
                elif action == "register":
                    print("Navigating to registration page...")
                    login_popup_instance = None  # Close popup
                    return "start_screen"
                elif action == "cancel":
                    print("Login cancelled.")
                    login_popup_instance = None  # Close popup
                    return "start_screen"
            else:
                # Handle button clicks when no popup is open
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.is_clicked(event.pos):
                            if button == new_game_button:
                                return 'start_game'  # Start new game
                            elif button == continue_game_button:
                                return 'main_game'  # Show level selection
                            elif button == quit_game_button:
                                running = False  # Quit game
                            elif button == login_game_button:
                                # Open login popup
                                login_popup_instance = LoginPopup(screen)

        # If login popup is active, draw it
        if login_popup_instance:
            login_popup_instance.update(mouse_pos)  # Update hover states for buttons
            login_popup_instance.draw()  # Draw popup on the screen

        pygame.display.flip()  # Update display
    pygame.quit()