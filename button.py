import pygame

class Button:
    def __init__(self, x, y, width, height, shape='rect', color=(0, 128, 255), text='', text_color=(255, 255, 255),
                 font_size=30, padding=10, hover_color=None, border_radius=0, alpha=255, image=None, animation_speed=5):
        """
        x, y: Position of the button on the screen.
        width, height: Size of the button.
        shape: 'rect' for rectangle, 'circle' for circle button.
        color: Background color of the button.
        text: Button text.
        text_color: Color of the text.
        font_size: Size of the text font.
        padding: Padding around the text inside the button.
        hover_color: Color to use when hovering over the button.
        border_radius: Radius for rounded corners (only used for rectangles).
        alpha: Transparency level for the button.
        image: Optional image to display inside the button (as a pygame.Surface).
        """
        self.x = x
        self.y = y
        self.original_width = width
        self.original_height = height
        self.width = width
        self.height = height
        self.shape = shape
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)
        self.padding = padding
        self.hover_color = hover_color if hover_color else color
        self.border_radius = border_radius
        self.alpha = alpha
        self.image = image  # Optional image for the button
        self.animation_speed = animation_speed
        self.current_alpha = alpha
        self.is_hovered = False
        self.current_scale = 1.0
        self.active = True

    def draw(self, surface):
        # Create a temporary surface with transparency
        button_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        button_surface.set_alpha(self.current_alpha)

        # Handle different button shapes
        if self.shape == 'rect':
            # Draw a rectangle with optional rounded corners
            pygame.draw.rect(button_surface, self.hover_color if self.is_hovered else self.color, button_surface.get_rect(), 
                             border_radius=self.border_radius)
        elif self.shape == 'circle':
            # Draw a circle button
            pygame.draw.circle(button_surface, self.hover_color if self.is_hovered else self.color, 
                               (self.width // 2, self.height // 2), self.width // 2)

        # Draw the image if provided
        if self.image:
            img_rect = self.image.get_rect(center=(self.width // 2, self.height // 2))
            button_surface.blit(self.image, img_rect)

        # Draw the text inside the button
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        button_surface.blit(text_surface, text_rect)

        # Draw the button surface to the main surface
        surface.blit(button_surface, (self.x - (self.width - self.original_width) // 2,
                                      self.y - (self.height - self.original_height) // 2))

    def update_hover(self, mouse_pos):
        self.is_hovered = self.get_rect().collidepoint(mouse_pos) if self.active else False
        if self.is_hovered:
            # Increase alpha for fade-in effect
            self.current_alpha = min(255, self.current_alpha + self.animation_speed)
            # Scale the button for animation
            self.current_scale = min(1.1, self.current_scale + 0.05)  # Adjusted for responsiveness
        else:
            # Decrease alpha for fade-out effect
            self.current_alpha = max(self.alpha, self.current_alpha - self.animation_speed)
            # Reset scale when not hovered
            self.current_scale = max(1.0, self.current_scale - 0.05)

        # Update the width and height based on scale
        self.width = int(self.original_width * self.current_scale)
        self.height = int(self.original_height * self.current_scale)

    def get_rect(self):
        return pygame.Rect(self.x - (self.width - self.original_width) // 2, 
                           self.y - (self.height - self.original_height) // 2, 
                           self.width, self.height)

    def is_clicked(self, mouse_pos):
        return self.is_hovered and self.get_rect().collidepoint(mouse_pos)
    
    def deactivate(self):
        self.active = False
        self.color = (150, 150, 150) 
