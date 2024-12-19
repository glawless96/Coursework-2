import pygame

from button import Button
from static import HeaderData, ScreenData, HealthData, ColorData

header_static = HeaderData()
screen_static = ScreenData()
health_static = HealthData()
color_static = ColorData()

class HeadUpDisplay():
    def __init__(self, target_number, game_question):
        self.height = header_static.height
        self.width = header_static.width
        self.font = pygame.font.Font(None, 36)
        self.time_start = pygame.time.get_ticks()
        self.collected_items = []
        self.target_number = target_number
        self.health = health_static.maxHealth
        self.health_icon_size = (40, 40)
        self.health_images = [
            pygame.transform.scale(pygame.image.load(health_static.health_image), self.health_icon_size)
            for _ in range(self.health)
        ]
        self.game_question = game_question
        self.remaining_time = 0
        self.total_time = 360  # Set total time for the game in seconds
        self.progress_bar_width = 200  # Fixed width for the progress bar
        self.progress_bar_height = 20
        self.progress_bar_x = 20
        self.progress_bar_y = 20
        self.paused = False
        
        # Create the pause button
        self.pause_button = Button(
            x=screen_static.width - 180,  # Position near the top-right corner
            y=10,
            width=60,
            height=40,
            shape='rect',
            text="Pause",
            color=(232, 60, 60),
            text_color=(0, 0, 0),
            font_size=30,
            border_radius=5,
            hover_color=(255, 0, 0),
            alpha=200
        )
        self.help_button = Button(
            x=screen_static.width - 100,  # Position near the top-right corner
            y=10,
            width=60,
            height=40,
            shape='rect',
            text="Help",
            color=(254, 247, 140),
            text_color=(0, 0, 0),
            font_size=30,
            border_radius=5,
            hover_color=(245, 238, 135),
            alpha=200
        )

    def update_paused(self):
        self.paused = not self.paused

    def update_target(self, target_number):
        self.target_number = target_number

    def update_collectiables(self, collected_items):
        self.collected_items = collected_items 

    def update_health(self, remaining_health):
        self.health = remaining_health
        # Dynamically update health images based on remaining health
        self.health_images = [
            pygame.transform.scale(pygame.image.load(health_static.health_image).convert_alpha(), self.health_icon_size)
            for _ in range(self.health)
        ]

    def get_elapsed_time(self):
        current_time = pygame.time.get_ticks()
        return (current_time - self.time_start) // 100

    def update_remainig_time(self, remaining_time):
        self.remaining_time = remaining_time

    def interpolate_color(self, start_color, end_color, progress):
        r = start_color[0] + (end_color[0] - start_color[0]) * progress
        g = start_color[1] + (end_color[1] - start_color[1]) * progress
        b = start_color[2] + (end_color[2] - start_color[2]) * progress
        return (int(r), int(g), int(b))

    def draw_progress_bar(self, screen):
        # Calculate the progress ratio (0 to 1)
        progress = self.remaining_time / self.total_time
        filled_width = int(self.progress_bar_width * progress)

        # Colors for start (green) and end (red)
        start_color = (3, 252, 69)  # Hex: #03fc45
        end_color = (252, 3, 3)     # Hex: #fc0303

        # Calculate the interpolated color based on progress
        current_color = self.interpolate_color(start_color, end_color, 1 - progress)

        # Draw the filled portion of the progress bar with rounded corners
        pygame.draw.rect(
            screen,
            current_color,  # Dynamic color
            (self.progress_bar_x, self.progress_bar_y, filled_width, self.progress_bar_height),
            border_radius=10
        )

        # Draw the unfilled portion with a black background (optional)
        pygame.draw.rect(
            screen,
            (0, 0, 0),  # Black background for unfilled
            (self.progress_bar_x + filled_width, self.progress_bar_y, self.progress_bar_width - filled_width, self.progress_bar_height),
            border_radius=10
        )

        # Render the remaining time text
        time_text = self.font.render(f"{self.remaining_time}s", True, (255, 255, 255))  # White color
        text_rect = time_text.get_rect(center=(
            self.progress_bar_x + self.progress_bar_width // 2,  # Center horizontally
            self.progress_bar_y + self.progress_bar_height // 2  # Center vertically
        ))
        screen.blit(time_text, text_rect)

    def draw_header(self, screen):
        pygame.draw.rect(screen, color_static.black, (0, 0, self.width, self.height))

        # Time text
        # time_text = self.font.render(f"Time left: {self.remaining_time} s", True, color_static.white)
        # screen.blit(time_text, (20, 20))

        exp = self.game_question + str(self.target_number)
        # Target number
        target_text = self.font.render(f"{exp}", True, color_static.white)
        screen.blit(target_text, (300, 30))

        # Collected numbers
        collected_text = self.font.render("Collected Numbers:", True, color_static.white)
        screen.blit(collected_text, (300, 60))
        for idx, item in enumerate(self.collected_items):
            collected_item_text = self.font.render(str(item), True, color_static.white)
            screen.blit(collected_item_text, (600 + idx * 30, 60))  # Space out the collected items

        # Health icons
        for i in range(self.health):
            x = 20 + i * (self.health_icon_size[0] + 5)
            y = self.height - self.health_icon_size[1] - 10
            screen.blit(self.health_images[i], (x, y))

        # Draw the progress bar
        self.draw_progress_bar(screen)

        self.pause_button.draw(screen)
        self.help_button.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.pause_button.is_clicked(mouse_pos):
                self.update_paused()
                if self.paused:
                    self.pause_button.text = "Play"
                    self.pause_button.hover_color=(17, 255, 0)
                    self.pause_button.color=(52, 207, 41)
                else:
                    self.pause_button.text = "Pause"
                    self.pause_button.hover_color=(255, 0, 0)
                    self.pause_button.color=(232, 60, 60)
                return "pause"
            if self.help_button.is_clicked(mouse_pos):
                return "help"
        return None

    def update_hover(self, mouse_pos):
        self.pause_button.update_hover(mouse_pos)
        self.help_button.update_hover(mouse_pos)
