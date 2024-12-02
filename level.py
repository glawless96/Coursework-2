import pygame
import random
from maze import Maze
from player import Player
from enemy import Enemy
from collectibles import Collectible
from static import MazeData, ScreenData, CharacterData, ColorData, EnemyData
from head_up_display import HeadUpDisplay
from popup import PopUp

# Static configurations
static_maze = MazeData()
color = ColorData()
main_screen = ScreenData()
char_image = CharacterData()
enemy_static = EnemyData()

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
    def __init__(self, current_level, number_of_enemies):
        self.level = current_level
        self.enemies = number_of_enemies
        self.collected_numbers = []

    def load_image(self, path, size=None, alpha=False):
        """Load an image with optional scaling."""
        try:
            image = pygame.image.load(path).convert_alpha() if alpha else pygame.image.load(path).convert()
            if size:
                image = pygame.transform.scale(image, size)
            return image
        except pygame.error as e:
            print(f"Error loading image at {path}: {e}")
            return None

    def start_level(self, screen):
        # Load images with proper error handling
        wall_image = self.load_image(MAZE_WALL_IMAGEURL, (CELL_SIZE, CELL_SIZE))
        path_image = self.load_image(MAZE_PATH_IMAGEURL, (CELL_SIZE, CELL_SIZE))
        player_image = self.load_image(PLAYER_IMAGEURL, (CELL_SIZE, CELL_SIZE), alpha=True)
        end_image = self.load_image(MAZE_END_IMAGEURL, (CELL_SIZE, CELL_SIZE))
        
        # Initialize popups
        #game over popup
        game_over_popup = PopUp(390, 100, 500, 420, (200, 200, 200), (0, 0, 0))
        game_over_popup.set_message("Game Over! You ran out of health.")
        game_over_popup.add_button(-70, 60, 100, 40, shape = 'rect', color=(40, 209, 90), text="Retry",
                                       hover_color = (38 , 199, 85), text_color=(255, 255, 255), font_size=36, alpha = 170, border_radius = 10 )
        game_over_popup.add_button(70, 60, 100, 40, shape = 'rect', color=(255, 5, 21), text="Quit",
                                        hover_color = (209 , 4, 14), text_color=(255, 255, 255), font_size=36, alpha = 170, border_radius = 10)

        #Collectibles popups
        collectibles_popup = PopUp(390, 100, 500, 200, (200, 200, 200), (0, 0, 0))
        collectibles_popup.add_button(-70, 60, 100, 40, shape = 'rect', color=(40, 209, 90), text="Collect",
                                       hover_color = (38 , 199, 85), text_color=(255, 255, 255), font_size=36, alpha = 170, border_radius = 10 )
        collectibles_popup.add_button(70, 60, 100, 40, shape = 'rect', color=(255, 5, 21), text="Cancel",
                                        hover_color = (209 , 4, 14), text_color=(255, 255, 255), font_size=36, alpha = 170, border_radius = 10)

        #Game Complete Popups
        game_complete_popup = PopUp(390, 100, 500, 420, (200, 200, 200), (0, 0, 0))
        game_complete_popup.set_message("You have complete the level !!!")
        game_complete_popup.add_button(-70, 60, 100, 40, shape = 'rect', color=(40, 209, 90), text="Next Level",
                                       hover_color = (38 , 199, 85), text_color=(255, 255, 255), font_size=36, alpha = 170, border_radius = 10 )
        game_complete_popup.add_button(70, 60, 100, 40, shape = 'rect', color=(255, 5, 21), text="Quit",
                                        hover_color = (209 , 4, 14), text_color=(255, 255, 255), font_size=36, alpha = 170, border_radius = 10)

        # Generate random target number
        target_number = Collectible.generate_target_number(self.level)
        all_possible_solutions = Collectible.get_addition_solutions_set(target_number)
        print('Target Number:', target_number)
        print('Possible Solutions:', all_possible_solutions)

        #Question popup
        game_question_popup = PopUp(390, 100, 500, 420, (200, 200, 200), (0, 0, 0))
        game_question_popup.set_message("Get all numbers that adds up to : "+str(target_number))
        game_question_popup.add_button(-70, 60, 100, 40, shape = 'rect', color=(40, 209, 90), text="Start",
                                       hover_color = (38 , 199, 85), text_color=(255, 255, 255), font_size=36, alpha = 170, border_radius = 10 )
        game_question_popup.add_button(70, 60, 100, 40, shape = 'rect', color=(255, 5, 21), text="Quit",
                                        hover_color = (209 , 4, 14), text_color=(255, 255, 255), font_size=36, alpha = 170, border_radius = 10)
        game_question_popup.show()

        # Add random numbers to solutions for variety
        all_possible_solutions.extend(random.randint(1, target_number) for _ in range(self.level))

        hud = HeadUpDisplay(target_number)

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

        # Track player's last position and popup state
        last_position = None
        active_collectible = None  # Currently active collectible for the popup

        while running:
            delta_time =  clock.tick(10) / 1000
            screen.fill(color.black)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
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
                                if button.text == "Next Level":
                                    return "Next Level"
                                elif button.text == "Quit":
                                    running = False
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
                                collectibles_popup.set_message(f"You can collect {item.label}! Collect or Cancel?")
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
                        game_over_popup.show()
                        game_over_shown = True
                        game_pause = True

                #Check if target is achieved
                if check_target_reached(self.collected_numbers, hud.target_number, "+"):
                    game_complete_popup.show()
                    game_complete_shown = True
                    game_pause = True

                # Move enemies
                for enemy in enemies:
                    enemy.move()
                hud.update_collectiables(collected_items) 

            # Draw elements
            hud.draw_header(screen)
            generated_maze.draw_maze(screen, wall_image, path_image, end_image)
            player.draw(screen)
            for collectible in generated_maze.collectibles:
                collectible.draw(screen)
            for enemy in enemies:
                enemy.draw(screen)

            # Display active popups
            if game_over_shown:
                mouse_pos = pygame.mouse.get_pos()
                game_over_popup.update(mouse_pos, delta_time )
                game_over_popup.draw(screen)

            if collectibles_popup_shown:
                mouse_pos = pygame.mouse.get_pos()
                collectibles_popup.update(mouse_pos, delta_time )
                collectibles_popup.draw(screen)

            if game_complete_shown:
                mouse_pos = pygame.mouse.get_pos()
                game_complete_popup.update(mouse_pos, delta_time )
                game_complete_popup.draw(screen)
            
            if game_question_popup_shown:
                mouse_pos = pygame.mouse.get_pos()
                game_question_popup.update(mouse_pos, delta_time )
                game_question_popup.draw(screen)

            pygame.display.flip()
          

        pygame.quit()
        return False

def check_enemy_collision(player, enemies):
    return any(player.row == enemy.row and player.col == enemy.col for enemy in enemies)

def check_target_reached(collected_numbers, target_number, opeartion):
    if opeartion == "+":
        if len(collected_numbers) > 0:
            total = sum(collected_numbers)
            return total == target_number