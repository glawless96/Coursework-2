import pygame
import random
from maze import Maze
from player import Player
from enemy import Enemy
from collectibles import Collectible
from static import CharacterData, ColorData, EnemyData, HeaderQuestions, MazeData, ScreenData
from head_up_display import HeadUpDisplay
from level_math_util import LevelMathUtil
from help_text import HelpTexts
from popup import PopUp
from operation_animation_manager import AnimationManager

# Static configurations
static_maze = MazeData()
color = ColorData()
main_screen = ScreenData()
char_image = CharacterData()
enemy_static = EnemyData()
math_utils = LevelMathUtil()
header_question = HeaderQuestions()


# Screen dimensions and properties
SCREEN_WIDTH = main_screen.width
SCREEN_HEIGHT = main_screen.height
CELL_SIZE = static_maze.cell_size

# Asset paths
MAZE_WALL_IMAGEURL = static_maze.wall_image
MAZE_PATH_IMAGEURL = static_maze.path_image
MAZE_END_IMAGEURL = static_maze.end_maze_image
PLAYER_IMAGEURL = char_image.front_image
COLLECTABLE_IMAGEURL = 'data\\images\\collectables\\collectable_2.png'

clock = pygame.time.Clock()

# Global variables for collected numbers
class Level:
    def __init__(self, current_level, current_difficulty, number_of_enemies, game_time_limit):
        self.level = current_level
        self.difficulty = current_difficulty
        self.enemies = number_of_enemies
        self.collected_numbers = []
        self.time_limit = game_time_limit

        self.target_number = math_utils.get_target_number(current_level, current_difficulty)
        self.operator = None
        self.possible_solutions = []
        self.game_question = None
        self.start_game_help_text = None

    def load_image(self, path, size=None, alpha=False):
        try:
            image = pygame.image.load(path).convert_alpha() if alpha else pygame.image.load(path).convert()
            if size:
                image = pygame.transform.scale(image, size)
            return image
        except pygame.error as e:
            print(f"Error loading image at {path}: {e}")
            return None

    def start_level(self, screen):

        # Generate random target number
        self.operator = math_utils.set_math_operator(self.level, self.difficulty) if self.operator is None else "+"
        self.game_question = get_question(self.operator)
        self.possible_solutions =  math_utils.get_all_possible_solutions(self.target_number, self.operator)
        self.start_game_help_text = HelpTexts(self.operator, self.target_number, self.level, self.difficulty)
        all_possible_solutions = self.possible_solutions
        print('Maths operations: ',self.operator)
        print('Target Number:', self.target_number)
        print('Possible Solutions:', all_possible_solutions)

        # Load images with proper error handling
        # wall_image = self.load_image(MAZE_WALL_IMAGEURL, (CELL_SIZE, CELL_SIZE), alpha=True) 
        path_image = self.load_image(MAZE_PATH_IMAGEURL, (CELL_SIZE, CELL_SIZE), alpha=True)
        inner_wall = self.load_image(static_maze.inner_wall, (CELL_SIZE, CELL_SIZE), alpha=True)
        player_image = self.load_image(PLAYER_IMAGEURL, (CELL_SIZE, CELL_SIZE), alpha=True)
        # end_image = self.load_image(MAZE_END_IMAGEURL, (CELL_SIZE, CELL_SIZE))
        
        top_wall = self.load_image(static_maze.top_wall, (CELL_SIZE, CELL_SIZE), alpha=True)
        top_right_wall = self.load_image(static_maze.top_right_wall, (CELL_SIZE, CELL_SIZE), alpha=True)
        right_wall = self.load_image(static_maze.right_wall, (CELL_SIZE, CELL_SIZE), alpha=True)
        bottom_right_wall = self.load_image(static_maze.bottom_right_wall, (CELL_SIZE, CELL_SIZE), alpha=True)
        bottom_wall = self.load_image(static_maze.bottom_wall, (CELL_SIZE, CELL_SIZE), alpha=True)
        bottom_left_wall =self.load_image(static_maze.bottom_left_wall, (CELL_SIZE, CELL_SIZE), alpha=True)
        left_wall = self.load_image(static_maze.left_wall, (CELL_SIZE, CELL_SIZE), alpha=True)
        top_left_wall = self.load_image(static_maze.top_left_wall, (CELL_SIZE, CELL_SIZE), alpha=True)

        # Initialize popups

        # Question popup / Start Game screen
        game_question_popup = PopUp(390, 100, 500, 420, (200, 200, 200), color.white)
        game_question_popup.set_title("Start Game", font_size=40, font_style="bold", color=(0,0,255))
        game_question_popup.set_message(f'Level : {self.level}', font_size=30, align="center", x=-70 )
        game_question_popup.set_message(f'Difficulty : {self.difficulty} / 20', font_size=30, align="center", x=70)
        game_question_popup.set_message( self.game_question + str(self.target_number), font_size=30, align="center", spacing=60)
        game_question_popup.set_message( self.start_game_help_text.helptext.title, border_group="group1", font_size=40, align="center", spacing=60, border_color=color.white, border_width=3, padding=20)
        for helptext in self.start_game_help_text.helptext.messages:
            game_question_popup.set_message(helptext, align="center", border_group="group1", font_size=30, color=color.white, spacing=30, border_color=color.white, border_width=3, padding=20)

        game_question_popup.add_button(-70, 170, 100, 40, shape='rect', color=(40, 209, 90), text="Start",
                                       hover_color=(38 , 199, 85), text_color=(255, 255, 255), font_size=36, alpha=170, border_radius=10)
        game_question_popup.add_button(70, 170, 100, 40, shape='rect', color=(255, 5, 21), text="Quit",
                                       hover_color=(209 , 4, 14), text_color=(255, 255, 255), font_size=36, alpha=170, border_radius=10)
        game_question_popup.show()


        #Help Screen popup
        help_popup = PopUp(390, 100, 500, 420, (200, 200, 200), color.white)
        help_popup.set_title("Help", font_size=40, font_style="bold", color=(0,0,255))

        help_popup.set_message( self.start_game_help_text.helptext.title, font_size=40, border_group="group1", align="center", spacing=60, border_color=color.white, border_width=3, padding=20)
        for helptext in self.start_game_help_text.helptext.messages:
            help_popup.set_message(helptext, align="center", font_size=30, color=color.white, border_group="group1", spacing=30, border_color=color.white, border_width=4, padding=20)

        help_popup.set_message(get_solution(self.operator, self.collected_numbers, self.target_number, all_possible_solutions), align="center", font_size=30, spacing = 60)

        help_popup.add_button(0, 170, 100, 40, shape='rect', color=(255, 5, 21), text="Close",
                                       hover_color=(209 , 4, 14), text_color=(255, 255, 255), font_size=36, alpha=170, border_radius=10)
        help_popup.show()

        # Game over popup
        game_over_popup = PopUp(390, 100, 500, 520, (200, 200, 200), color.white)
        game_over_popup.set_title("Game Over", font_size=50, font_style="bold", color=color.red)
        game_over_popup.add_button(-70, 150, 100, 40, shape='rect', color=(40, 209, 90), text="Retry",
                                   hover_color=(38 , 199, 85), text_color=(255, 255, 255), font_size=36, alpha=170, border_radius=10)
        game_over_popup.add_button(70, 150, 100, 40, shape='rect', color=(255, 5, 21), text="Quit",
                                   hover_color=(209, 4, 14), text_color=(255, 255, 255), font_size=36, alpha=170, border_radius=10)

        # Collectibles popups
        collectibles_popup = PopUp(390, 100, 500, 200, (200, 200, 200), color.white)
        collectibles_popup.add_button(-70, 60, 100, 40, shape='rect', color=(40, 209, 90), text="Collect",
                                      hover_color=(38 , 199, 85), text_color=(255, 255, 255), font_size=36, alpha=170, border_radius=10)
        collectibles_popup.add_button(70, 60, 100, 40, shape='rect', color=(255, 5, 21), text="Cancel",
                                      hover_color=(209 , 4, 14), text_color=(255, 255, 255), font_size=36, alpha=170, border_radius=10)

        # Game Complete Popups
        game_complete_popup = PopUp(390, 100, 500, 420, (200, 200, 200), color.white)
        game_complete_popup.set_title("Level Completed" if self.difficulty == 20 else ( "Game Completed" if self.level == 5 else "Question Answered correctly"), font_size=40, color=(0,0,255))
        game_complete_popup.set_message("You have completed the level." if self.difficulty == 20 else ( "You have completed the game" if self.level == 5 else "You have answered the question correctly"), spacing=100)
        game_complete_popup.set_message("Click 'New Level' to start a new level" if self.difficulty == 20 else ( "Click 'New Game' to start a new game" if self.level == 5 else "Click 'New Question' to start a new question"), spacing=30)
        game_complete_popup.set_message("or click 'Quit' to exit the Game", spacing=20 )
        game_complete_popup.add_button(-90, 150, 170, 40, shape='rect', color=(40, 209, 90), text="New Level" if self.difficulty == 20 else ( "New Game" if self.level == 5 else "New Question") ,
                                       hover_color=(38 , 199, 85), text_color=(255, 255, 255), font_size=36, alpha=170, border_radius=10)
        game_complete_popup.add_button(90, 150, 170, 40, shape='rect', color=(255, 5, 21), text="Quit",
                                       hover_color=(209 , 4, 14), text_color=(255, 255, 255), font_size=36, alpha=170, border_radius=10)


        # Add random numbers to solutions for variety
        all_possible_solutions.extend(random.randint(1, self.target_number) for _ in range(self.level))
        all_possible_solutions = list(filter(lambda x: x > 0, all_possible_solutions ))
        hud = HeadUpDisplay(self.target_number, self.game_question)

        # Maze dimensions
        rows = (SCREEN_HEIGHT - hud.height) // CELL_SIZE
        cols = SCREEN_WIDTH // CELL_SIZE

        # Initialize maze, player, and collectibles
        generated_maze = Maze(rows, cols)
        player = Player((1, 1))
        generated_maze.place_collectibles(len(all_possible_solutions), COLLECTABLE_IMAGEURL, None, all_possible_solutions)

        # Initialize enemies
        enemies = [Enemy(generated_maze, enemy_static.enemy_image_1, 4) for _ in range(self.enemies)]

        # Game variables
        running = True
        game_over_shown = False
        collectibles_popup_shown = False
        seen_collectibles = set()
        game_pause = True
        game_complete_shown = False
        game_question_popup_shown = True
        game_help_popup_shown = False

        # Track player's last position and popup state
        last_position = None
        active_collectible = None  # Currently active collectible for the popup

        start_time = pygame.time.get_ticks()

        while running:
            delta_time =  clock.tick(10) / 1000
            screen.fill(color.black)

            if not game_pause:
                elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Elapsed time in seconds
                hud.update_remainig_time(self.time_limit - elapsed_time)
            else:
                elapsed_time = 0

            if elapsed_time >= self.time_limit and not game_over_shown:
                game_over_popup.set_title("Time's Up!", font_size=40, font_style="bold", color=(255,0,0))
                game_over_popup.set_message("You ran out of time.", font_size=30, align="center", spacing=40)
                if len(self.collected_numbers) == 0:
                    game_over_popup.set_message("Please collect the numbers within the time", font_size=40, align="center", spacing=40)
                    game_over_popup.set_message("to pass the level", font_size=40, align="center", spacing=40)
                elif len(self.collected_numbers) == 1:
                    game_over_popup.set_message("You failed to get correct answer.", font_size=40, align="center", spacing=40)
                    game_over_popup.set_message("Correct answer would be :", font_size=30, align="center")
                    game_over_popup.set_message(get_solution(self.operator, self.collected_numbers, self.target_number, all_possible_solutions), font_size=30, align="center", spacing=50)

                game_over_popup.show()
                game_over_shown = True
                game_pause = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                hud_action = hud.handle_event(event)
                if hud_action == "pause":
                    game_pause = not game_pause
                    print('game_paused ',game_pause)
                elif hud_action == "help":
                    game_help_popup_shown = not game_help_popup_shown
                    print("show help popup") 

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if game_question_popup_shown:
                        for button in game_question_popup.buttons:
                            if button.is_clicked(mouse_pos):
                                if button.text == "Start":
                                    game_question_popup_shown = False
                                    game_pause = False
                                elif button.text == "Quit":
                                    running = False
                    elif game_over_shown:
                        for button in game_over_popup.buttons:
                            if button.is_clicked(mouse_pos):
                                if button.text == "Retry":
                                    return True
                                elif button.text == "Quit":
                                    running = False
                    elif game_complete_shown:
                        for button in game_complete_popup.buttons:
                            if button.is_clicked(mouse_pos):
                                if button.text == "New Level":
                                    return "New Level"
                                elif button.text == "New Question":
                                    return "New Question"
                                elif button.text == "Quit":
                                    running = False
                    elif game_help_popup_shown:
                        for button in help_popup.buttons:
                            if button.is_clicked(mouse_pos):
                                if button.text == "Close":
                                    game_help_popup_shown = not game_help_popup_shown

                    elif collectibles_popup_shown:
                        for button in collectibles_popup.buttons:
                            if button.is_clicked(mouse_pos):
                                game_pause = False
                                if button.text == "Collect" and active_collectible:
                                    self.collected_numbers.append(int(active_collectible.label))
                                    active_collectible.collect()  # Mark the collectible as collected
                                    generated_maze.remove_collectible_maze()
                                    seen_collectibles.add(active_collectible)  # Mark as seen and handled

                                    collectibles_popup_shown = False
                                    active_collectible = None  # Reset active collectible
                                elif button.text == "Cancel":
                                    collectibles_popup_shown = False
                                    active_collectible = None  # Reset active collectible
                                break

            if not game_pause:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    player.move(generated_maze, (-1, 0))
                if keys[pygame.K_DOWN]:
                    player.move(generated_maze, (1, 0))
                if keys[pygame.K_LEFT]:
                    player.move(generated_maze, (0, -1))
                if keys[pygame.K_RIGHT]:
                    player.move(generated_maze, (0, 1))

                # Check for collectible collision
                current_position = (player.row, player.col)
                if current_position != last_position:  # Player moved
                    collected_items = generated_maze.check_collectibles_collision(player)

                    # Handle collectible popup logic
                    if collected_items:
                        for item in collected_items:
                            if item not in seen_collectibles or item != active_collectible:
                                active_collectible = item
                                collectibles_popup.reset_messages()  #resetting array.may contains old collectiables messages
                                collectibles_popup.set_title("Collect Number ?")
                                collectibles_popup.set_message(f"You can collect {item.label}!")
                                collectibles_popup.show()
                                collectibles_popup_shown = True
                                game_pause = True
                                break

                    # Reset collectible state if player left the current collectible
                    if not collected_items:
                        active_collectible = None

                    last_position = current_position  # Update last position

                # Player-Enemy Collision
                if check_enemy_collision(player, enemies):
                    player.handle_collision(screen)
                    hud.update_health(player.health)
                    if player.health <= 0:
                        game_over_popup.set_message("You were killed by the monsters.", font_size=30, align="center")
                        game_over_popup.set_message("Please try to avoide the monsters.", font_size=30, align="center")
                        game_over_popup.set_message("Please click 'Retry' to try again or", font_size=30, align="center")
                        game_over_popup.set_message("'Quit' to quit the game", font_size=30, align="center")
                        game_over_popup.show()
                        game_over_shown = True
                        game_pause = True

                # Check if target is achieved
                if check_target_reached(self.collected_numbers, hud.target_number, self.operator) == True:
                    game_complete_popup.show()
                    game_complete_shown = True
                    game_pause = True
                elif check_target_reached(self.collected_numbers, hud.target_number, self.operator) == False and len(self.collected_numbers) == 2:
                    game_over_popup.set_message("You failed to answer the question correctly.", font_size=30, align="center")
                    game_over_popup.set_message("You picked the wrong numbers", font_size=30, align="center")
                    game_over_popup.set_message("Correct answer would be :", font_size=30, align="center")
                    game_over_popup.set_message(get_solution(self.operator, self.collected_numbers, self.target_number, all_possible_solutions))
                    game_over_popup.set_message("Please click 'Retry' to try again or", font_size=30, align="center",spacing=50)
                    game_over_popup.set_message("'Quit' to quit the game", font_size=30, align="center")
                    game_over_popup.show()
                    game_over_shown = True
                    game_pause = True                    

                # Move enemies
                for enemy in enemies:
                    enemy.move()
                hud.update_collectiables(self.collected_numbers)

            # Draw elements
            mouse_pos = pygame.mouse.get_pos()
            hud.update_hover(mouse_pos)
            hud.draw_header(screen)

            generated_maze.draw_maze(screen, top_wall, left_wall, right_wall, bottom_wall, top_left_wall, top_right_wall, bottom_left_wall, bottom_right_wall, inner_wall, path_image)
            player.draw(screen)
            for collectible in generated_maze.collectibles:
                collectible.update()  # Update particle system
                collectible.draw(screen)
            for enemy in enemies:
                enemy.draw(screen)

            # Display active popups
            if game_over_shown:
                mouse_pos = pygame.mouse.get_pos()
                game_over_popup.update(mouse_pos, delta_time)
                game_over_popup.draw(screen)

            if collectibles_popup_shown:
                mouse_pos = pygame.mouse.get_pos()
                collectibles_popup.update(mouse_pos, delta_time)
                collectibles_popup.draw(screen)

            if game_complete_shown:
                mouse_pos = pygame.mouse.get_pos()
                game_complete_popup.update(mouse_pos, delta_time)
                game_complete_popup.draw(screen)
            
            if game_question_popup_shown:
                mouse_pos = pygame.mouse.get_pos()
                game_question_popup.update(mouse_pos, delta_time)
                game_question_popup.draw(screen)
                game_question_popup.play_animation("addition", 0, 0, 500, 100)

               
            if game_help_popup_shown:
                mouse_pos = pygame.mouse.get_pos()
                help_popup.update(mouse_pos, delta_time)
                help_popup.draw(screen)


            pygame.display.flip()

        pygame.quit()
        return False

def check_enemy_collision(player, enemies):
    return any(player.row == enemy.row and player.col == enemy.col for enemy in enemies)

def check_target_reached(collected_numbers, target_number, operation):
    if operation == "+":
        if len(collected_numbers) > 0:
            total = sum(collected_numbers)
            return total == target_number
    if operation == "-":
        if len(collected_numbers) == 2:
            a = collected_numbers[0]
            b = collected_numbers[1]
            diff = 0
            if a > b:
                diff = a - b
            else:
                diff = b - a
            return target_number == diff
    if operation == "*":
        if len(collected_numbers) == 2:
            return target_number == (collected_numbers[0] * collected_numbers[1])
    if operation == "/":
        if len(collected_numbers) == 2:
            a = collected_numbers[0]
            b = collected_numbers[1]
            div = 0
            if a > b:
                div = a / b
            else:
                div = b / a
            return target_number == div 
    
    return -1

def get_question(operator):
    if operator == "+":
        return header_question.addition_question
    elif operator == "-":
        return header_question.subtraction_question
    elif operator == "*":
        return header_question.multiplication_question
    elif operator == "/":
        return header_question.division_question
    else:
        return '' 

def game_over_help_text(timeout, zero_health):
    helptextmessage = []
    if timeout:
        helptextmessage.append("Please try to complete the game on time.")
    if zero_health:
        helptextmessage.append("You were killed by the monsters.")
        helptextmessage.append("While collecting the numbers please try to avoide the monsters.")
    return helptextmessage

def get_solution(operator, collected_numbers, target_number, all_possible_solutions):
    len_collected_numbers = len(collected_numbers)
    expression = ''
    if len_collected_numbers == 0:
        if operator == "+":
            expression = "Please collect two numbers whose sum is "+str(target_number)
        elif operator == "-":
            expression = "Please collect two numbers whose difference is "+str(target_number)
        elif operator == "*":
            expression = "Please collect two numbers whose product is "+str(target_number)
        elif operator == "/": 
            expression = "Please collect two numbers whose division is "+str(target_number)
    
    if len_collected_numbers == 1:
        if operator == "+":
            a = collected_numbers[0]
            for i in collected_numbers:
                if i == target_number - a and not i == a:
                    expression = f' {a} + {i} = {target_number}' 
        elif operator == "-":
            a = collected_numbers[0]
            for i in collected_numbers:
                if i == target_number - a and not i == a:
                    if( i > a):
                        expression = f' {i} - {a} = {target_number}' 
                    else:
                        expression = f' {a} - {i} = {target_number}' 
        elif operator == "*":
            a = collected_numbers[0]
            for i in collected_numbers:
                if i == target_number // a and not i == a:
                    expression = f' {a} * {i} = {target_number}'
        elif operator == "/": 
            a = collected_numbers[0]
            for i in collected_numbers:
                if i == target_number * a and not i == a:
                    expression = f' {a} / {i} = {target_number}'
    
    if len_collected_numbers == 2:
        solutions = []
        expressions = []
        if operator == "+":
            for i in range(target_number + 1):
                result = target_number - i
                solutions.append((result, i))
        elif operator == "-":
            for i in range(1, target_number + 10):
                result = target_number - i
                solutions.append((result, i))
        elif operator == "*":
            for i in range(1, int(target_number**0.5) + 1):
                if target_number % i == 0:
                    solutions.append((target_number // i, i))
        elif operator == "/": 
            for i in range(1, target_number + 1):
                if target_number % i == 0:
                    solutions.append((target_number / i, i))

        for sol in solutions:
            if sol[0] in collected_numbers or sol[1] in collected_numbers:
                expression = f'{sol[0]} {operator} {sol[1]} = {target_number}'
            else:
                expression = f'{sol[0]} {operator} {sol[1]} = {target_number}'
    return expression
