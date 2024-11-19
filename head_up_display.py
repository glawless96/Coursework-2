import pygame

from static import HeaderData, ScreenData, HealthData, ColorData

header_static = HeaderData()
screen_static = ScreenData()
health_static = HealthData()
color_static = ColorData()

class HeadUpDisplay():
    def __init__(self, target_number):
        self.height = header_static.height
        self.width = header_static.width
        self.font = pygame.font.Font(None, 36)
        self.time_start = pygame.time.get_ticks()
        self.collected_items = []
        self.target_number = target_number
        self.health = 5
        self.health_icon_size = (40, 40)
        self.health_images = [
            pygame.transform.scale(pygame.image.load(health_static.health_image), self.health_icon_size)
            for _ in range(self.health)
        ]
    
    def update_collectiables(self, collected_items):
        self.collected_items = collected_items 
    
    def update_health(self, remainig_health):
        self.health = remainig_health

    def get_elapsed_time(self):
        current_time = pygame.time.get_ticks()
        return (current_time - self.time_start) // 100
    
    def draw_header(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), (0, 0, self.width, self.height))

        time_elapsed = self.get_elapsed_time()
        time_text = self.font.render(f"Time : {time_elapsed}", True, color_static.white)
        screen.blit(time_text, (20, 20))

        collected_text = self.font.render(f"Target Number: {self.target_number}", True, color_static.white)
        screen.blit(collected_text, (200, 20))

        collected_text = self.font.render(f"Collected Numbers: ", True, color_static.white)
        screen.blit(collected_text, (200, 20))

        for i in range(self.health):
            x = 10 + i * (self.health_icon_size[0] + 5)
            y = 10
            screen.blit(self.health_images[i], (x, y))
