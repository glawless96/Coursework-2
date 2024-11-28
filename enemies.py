import pygame

class Enemy1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("data\\images\\monsters\\1_en.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
        self.velocity = pygame.math.Vector2(1, 0)

    def update(self, wall):
        original_position = self.rect.topleft
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        if pygame.sprite.spritecollide(self, wall, dokill = False):
            self.velocity.x *= -1
            self.rect.topleft = original_position


class Enemy2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("data\\images\\monsters\\1_en.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
        self.velocity = pygame.math.Vector2(0, 2)

    def update(self, wall):
        original_position = self.rect.topleft
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        if pygame.sprite.spritecollide(self, wall, dokill = False):
            self.velocity.y *= -1
            self.rect.topleft = original_position