import pygame
import maze
import collectibles
import maze_completion

from static import Maze, Screen, Character, Color

static_maze = Maze()
color = Color()
main_screen = Screen()
char_image = Character()

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


    #Generate Random Target Number
    target_number = collectibles.generate_target_number(1)
    all_possible_solutions_set = collectibles.get_addition_solutions_set(target_number)
    print('target number ',target_number)
    print('all_possible_solutions ',all_possible_solutions_set)
    collectible_images = []
    
    for i in range(1, len(all_possible_solutions_set) + 10, 1):
        image = pygame.image.load(COLLECTABLE_IMAGEURL).convert_alpha()
        image = pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))
        collectible_images.append(image)

    # Generate maze and collectibles
    rows = SCREEN_HEIGHT // CELL_SIZE
    cols = SCREEN_WIDTH // CELL_SIZE
    generated_maze = maze.generate_maze(rows, cols)
    generated_collectibles = collectibles.place_images_randomly(generated_maze, collectible_images, CELL_SIZE)

    # Player properties
    player_x, player_y = 1, 1

    # Main game loop
    running = True

    while running:
        screen.fill(color.black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Check for key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and generated_maze[player_y - 1][player_x] == 0:
            player_y -= 1
        if keys[pygame.K_DOWN] and generated_maze[player_y + 1][player_x] == 0:
            player_y += 1
        if keys[pygame.K_LEFT] and generated_maze[player_y][player_x - 1] == 0:
            player_x -= 1
        if keys[pygame.K_RIGHT] and generated_maze[player_y][player_x + 1] == 0:
            player_x += 1

        maze.draw_maze(screen, generated_maze, wall_image, path_image, end_image, CELL_SIZE, color.black)
        collectibles.draw_collectibles(screen, generated_collectibles, CELL_SIZE)
        screen.blit(player_image, (player_x * CELL_SIZE, player_y * CELL_SIZE))

        # Check for collision with collectibles
        new_collectibles_pos = []
        for x, y, image, number in generated_collectibles:
            if (player_x, player_y) == (x, y):
                collected_numbers.append(number)
                print(f'Collected item at ({x}, {y}) with number {number}!')
            else:
                new_collectibles_pos.append((x, y, image, number))
        generated_collectibles = new_collectibles_pos
            
        endcollision = maze.check_for_end_collision(player_x, player_y, cols - 3, rows - 3)
        if endcollision == 'questionnaire':
            maze_completion.question_screen(screen, collected_numbers)
            return 

        pygame.display.flip()
        clock.tick(10) 
    # Quit Pygame
    pygame.quit()
