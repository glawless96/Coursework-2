import random
import pygame

from static import MazeData, HeaderData
from collectibles import Collectible

maze_static = MazeData()
header_static = HeaderData()

CELL_SIZE = maze_static.cell_size

class Maze():
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.layout = self.generate_maze()
        self.collectibles = []
        self.offset = header_static.height
    
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
        extra_paths = (self.rows * self.cols) // 2  # Adjust this value to control the number of additional paths
        for _ in range(extra_paths):
            x = random.randint(1, self.cols - 2)
            y = random.randint(1, self.rows - 2)
            if maze[y][x] == 1:  # Only add a path where there's currently a wall
                maze[y][x] = 0

        return maze

    def place_collectibles(self, num_collectibles, collectible_image, animation_paths, labels):
        self.collectibles.clear()
        occupied_positions = set()  # Track occupied positions

        for i in range(num_collectibles):
            while True:
                r = random.randint(1, self.rows - 2)
                c = random.randint(1, self.cols - 2)
                position = (r, c)

                if self.layout[r][c] == 0 and position not in occupied_positions:  # Ensure no overlap
                    collectible = Collectible(
                        c * CELL_SIZE, r * CELL_SIZE, [collectible_image], animation_paths, str(labels[i])
                    )
                    self.collectibles.append(collectible)
                    occupied_positions.add(position)  # Mark position as occupied
                    break

    
    # def draw_maze(self, screen, wall_image, path_image, end_image):
    #     rows, cols = self.rows, self.cols
    #     for row in range(self.rows):
    #         for col in range(self.cols): 
    #             if self.layout[row][col] == 1:
    #                 screen.blit(wall_image, (col * CELL_SIZE, row * CELL_SIZE + self.offset))
    #             else:
    #                 screen.blit(path_image, (col * CELL_SIZE, row * CELL_SIZE + self.offset))
    def draw_maze(self, screen, top_wall_image, left_wall_image, right_wall_image, bottom_wall_image, top_left_corner_image, top_right_corner_image, bottom_left_corner_image, bottom_right_corner_image, inner_wall_image, path_image):
        rows, cols = self.rows, self.cols
        for row in range(rows):
            for col in range(cols):
                if self.layout[row][col] == 1:  # If it's a wall
                    # Determine the position of the wall
                    if row == 0 and col == 0:  # Top-left corner
                        screen.blit(top_left_corner_image, (col * CELL_SIZE, row * CELL_SIZE + self.offset))
                    elif row == 0 and col == cols - 1:  # Top-right corner
                        screen.blit(top_right_corner_image, (col * CELL_SIZE, row * CELL_SIZE + self.offset))
                    elif row == rows - 1 and col == 0:  # Bottom-left corner
                        screen.blit(bottom_left_corner_image, (col * CELL_SIZE, row * CELL_SIZE + self.offset))
                    elif row == rows - 1 and col == cols - 1:  # Bottom-right corner
                        screen.blit(bottom_right_corner_image, (col * CELL_SIZE, row * CELL_SIZE + self.offset))
                    elif row == 0:  # Top wall
                        screen.blit(top_wall_image, (col * CELL_SIZE, row * CELL_SIZE + self.offset))
                    elif row == rows - 1:  # Bottom wall
                        screen.blit(bottom_wall_image, (col * CELL_SIZE, row * CELL_SIZE + self.offset))
                    elif col == 0:  # Left wall
                        screen.blit(left_wall_image, (col * CELL_SIZE, row * CELL_SIZE + self.offset))
                    elif col == cols - 1:  # Right wall
                        screen.blit(right_wall_image, (col * CELL_SIZE, row * CELL_SIZE + self.offset))
                    else:  # Inner walls
                        screen.blit(inner_wall_image, (col * CELL_SIZE, row * CELL_SIZE + self.offset))
                else:
                    # Draw the path image
                    screen.blit(path_image, (col * CELL_SIZE, row * CELL_SIZE + self.offset))
    

    def check_collectibles_collision(self, player):
        collected_items = []
        for collectible in self.collectibles: #Iterate over all collectaibles
            if collectible.is_colliding(player): # checking if layer collides with the collectibles
                collected_items.append(collectible) 
                #self.collectibles.remove(collectible)
        return collected_items
    
    def remove_collectible_maze(self):
        for collectible in self.collectibles:
            if collectible.is_collected:
                self.collectibles.remove(collectible)
