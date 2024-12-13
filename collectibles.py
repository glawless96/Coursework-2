import pygame
import random
from static import ColorData, MazeData, HeaderData
from particle import ParticleSystem

maze_static = MazeData()
color = ColorData()
header_static = HeaderData()

CELL_SIZE = maze_static.cell_size

class Collectible:
    def __init__(self, x, y, image_paths, animation_paths=None, label="Collect Me"):
        self.x = x
        self.y = y + header_static.height
        self.image_paths = image_paths
        self.images = [pygame.image.load(image).convert_alpha() for image in image_paths]
        self.images = [pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE)) for img in self.images]
        self.current_image = 0  # Start with the first image
        self.rect = self.images[0].get_rect(topleft=(self.x, self.y))

        self.animation_paths = animation_paths or []
        self.animation_frames = [pygame.image.load(image).convert_alpha() for image in animation_paths] if animation_paths else []
        self.animation_frame = 0  # For the animation
        self.is_collected = False

        # Add text label
        self.label = label
        self.font = pygame.font.Font(None, 30)  # Adjust font size as necessary
        self.text_surface = self.font.render(self.label, True, (0, 0, 0))

        self.offset = header_static.height

        # Particle system for visual effects
        self.particle_system = ParticleSystem()

    def draw(self, screen):
        # Draw particles if they are active
        self.particle_system.draw(screen)

        if self.is_collected:
            if self.animation_frame < len(self.animation_frames):
                screen.blit(self.animation_frames[self.animation_frame], (self.x, self.y))
                self.animation_frame += 1
            else:
                self.is_collected = False  # Stop animation when done
        else:
            # Draw image of the collectible
            scaled_image = pygame.transform.scale(self.images[self.current_image], (CELL_SIZE, CELL_SIZE))
            screen.blit(scaled_image, (self.x, self.y))

            # Draw the text label
            text_rect = self.text_surface.get_rect(center=(self.x + CELL_SIZE // 2, self.y + CELL_SIZE // 2))
            screen.blit(self.text_surface, text_rect)

    def collect(self):
        self.is_collected = True
        self.animation_frame = 0

        # Trigger particle emission at the collectible's position
        self.particle_system.emit(
            x=self.x + CELL_SIZE // 2,
            y=self.y + CELL_SIZE // 2,
            color=(255, 215, 0),  # Golden yellow color
            count=20,
            size_range=(2, 6),
            lifespan_range=(20, 50)
        )

    def is_colliding(self, player):
        player_rect = pygame.Rect(player.col * CELL_SIZE, player.row * CELL_SIZE + self.offset, CELL_SIZE, CELL_SIZE)
        return self.rect.colliderect(player_rect)

    def update(self):
        # Update particles every frame
        self.particle_system.update()

