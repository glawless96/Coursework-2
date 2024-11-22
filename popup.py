import pygame
from button import Button


class PopUp:
    def __init__(self, x, y, width, height, bg_color=(200, 200, 200), text_color=(0, 0, 0), border_radius=15, shadow_offset=5):
        """
        A reusable pop-up class with animations and interactive buttons.
        :param x: X-coordinate of the top-left corner.
        :param y: Y-coordinate of the top-left corner.
        :param width: Width of the pop-up.
        :param height: Height of the pop-up.
        :param font: Pygame font for text.
        :param bg_color: Background color of the pop-up.
        :param text_color: Text color.
        :param border_radius: Radius for rounded corners.
        :param shadow_offset: Offset for the shadow effect.
        """
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
        self.animation_progress = 0  # Used for smooth scaling animations

    def set_message(self, message):
        """Set the message to display in the pop-up."""
        self.message = message

    def add_button(self, x_offset, y_offset, width, height, **kwargs):
        """
        Add a button to the pop-up.
        :param x_offset: X-offset relative to the pop-up's center.
        :param y_offset: Y-offset relative to the pop-up's center.
        :param width: Width of the button.
        :param height: Height of the button.
        :param kwargs: Additional arguments for the Button class (e.g., text, color, etc.).
        """
        button_x = self.rect.centerx + x_offset - width // 2
        button_y = self.rect.centery + y_offset - height // 2
        button = Button(button_x, button_y, width, height, **kwargs)
        self.buttons.append(button)

    def show(self):
        self.visible = True
        self.animation_progress = 0  # Reset animation progress when shown

    def hide(self):
        self.visible = False

    def update(self, mouse_pos):
        if self.visible:
            for button in self.buttons:
                button.update_hover(mouse_pos)

    def draw(self, screen):
        """Render the pop-up on the screen."""
        if not self.visible:
            return

        # Draw shadow
        shadow_rect = self.rect.move(self.shadow_offset, self.shadow_offset)
        pygame.draw.rect(screen, (50, 50, 50), shadow_rect, border_radius=self.border_radius)

        # Smooth scaling animation
        scale = min(1.0, self.animation_progress / 10)
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

        # Update animation progress
        if self.animation_progress < 10:
            self.animation_progress += 1
