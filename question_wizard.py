# main.py

import pygame
import sys
import random
from button import Button
from question_generator import Question
from collision_handler import handle_collision

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Math Question Game")

# Colors and font
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
font = pygame.font.Font(None, 36)

# Button and game variables
button_width, button_height = 50, 50
number_buttons = []
question = Question()
dragging = False
dragged_button = None
offset_x, offset_y = 0, 0

def create_number_buttons(collected_numbers):
    print('create num buttons ',collected_numbers)
    global number_buttons
    number_buttons = []
    for i, num in enumerate(collected_numbers):
        x, y = 50, 50 + i * (button_height + 10)
        button = Button(x, y, button_width, button_height,'rect', color = (254, 247, 140), text = str(num),
                            hover_color=(245, 238, 135), text_color = (255, 255, 255), font_size = 36, alpha = 150)
        number_buttons.append(button)
    
    return number_buttons

def draw_setup_screen(screen, collected_numbers):
    screen.fill(WHITE)
    title = font.render("Collect Numbers for the Math Challenge", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
    instruction = font.render("Press SPACE to start", True, BLACK)
    screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, 100))
    for i, num in enumerate(collected_numbers):
        text = font.render(str(num), True, BLACK)
        screen.blit(text, (100 + i * 60, 200))

def draw_question_screen(screen, number_buttons):
    screen.fill(WHITE)
    for button in number_buttons:
        button.draw(screen)
    for i, (x, y, label) in enumerate(question.get_slots()):
        pygame.draw.rect(screen, GRAY, (x, y, button_width, button_height))
        slot_text = font.render(label, True, BLACK)
        slot_text_rect = slot_text.get_rect(center=(x + button_width // 2, y + button_height // 2))
        screen.blit(slot_text, slot_text_rect)
    prompt_text = font.render(f"Find two numbers that add up to {question.target_sum}", True, BLACK)
    screen.blit(prompt_text, (300, 100))

def check_and_display_result(screen):
    if question.check_solution():
        result_text = font.render("Correct!", True, BLACK)
    else:
        result_text = font.render("Incorrect. Try Again!", True, BLACK)
    screen.blit(result_text, result_text.get_rect(center=(WIDTH // 2, HEIGHT - 50)))
    pygame.display.flip()
    pygame.time.delay(2000)


def start_question_wizard(screen, collected_numbers):
    global dragging, dragged_button, offset_x, offset_y
    print("start question scree ",collected_numbers)
    clock = pygame.time.Clock()
    number_buttons = create_number_buttons(collected_numbers)
    draw_question_screen(screen, number_buttons)
    question.generate_question(collected_numbers)
    check_and_display_result(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN :
                for button in number_buttons:
                    print('active ',button.active, ' ||  button.update_hover(event.pos) ',button.update_hover(event.pos))
                    if button.active:
                        dragging = True
                        dragged_button = button
                        offset_x = event.pos[0] - button.x
                        offset_y = event.pos[1] - button.y
                        break

            elif event.type == pygame.MOUSEBUTTONUP and dragging:
                dragging = False
                if dragged_button:
                    for i, (x, y, _) in enumerate(question.get_slots()):
                        slot_rect = pygame.Rect(x, y, button_width, button_height)
                        if slot_rect.collidepoint(event.pos):
                            question.set_slot_value(i, dragged_button.text)
                            dragged_button.deactivate()  # Deactivate the button once dropped
                            break
                    dragged_button = None
                    check_and_display_result(screen)

            elif event.type == pygame.MOUSEMOTION and dragging:
                if dragged_button:
                    dragged_button.x = event.pos[0] - offset_x
                    dragged_button.y = event.pos[1] - offset_y

            

        pygame.display.flip()
        clock.tick(30)
