import pygame
import random

class Particle:
    def __init__(self, x, y, color, size, lifespan, dx=None, dy=None):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.lifespan = lifespan  # Number of frames before disappearing
        self.dx = dx if dx is not None else random.uniform(-1, 1)
        self.dy = dy if dy is not None else random.uniform(-1, 1)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.lifespan -= 1

    def draw(self, screen):
        if self.lifespan > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, color, count=10, size_range=(2, 5), lifespan_range=(20, 50)):
        for _ in range(count):
            size = random.randint(*size_range)
            lifespan = random.randint(*lifespan_range)
            particle = Particle(
                x=x,
                y=y,
                color=color,
                size=size,
                lifespan=lifespan
            )
            self.particles.append(particle)

    def update(self):
        for particle in self.particles:
            particle.update()
        self.particles = [p for p in self.particles if p.lifespan > 0]

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)

