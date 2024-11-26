import pygame
import charactersTest
import enemiesTest

pygame.init()

screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Character-Enemy Collision Test")

clock = pygame.time.Clock()

character = charactersTest.baseCharacterClass()
enemy = enemiesTest.Enemy1(600, 600)

characterGroup = pygame.sprite.Group()
characterGroup.add(character)

enemyGroup = pygame.sprite.Group()
enemyGroup.add(enemy)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    character.update(enemyGroup, enemyGroup)
    enemy.update(characterGroup)

    characterGroup.draw(screen)
    enemyGroup.draw(screen)

    if character.hasTakenDamage == True:
        print("Damage Taken Detected!")
        running = False

    pygame.display.flip()

    clock.tick(60)

pygame.quit()