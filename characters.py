import pygame
import time

class health(pygame.sprite.Sprite):
    def __init__(self, total_health):
        super().__init__()
        self.image = pygame.image.load("data\\images\\player_character\\player_character.png")
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.health = total_health

    def take_damage(self):
        self.health -= 1
    
    def isDead(self):
        return self.health == 0



class baseCharacterClass(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("data\\images\\player_character\\player_character.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (49, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (50, 550)

        self.health = health(3)
        self.speed = 4
        
        self.invincible = False
        self.invincible_duration = 3
        self.invincibility_start_time = 0

    def update(self, enemies, wall):
        original_position = self.rect.topleft
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if keys[pygame.K_UP]:
            self.rect.y -= self.speed

        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        

        if not self.isInvincible() and pygame.sprite.spritecollide(self, enemies, dokill = False):
            self.rect.topleft = original_position
            self.health.take_damage()
            self.invincible = True
            self.invincibility_start_time = time.time()

        
        if pygame.sprite.spritecollide(self, wall, dokill = False):
            self.rect.topleft = original_position

        if self.health.isDead():
            self.kill()
        
        self.updateVisibility()
        

        self.updateInvincibility()

    def isInvincible(self):
        return self.invincible
    
    def updateInvincibility(self):
        if self.isInvincible() and time.time() - self.invincibility_start_time > self.invincible_duration:
            self.invincible = False 
    
    def updateVisibility(self):
        elapsed = time.time() - self.invincibility_start_time
        if self.invincible and int(elapsed * 5) % 2 == 0:
            self.image.set_alpha(128)

        else:
            self.image.set_alpha(255)