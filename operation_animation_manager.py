import pygame
import time

class AnimationManager:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)

    def play(self, screen, animation_type, popup_rect):
        if animation_type == "addition":
            self.addition_animation(screen, popup_rect)
        elif animation_type == "subtraction":
            self.subtraction_animation(screen, popup_rect)
        elif animation_type == "multiplication":
            self.multiplication_animation(screen, popup_rect)
        elif animation_type == "division":
            self.division_animation(screen, popup_rect)

    def _display_text(self, screen, text, position, popup_rect):
        text_surface = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(topleft=(popup_rect.x + position[0], popup_rect.y + position[1]))
        screen.blit(text_surface, text_rect)

    def addition_animation(self, screen, popup_rect):
        apple_image = pygame.image.load('data\\images\\collectables\\collectable_1.png')
        apple_image = pygame.transform.scale(apple_image, (40, 40))

        # Step 1: Display initial message
        screen.fill((255, 255, 255), popup_rect)  # Clear only the popup area
        self._display_text(screen, "I have 2 apples.", (20, 20), popup_rect)
        pygame.display.update(popup_rect)
        time.sleep(1.5)

        # Step 2: Display initial apples
        for i in range(2):
            screen.blit(apple_image, (popup_rect.x + 40 + i * 50, popup_rect.y + 80))
        pygame.display.update(popup_rect)
        time.sleep(1.5)

        # Step 3: Display additional apples
        self._display_text(screen, "Another person gives me 3 more apples.", (20, 150), popup_rect)
        pygame.display.update(popup_rect)
        time.sleep(1.5)
        for i in range(3):
            screen.blit(apple_image, (popup_rect.x + 40 + (i + 2) * 50, popup_rect.y + 80))
        pygame.display.update(popup_rect)
        time.sleep(1.5)

        # Step 4: Display final result
        self._display_text(screen, "Now, I have 5 apples!", (20, 220), popup_rect)
        pygame.display.update(popup_rect)
        time.sleep(2)

    def subtraction_animation(self, screen, popup_rect):
        apple_image = pygame.image.load('apple.png')
        apple_image = pygame.transform.scale(apple_image, (40, 40))

        # Step 1: Display initial message
        screen.fill((255, 255, 255), popup_rect)  # Clear only the popup area
        self._display_text(screen, "I have 5 apples.", (20, 20), popup_rect)
        pygame.display.update(popup_rect)
        time.sleep(1.5)

        # Step 2: Display initial apples
        for i in range(5):
            screen.blit(apple_image, (popup_rect.x + 40 + i * 50, popup_rect.y + 80))
        pygame.display.update(popup_rect)
        time.sleep(1.5)

        # Step 3: Remove apples
        self._display_text(screen, "I give away 3 apples.", (20, 150), popup_rect)
        pygame.display.update(popup_rect)
        time.sleep(1.5)
        for i in range(3):
            pygame.draw.rect(screen, (255, 255, 255), (popup_rect.x + 40 + i * 50, popup_rect.y + 80, 40, 40))
            pygame.display.update(popup_rect)
            time.sleep(0.5)

        # Step 4: Display final result
        self._display_text(screen, "Now, I have 2 apples left!", (20, 220), popup_rect)
        pygame.display.update(popup_rect)
        time.sleep(2)

    def multiplication_animation(self, screen, popup_rect):
        apple_image = pygame.image.load('apple.png')
        apple_image = pygame.transform.scale(apple_image, (40, 40))

        # Step 1: Display initial message
        screen.fill((255, 255, 255), popup_rect)  # Clear only the popup area
        self._display_text(screen, "I create 3 groups of 2 apples.", (20, 20), popup_rect)
        pygame.display.update(popup_rect)
        time.sleep(1.5)

        # Step 2: Draw groups of apples
        for group in range(3):
            for i in range(2):
                screen.blit(apple_image, (popup_rect.x + 40 + i * 50, popup_rect.y + 80 + group * 60))
            pygame.display.update(popup_rect)
            time.sleep(0.5)

        # Step 3: Display final result
        self._display_text(screen, "In total, I have 6 apples!", (20, 220), popup_rect)
        pygame.display.update(popup_rect)
        time.sleep(2)

    def division_animation(self, screen, popup_rect):
        apple_image = pygame.image.load('apple.png')
        apple_image = pygame.transform.scale(apple_image, (40, 40))

        # Step 1: Display initial message
        screen.fill((255, 255, 255), popup_rect)  # Clear only the popup area
        self._display_text(screen, "I have 6 apples, I divide them into 2 groups.", (20, 20), popup_rect)
        pygame.display.update(popup_rect)
        time.sleep(1.5)

        # Step 2: Draw apples
        for i in range(6):
            screen.blit(apple_image, (popup_rect.x + 40 + (i % 3) * 50, popup_rect.y + 80 + (i // 3) * 60))
        pygame.display.update(popup_rect)
        time.sleep(1.5)

        # Step 3: Display final result
        self._display_text(screen, "Each group has 3 apples!", (20, 220), popup_rect)
        pygame.display.update(popup_rect)
        time.sleep(2)
