import random
import pygame

from static import MazeData
from collectibles import Collectible

maze_static = MazeData()

CELL_SIZE = maze_static.cell_size

class Maze():
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.layout = self.generate_maze()
        self.collectibles = []
    
    def generate_maze(self):
        maze = [[1 for _ in range(self.cols)] for _ in range(self.rows)]  # 1 means wall, 0 means path

        def dfs(x, y):
            maze[y][x] = 0  # Mark the current cell as path
            directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            random.shuffle(directions)

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 1 <= nx < self.cols - 1 and 1 <= ny < self.rows - 1 and maze[ny][nx] == 1:
                    maze[ny][nx] = 0
                    maze[y + dy // 2][x + dx // 2] = 0  # Clear the wall between cells
                    dfs(nx, ny)

        # Generate the maze using DFS
        dfs(1, 1)

        # Add additional random paths to create more openings
        extra_paths = (self.rows * self.cols) // 10  # Adjust this value to control the number of additional paths
        for _ in range(extra_paths):
            x = random.randint(1, self.cols - 2)
            y = random.randint(1, self.rows - 2)
            if maze[y][x] == 1:  # Only add a path where there's currently a wall
                maze[y][x] = 0

        return maze

    def place_collectibles(self, num_collectibles, collectible_image,  animation_paths, labels):
        self.collectibles.clear()
        for i in range(num_collectibles):
            while True:
                r = random.randint(1, self.rows - 2)
                c = random.randint(1, self.cols - 2)
                if self.layout[r][c] == 0:  # Only place on a path
                    collectible = Collectible(c * CELL_SIZE, r * CELL_SIZE, [collectible_image],  animation_paths, str(labels[i]))
                    self.collectibles.append(collectible)
                    break
    
    def draw_maze(self, screen, wall_image, path_image, end_image):
        rows, cols = self.rows, self.cols
        for row in range(self.rows):
            for col in range(self.cols): 
                if (col, row) == (cols - 3, rows - 3):
                    # Draw the end image at this cell
                    screen.blit(end_image, (col * CELL_SIZE, row * CELL_SIZE))
                else:
                    # Draw wall or path based on maze structure
                    if self.layout[row][col] == 1:
                        screen.blit(wall_image, (col * CELL_SIZE, row * CELL_SIZE))
                    else:
                        screen.blit(path_image, (col * CELL_SIZE, row * CELL_SIZE))
        

    def check_collectibles_collision(self, player):
        collected_items = []
        for collectible in self.collectibles:
            if collectible.is_colliding(player):
                collected_items.append(collectible)
                self.collectibles.remove(collectible)
        return collected_items

def check_for_end_collision(player_x, player_y, end_x, end_y):
    if(player_x, player_y) == (end_x, end_y):
        return 'questionnaire'
