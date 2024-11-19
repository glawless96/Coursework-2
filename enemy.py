import pygame
import random

from static import MazeData

maze_static = MazeData()

CELL_SIZE = maze_static.cell_size

class Enemy:
    def __init__(self, maze, image_path, speed):
        #load enemy Images , animations, transform to fit
        self.images = [pygame.image.load(image_path).convert_alpha()]  # Add more frames for animations
        self.images = [pygame.transform.scale(img ,(CELL_SIZE,CELL_SIZE)) for img in self.images]
        self.current_frame = 0
        self.image = self.images[self.current_frame]
        
        #Initilize enemy position
        self.row, self.col = self.get_random_position(maze)
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        self.current_direction = random.choice(self.directions)

        # Speed properties
        self.speed = speed  # Speed: moves every `speed` frames
        self.move_counter = 0
        self.maze = maze

    def get_random_position(self, maze):
        while True: # Loop and place the enemy on the first path element
            row = random.randint(0, len(maze.layout) - 1)
            col = random.randint(0, len(maze.layout[0]) - 1)
            if maze.layout[row][col] == 0: # place on paths
                return row, col

    def is_valid_move(self, new_row, new_col):
        return 0 <= new_row < len(self.maze.layout) and 0 <= new_col < len(self.maze.layout[0]) and self.maze.layout[new_row][new_col] == 0

    def move(self):
        self.move_counter += 1
        if self.move_counter >= self.speed:
            self.move_counter = 0  # Reset the counter

            # Attempt to move in the current direction
            dr, dc = self.current_direction
            new_row, new_col = self.row + dr, self.col + dc

            if self.is_valid_move(new_row, new_col):
                # Continue moving in the current direction
                self.row, self.col = new_row, new_col
            else:
                # Hit a wall, pick a new valid random direction
                valid_directions = [
                    (dr, dc) for dr, dc in self.directions 
                    if self.is_valid_move(self.row + dr, self.col + dc)
                ]
                if valid_directions:
                    self.current_direction = random.choice(valid_directions)
                    dr, dc = self.current_direction
                    self.row, self.col = self.row + dr, self.col + dc

    def draw(self, screen):
        x, y = self.col * CELL_SIZE, self.row * CELL_SIZE
        screen.blit(self.image, (x, y))
