import pygame
import time

class health(pygame.sprite.Sprite):
    def __init__(self, total_health):
        super().__init__()
        self.image = pygame.image.load("data\\images\\player_character\\heart.png")
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.health = total_health
        self.hearts = [self.image, self.image, self.image]

    def take_damage(self):
        self.health -= 1
    
    def isDead(self):
        return self.health == 0

    def draw(self, screen):
        space = 10
        for heart in self.hearts:
            screen.blit(heart, (880 + space, 30))
            space += 30

    
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
        self.invincibleDuration = 3
        self.invincibilityStartTime = 0
        
        self.hasCollided = False
        self.hasTakenDamage = False
        self.hasDied = False

    def update(self, enemies, wall):
        self.moveRight()
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
            self.invincibilityStartTime = time.time()
            self.hasCollided = True
            if len(self.health.hearts) > 0:
                self.hasTakenDamage = True
                self.health.hearts.pop()

        
        if pygame.sprite.spritecollide(self, wall, dokill = False):
            self.rect.topleft = original_position

        if self.health.isDead():
            self.kill()
        
        self.updateVisibility()
        

        self.updateInvincibility()

    def isInvincible(self):
        return self.invincible
    
    def updateInvincibility(self):
        if self.isInvincible() and time.time() - self.invincibilityStartTime > self.invincibleDuration:
            self.invincible = False 
    
    def updateVisibility(self):
        elapsed = time.time() - self.invincibilityStartTime
        if self.invincible and int(elapsed * 5) % 2 == 0:
            self.image.set_alpha(128)

        else:
            self.image.set_alpha(255)
    
    def collision(self):
        return self.hasCollided
    
    def moveRight(self):
        self.rect.x += self.speed