import pygame
import sqlite3
import hashlib

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Login Page")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
HOVER_COLOR = (245, 238, 135)
BUTTON_COLOR = (254, 247, 140)
TRANSLUCENT_SHADE = (0, 0, 0, 150)  # RGBA with alpha for transparency

# Fonts
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 74)

# Background image
background_image = pygame.image.load("StartScreen_background.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# SQLite setup
db_file = "game_data.db"

def setup_database():
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            level INTEGER DEFAULT 1
        )
    ''')
    connection.commit()
    connection.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO players (username, password) VALUES (?, ?)', (username, hash_password(password)))
        connection.commit()
        connection.close()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(username, password):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM players WHERE username = ? AND password = ?', (username, hash_password(password)))
    user = cursor.fetchone()
    connection.close()
    return user

class Button:
    def __init__(self, x, y, w, h, text, font, color, hover_color, text_color, border_radius=10):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_radius = border_radius

    def draw(self, screen, mouse_pos):
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=self.border_radius)
        text_surf = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surf, (self.rect.x + (self.rect.width - text_surf.get_width()) // 2,
                                self.rect.y + (self.rect.height - text_surf.get_height()) // 2))

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# Main login page
def login_page():
    setup_database()

    username = ""
    password = ""
    message = ""

    username_box = pygame.Rect(360, 200, 300, 40)
    password_box = pygame.Rect(360, 260, 300, 40)

    login_button = Button(360, 320, 200, 50, "Login", font, BUTTON_COLOR, HOVER_COLOR, BLACK)
    register_button = Button(360, 380, 200, 50, "Register", font, BUTTON_COLOR, HOVER_COLOR, BLACK)

    input_active = {"username": False, "password": False}

    # Create translucent shade
    translucent_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    translucent_surface.fill(TRANSLUCENT_SHADE)

    running = True
    while running:
        screen.blit(background_image, (0, 0))
        screen.blit(translucent_surface, (0, 0))  # Apply translucent shade

        # Draw UI elements
        title_text = title_font.render("Login Page", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

        username_label = font.render("Username:", True, WHITE)
        password_label = font.render("Password:", True, WHITE)
        screen.blit(username_label, (200, 200))
        screen.blit(password_label, (200, 260))

        pygame.draw.rect(screen, GRAY, username_box, 2)
        pygame.draw.rect(screen, GRAY, password_box, 2)

        login_button.draw(screen, pygame.mouse.get_pos())
        register_button.draw(screen, pygame.mouse.get_pos())

        # Display messages
        message_text = font.render(message, True, WHITE)
        screen.blit(message_text, (WIDTH // 2 - message_text.get_width() // 2, 450))

        # Display input text
        username_text = font.render(username, True, WHITE)
        password_text = font.render("*" * len(password), True, WHITE)
        screen.blit(username_text, (username_box.x + 5, username_box.y + 5))
        screen.blit(password_text, (password_box.x + 5, password_box.y + 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                input_active["username"] = username_box.collidepoint(event.pos)
                input_active["password"] = password_box.collidepoint(event.pos)

                if login_button.is_clicked(event.pos):
                    user = login_user(username, password)
                    if user:
                        message = f"Welcome back, {username}! Level: {user[3]}"
                    else:
                        message = "Invalid username or password!"
                elif register_button.is_clicked(event.pos):
                    if register_user(username, password):
                        message = "Registration successful! Please login."
                    else:
                        message = "Username already exists!"

            if event.type == pygame.KEYDOWN:
                if input_active["username"]:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode
                elif input_active["password"]:
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    login_page()
