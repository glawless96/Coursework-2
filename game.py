import pygame
from start_screen import start_screen
from level_selection import main_game

from level import Level
from static import ScreenData
from game_utilities import setup_database, setup_operations_table, get_operations_by_user, User

# Game constants
GAMENAME = "Coursework 2 Demo Game"

# Screen dimensions
screen_data = ScreenData()
WIDTH, HEIGHT = screen_data.width, screen_data.height

# Initialize Pygame and screen
pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAMENAME)

# Game state
current_screen = "start_screen"
level = 1
difficulty = 1
max_difficulty = 20
initial_enemies = 4
time_limit = 360 

pygame.mixer.init()
pygame.mixer.music.load('data\\music\\start_level.wav')
pygame.mixer.music.set_volume(0)
pygame.mixer.music.play()

setup_database()
setup_operations_table()
user = User()
user_id =''
# Main game loop
while True:
    print(user, user)
    if current_screen == "start_screen":
        if user.username != None:
            user_data = get_operations_by_user(user_id)
            right_questions = sum(1 for data in user_data if data["correctly_answered"])
            wrong_questions = len(user_data) - right_questions

            # Update user details
            if user_data:
                user.update_user_details(
                    id=user_id,
                    username=user.username,
                    level=user_data[0]["level"],
                    difficulty=user_data[0]["difficulty"],
                    total_question=len(user_data),
                    right_question=right_questions,
                    wrong_question=wrong_questions,
                )
            else:
                user.update_user_details(
                    id=user_id,
                    username=user.username,
                    level=0,
                    difficulty=0,
                    total_question=0,
                    right_question=0,
                    wrong_question=0,
                )

        # Show the start screen and handle its return data
        return_data = start_screen(screen, user)
        if return_data:
            # Update game state and user based on return data
            current_screen = return_data.get("current_screen")
            user_id = return_data.get("current_user").id
            user.username = return_data.get("current_user").username

    elif current_screen == "start_game":
        pygame.mixer.music.stop()
        current_level = Level(level, difficulty, initial_enemies, time_limit)
        status = current_level.start_level(screen, user)
        if status == "New Question":
            if difficulty < max_difficulty:
                difficulty += 1
        elif status == "New Level":
            level += 1
            difficulty = 1

    elif current_screen == "continue_game":
        if level <= user.level:
            level = int(user.level) if isinstance(user.level, str) else user.level
        if difficulty <= user.difficulty:
            difficulty = int(user.difficulty) if isinstance(user.difficulty, str) else user.difficulty
        print(' ',type(level),' ', type(difficulty))
        current_level = Level(level, difficulty, initial_enemies, time_limit)
        status = current_level.start_level(screen, user)
        if status == "New Question":
            if difficulty < max_difficulty:
                difficulty += 1
        elif status == "New Level":
            level += 1
            difficulty = 1
        

pygame.mixer.music.stop()
pygame.quit()
