import pygame
import sys
from start_screen import start_screen
from level_selection import main_game

from level import Level
from static import ScreenData
from game_utilities import setup_database, setup_operations_table, get_operations_by_user, User

# Initialize game
pygame.init()
pygame.mixer.init()

# Game constants
GAMENAME = "Coursework 2 Demo Game"
screen_data = ScreenData()
WIDTH, HEIGHT = screen_data.width, screen_data.height
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAMENAME)


# Database setup
setup_database()
setup_operations_table()

# Game variables
user = User()
user_id = ''
current_screen = "start_screen"
level, difficulty = 1, 1
max_difficulty, initial_enemies, time_limit = 20, 4, 360
running = True

# Main game loop
while running:
    # Handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game state handling
    if current_screen == "start_screen":
        if user.username:
            if user_id:
                user_data = get_operations_by_user(user_id)
                right_questions = sum(1 for data in user_data if data["correctly_answered"])
                wrong_questions = len(user_data) - right_questions
                user.update_user_details(
                    id=user_id,
                    username=user.username,
                    level=user_data[0]["level"] if user_data else 1,
                    difficulty=user_data[0]["difficulty"] if user_data else 1,
                    total_question=len(user_data),
                    right_question=right_questions,
                    wrong_question=wrong_questions,
                )
            else:
                user.update_user_details(id=user_id, username=user.username, level=1, difficulty=1, total_question=0, right_question=0, wrong_question=0)
        
        return_data = start_screen(screen, user)
        if return_data:
            current_screen = return_data.get("current_screen")
            if return_data.get("current_user"):
                user_id = return_data["current_user"].id
                user.username = return_data["current_user"].username

    elif current_screen == "start_game":
        pygame.mixer.music.stop()
        current_level = Level(level, difficulty, initial_enemies, time_limit)
        status = current_level.start_level(screen, user)
        if status == "New Question" and difficulty < max_difficulty:
            difficulty += 1
        elif status == "New Level":
            level += 1
            difficulty = 1
        elif status == "start_screen":
            current_screen = "start_screen"
        elif status == "exit_game":
            current_screen = "exit_game"

    elif current_screen == "continue_game":
        if user.id:
            level = max(level, int(user.level)) if isinstance(user.level, str) else user.level
            difficulty = max(difficulty, int(user.difficulty)) if isinstance(user.difficulty, str) else user.difficulty
        current_level = Level(level, difficulty, initial_enemies, time_limit)
        status = current_level.start_level(screen, user)
        if status == "New Question" and difficulty < max_difficulty:
            difficulty += 1
        elif status == "New Level":
            level += 1
            difficulty = 1
        elif status == "start_screen":
            current_screen = "start_screen"
        elif status == "exit_game":
            current_screen = "exit_game"

    elif current_screen == "exit_game":
        running = False

    pygame.display.flip() 

pygame.quit()
sys.exit()
