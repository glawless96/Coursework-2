import pygame
from button import Button

class PopUp:
    def __init__(self, x, y, width, height, bg_color=(200, 200, 200), text_color=(0, 0, 0), border_radius=15, shadow_offset=5):
        pygame.font.init()

        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, 36)
        self.bg_color = bg_color
        self.text_color = text_color
        self.message = ""
        self.buttons = []
        self.visible = False
        self.border_radius = border_radius
        self.shadow_offset = shadow_offset

        # Animation attributes
        self.animation_progress = 0.0  # Progress between 0.0 and 1.0
        self.animation_duration = 0.5  # Duration in seconds

    def set_message(self, message):
        self.message = message

    def add_button(self, x_offset, y_offset, width, height, **kwargs):
        button_x = self.rect.centerx + x_offset - width // 2
        button_y = self.rect.centery + y_offset - height // 2
        button = Button(button_x, button_y, width, height, **kwargs)
        self.buttons.append(button)

    def show(self):
        self.visible = True
        self.animation_progress = 0.0  # Reset animation progress

    def hide(self):
        self.visible = False

    def update(self, mouse_pos, delta_time):
        if self.visible:
            # Smoothly update popup animation
            self.animation_progress = min(self.animation_progress + delta_time / self.animation_duration, 1.0)
            
            # Update buttons independently
            for button in self.buttons:
                button.update_hover(mouse_pos)

    def draw(self, screen):
        if not self.visible:
            return

        # Draw shadow
        shadow_rect = self.rect.move(self.shadow_offset, self.shadow_offset)
        pygame.draw.rect(screen, (50, 50, 50), shadow_rect, border_radius=self.border_radius)

        # Smooth scaling animation
        scale = self.animation_progress
        animated_rect = self.rect.inflate(
            -int(self.rect.width * (1 - scale)), -int(self.rect.height * (1 - scale))
        )

        # Draw the background with rounded corners
        pygame.draw.rect(screen, self.bg_color, animated_rect, border_radius=self.border_radius)

        # Draw the border
        pygame.draw.rect(screen, (0, 0, 0), animated_rect, width=2, border_radius=self.border_radius)

        # Render the message text
        if self.message:
            text_surface = self.font.render(self.message, True, self.text_color)
            text_rect = text_surface.get_rect(center=(animated_rect.centerx, animated_rect.y + 40))
            screen.blit(text_surface, text_rect)

        # Draw the buttons
        for button in self.buttons:
            button.draw(screen)
