#import lib = python, sys
import pygame
import sys

#importing buttons
from button import Button
from static import ScreenData, StartScreenData, ColorData
from login_popup import LoginPopup
from game_utilities import get_operations_by_user

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
 
def start_screen(screen, user):

    start_bgImage = pygame.image.load(STARTSCREEN_Image)
    start_bgImage = pygame.transform.scale(start_bgImage, (WIDTH, HEIGHT))
    
    title_text = title_font.render("", True, color.white)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

    new_game_button = Button(100, 100, 200, 50, shape = 'rect', color = (254, 247, 140), text = NEWGAME_BUTTONLABEL,
                    hover_color=(245, 238, 135), text_color = (0, 0, 0), font_size = 36, alpha = 170, border_radius = 10)
    continue_game_button = Button(100, 160, 200, 50, shape='rect', color = (254, 247, 140), text = CONTINUE_BUTTONLABEL,
                hover_color=(245, 238, 135), text_color = (0, 0, 0), font_size = 36, alpha = 170, border_radius = 10)
    quit_game_button = Button(100, 500, 200, 50, shape = 'rect', color = (254, 247, 140), text = QUIT_BUTTONLABEL,
                hover_color=(245, 238, 135), text_color = (0, 0, 0), font_size = 36, alpha = 170, border_radius = 10)

    login_game_button = Button(100, 430, 200, 50, shape = 'rect', color = (254, 247, 140), text = "Login",
                hover_color=(245, 238, 135), text_color = (0, 0, 0), font_size = 36, alpha = 170, border_radius = 10)
    if user.username != None:
        buttons = [new_game_button, continue_game_button, quit_game_button]
    else:
        buttons = [new_game_button, continue_game_button, quit_game_button, login_game_button]

    running = True
    login_popup_instance = None  
    overlay_rect = pygame.Surface((300, 620))  
    overlay_rect.set_alpha(170)  
    overlay_rect.fill((23, 23, 23)) 

    howtoplay_rect = pygame.Surface(( 500 ,235)) 
    howtoplay_rect.set_alpha(170)
    howtoplay_rect.fill((23, 23, 23))

    feedback_rect = pygame.Surface(( 500 ,285)) 
    feedback_rect.set_alpha(170)
    feedback_rect.fill((23, 23, 23))

    while running:
        screen.fill(color.black) 
        screen.blit(start_bgImage, (0, 0))  
        screen.blit(title_text, title_rect)

        screen.blit(overlay_rect, (50, 50))  
        screen.blit(howtoplay_rect, (730, 50))  

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

        if user.username != None:
            screen.blit(feedback_rect, (730, 355))
            feedback_stats = [ 
                               f"Current Level: {user.level}",
                               f"Current Difficulty: {user.difficulty}",
                               f"Right Answers: {user.right_question}",
                               f"Wrong Answers: {user.wrong_question}",
                               f"Total Questions: {user.total_question}"
                            ]
            y_offset = 365
            user_name_header = stat_font.render(f"Welcome {user.username} ", True, color.white)
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
                return {"current_screen": "exit_game", "current_user": user} 
            elif login_popup_instance:
                # If popup is open, pass events to the popup
                login_details = login_popup_instance.handle_event(event)
                if login_details :
                    action = login_details['action']
                    current_user = login_details['user']
                    if action == "login":
                        login_popup_instance = None 
                        return  {"current_screen": "start_screen", "current_user": current_user}
                    elif action == "register":
                        login_popup_instance = None  
                        return  {"current_screen": "start_screen", "current_user": current_user}

                    elif action == "cancel":
                        login_popup_instance = None
                        return  {"current_screen": "start_screen", "current_user": current_user}
            else:
                # Handle button clicks when no popup is open
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.is_clicked(event.pos):
                            if button == new_game_button: 
                                return {"current_screen": "start_game", "current_user": user} 
                            elif button == continue_game_button:
                                return {"current_screen": "continue_game", "current_user": user} 
                            elif button == quit_game_button:
                                return {"current_screen": "exit_game", "current_user": user} 
                            elif button == login_game_button:
                                login_popup_instance = LoginPopup(screen)

        # If login popup is active, draw it
        if login_popup_instance:
            login_popup_instance.update(mouse_pos)  
            login_popup_instance.draw() 

        pygame.display.flip()