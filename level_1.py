import pygame
import maze
import collectibles

# Screen dimensions and properties
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

clock = pygame.time.Clock()
MAZE_WALL_IMAGEURL = 'data\\images\\maze\\maze_wall.png'
MAZE_PATH_IMAGEURL = 'data\\images\\maze\\path2.png'
PLAYER_IMAGEURL = 'data\\images\\player_character\\player_character.png'
COLLECTABLE_IMAGEURL = 'data\\images\\collectables\\collectable_1.png'

def start_level_1(screen):
    # Load images
    wall_image = pygame.image.load(MAZE_WALL_IMAGEURL).convert()
    wall_image = pygame.transform.scale(wall_image, (CELL_SIZE, CELL_SIZE))

    path_image = pygame.image.load(MAZE_PATH_IMAGEURL).convert()
    path_image = pygame.transform.scale(path_image, (CELL_SIZE, CELL_SIZE))

    player_image = pygame.image.load(PLAYER_IMAGEURL).convert_alpha()
    player_image = pygame.transform.scale(player_image, (CELL_SIZE, CELL_SIZE))

    collectible_images = []
    for i in range(1, 6):
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
        screen.fill(BLACK)

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

        maze.draw_maze(screen, generated_maze, wall_image, path_image, CELL_SIZE, BLACK)
        collectibles.draw_collectibles(screen, generated_collectibles, CELL_SIZE)
        screen.blit(player_image, (player_x * CELL_SIZE, player_y * CELL_SIZE))

        # Check for collision with collectibles
        new_collectibles_pos = []
        for x, y, image, number in generated_collectibles:
            if (player_x, player_y) == (x, y):
                print(f'Collected item at ({x}, {y}) with number {number}!')
            else:
                new_collectibles_pos.append((x, y, image, number))
        generated_collectibles = new_collectibles_pos
            

        pygame.display.flip()
        clock.tick(10) 
    # Quit Pygame
    pygame.quit()
