import random
import pygame

CELL_SIZE = 25

def generate_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]  # 1 means wall, 0 means path

    def dfs(x, y):
        maze[y][x] = 0  # Mark the current cell as path
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < cols - 1 and 1 <= ny < rows - 1 and maze[ny][nx] == 1:
                maze[ny][nx] = 0
                maze[y + dy // 2][x + dx // 2] = 0  # Clear the wall between cells
                dfs(nx, ny)

    dfs(1, 1)
    return maze

def draw_maze(screen, maze, wall_image, path_image, end_image, cell_size, color):
    rows, cols = len(maze), len(maze[0])
    for y in range(len(maze)):
        for x in range(len(maze[0])): 
            if (x, y) == (cols - 3, rows - 3):
                # Draw the end image at this cell
                screen.blit(end_image, (x * cell_size, y * cell_size))
            else:
                # Draw wall or path based on maze structure
                if maze[y][x] == 1:
                    screen.blit(wall_image, (x * cell_size, y * cell_size))
                else:
                    screen.blit(path_image, (x * cell_size, y * cell_size))

def check_for_end_collision(player_x, player_y, end_x, end_y):
    if(player_x, player_y) == (end_x, end_y):
        return 'questionnaire'