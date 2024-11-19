import pygame
import random

from maze import Maze
from player import Player
from enemy import Enemy
from collectibles import Collectible
from static import MazeData, ScreenData, CharacterData, ColorData, EnemyData

static_maze = MazeData()
color = ColorData()
main_screen = ScreenData()
char_image = CharacterData()
enemy_static = EnemyData()

# Screen dimensions and properties
SCREEN_WIDTH = main_screen.width
SCREEN_HEIGHT = main_screen.height
CELL_SIZE = static_maze.cell_size

MAZE_WALL_IMAGEURL = static_maze.wall_image #'data\\images\\maze\\maze_wall.png'
MAZE_PATH_IMAGEURL = static_maze.path_image #'data\\images\\maze\\path2.png'
MAZE_END_IMAGEURL = static_maze.end_maze_image #'data\\images\\maze\\portal.png'
PLAYER_IMAGEURL = char_image.front_image
COLLECTABLE_IMAGEURL = 'data\\images\\collectables\\collectable_2.png'

clock = pygame.time.Clock()

collected_numbers = []

def start_level_1(screen):

    # Load images
    wall_image = pygame.image.load(MAZE_WALL_IMAGEURL).convert()
    wall_image = pygame.transform.scale(wall_image, (CELL_SIZE, CELL_SIZE))

    path_image = pygame.image.load(MAZE_PATH_IMAGEURL).convert()
    path_image = pygame.transform.scale(path_image, (CELL_SIZE, CELL_SIZE))

    player_image = pygame.image.load(PLAYER_IMAGEURL).convert_alpha()
    player_image = pygame.transform.scale(player_image, (CELL_SIZE, CELL_SIZE))

    end_image = pygame.image.load(MAZE_END_IMAGEURL)
    end_image = pygame.transform.scale(end_image, (CELL_SIZE, CELL_SIZE))

    #maze Rows and cols
    rows = SCREEN_HEIGHT // CELL_SIZE
    cols = SCREEN_WIDTH // CELL_SIZE

    #Generate Random Target Number
    target_number = Collectible.generate_target_number(1)
    all_possible_solutions = Collectible.get_addition_solutions_set(target_number)
    print('target number ',target_number)
    print('all_possible_solutions ',all_possible_solutions)

    for i in range(0, 10):
        all_possible_solutions.append(random.randint(1, 100))

    #generate Maze
    generated_maze = Maze(rows, cols)

    #Initilize player
    player = Player((1,1))

    #Initilize Collectiables
    generated_maze.place_collectibles(len(all_possible_solutions), COLLECTABLE_IMAGEURL, None ,all_possible_solutions)

    #Initilize enemies
    enemies = []
    for i in range(0,6):
        enemies.append(Enemy(generated_maze, enemy_static.enemy_image_1, 2))

    running = True

    while running:
        screen.fill(color.black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.move(generated_maze, (-1, 0))
        if keys[pygame.K_DOWN]:
           player.move(generated_maze, (1, 0))
        if keys[pygame.K_LEFT]:
            player.move(generated_maze, (0, -1))
        if keys[pygame.K_RIGHT]:
           player.move(generated_maze, (0, 1))

        #check for player and collectiable collision
        collected_items = generated_maze.check_collectibles_collision(player)
        for item in collected_items:
            player.collect([item])


        #Player Enemy Collision    
        if check_enemy_collision(player, enemies):
            player.handle_collision(screen)

            if player.health <= 0:
                lose_text = pygame.font.Font(None, 36).render("Game Over! You ran out of health.", True, (255, 0, 0))
                screen.blit(lose_text, (SCREEN_WIDTH // 2 - lose_text.get_width() // 2, SCREEN_HEIGHT // 2))
                pygame.display.flip()
                pygame.time.delay(3000)

                running = False

        generated_maze.draw_maze(screen, wall_image, path_image, end_image)
        player.draw(screen)

        for collectible in generated_maze.collectibles:
            collectible.draw(screen)

        player.draw_health(screen)

        #Enemy movement
        for enemy in enemies:
            enemy.move()
            enemy.draw(screen)

        pygame.display.flip()
        clock.tick(10)

    # Quit Pygame
    pygame.quit()


def check_enemy_collision(player, enemies):
    for enemy in enemies:
        if player.row == enemy.row and player.col == enemy.col:
            return True
    return False