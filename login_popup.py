import pygame
from button import Button
from game_utilities import register_user, login_user

class LoginPopup:
    def __init__(self, screen):
        self.screen = screen
        self.active_user = False
        self.active_pass = False
        self.user_text = ''
        self.pass_text = ''
        self.popup_rect = pygame.Rect(150, 100, 980, 520)
        self.input_box_user = pygame.Rect(340, 200, 600, 50)
        self.input_box_pass = pygame.Rect(340, 270, 600, 50)
        self.color_inactive = pygame.Color('gray')
        self.color_active = pygame.Color('dodgerblue2')
        self.font = pygame.font.Font(None, 36)

        # Buttons
        self.login_button = Button(170, 340, 120, 50, text="Login", hover_color=(100, 200, 255))
        self.register_button = Button(310, 340, 120, 50, text="Register", hover_color=(150, 200, 150))
        self.cancel_button = Button(450, 340, 120, 50, text="Cancel", hover_color=(255, 100, 100))

    def draw(self):
        # Draw translucent background
        translucent_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        translucent_surface.fill((0, 0, 0, 128))  # Semi-transparent black
        self.screen.blit(translucent_surface, (0, 0))

        # Draw popup box
        pygame.draw.rect(self.screen, (30, 30, 30), self.popup_rect, border_radius=10)
        pygame.draw.rect(self.screen, pygame.Color('white'), self.popup_rect, width=2, border_radius=10)

        # Draw input boxes
        pygame.draw.rect(self.screen, self.color_active if self.active_user else self.color_inactive,
                         self.input_box_user, border_radius=5)
        pygame.draw.rect(self.screen, self.color_active if self.active_pass else self.color_inactive,
                         self.input_box_pass, border_radius=5)

        # Draw buttons
        self.login_button.draw(self.screen)
        self.register_button.draw(self.screen)
        self.cancel_button.draw(self.screen)

        # Draw text
        self.render_text("Username:", (170, 215))
        self.render_text("Password:", (170, 285))
        self.render_text(self.user_text, (340, 220), input_box=True)
        self.render_text('*' * len(self.pass_text), (340, 292), input_box=True)

    def render_text(self, text, pos, input_box=False):
        font = self.font if not input_box else pygame.font.Font(None, 28)
        text_surface = font.render(text, True, pygame.Color('white'))
        self.screen.blit(text_surface, pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if clicked inside input boxes
            if self.input_box_user.collidepoint(event.pos):
                self.active_user = True
                self.active_pass = False
            elif self.input_box_pass.collidepoint(event.pos):
                self.active_user = False
                self.active_pass = True
            else:
                self.active_user = False
                self.active_pass = False

            # Check if clicked buttons
            if self.login_button.is_clicked(event.pos):
                user = login_user(self.user_text, self.pass_text)
                if user:
                    return {"action": "login", "user": user}
                else:
                    print("Invalid User")
                    return {"action": "login", "user": None}
            
            if self.register_button.is_clicked(event.pos):
                user = register_user(self.user_text, self.pass_text)
                if user:
                    return {"action": "register", "user": user}
                else:
                    print("Invalid User")
                    return {"action": "register", "user": None}
            
            if self.cancel_button.is_clicked(event.pos):
                return {"action": "cancel", "user": None}

        if event.type == pygame.KEYDOWN:
            if self.active_user:
                if event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                else:
                    self.user_text += event.unicode
            elif self.active_pass:
                if event.key == pygame.K_BACKSPACE:
                    self.pass_text = self.pass_text[:-1]
                else:
                    self.pass_text += event.unicode

        return None

    def update(self, mouse_pos):
        # Update button hover states
        self.login_button.update_hover(mouse_pos)
        self.register_button.update_hover(mouse_pos)
        self.cancel_button.update_hover(mouse_pos)
