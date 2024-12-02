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
        self.health = health_static.maxHealth
        self.health_icon_size = (40, 40)
        self.health_images = [
            pygame.transform.scale(pygame.image.load(health_static.health_image), self.health_icon_size)
            for _ in range(self.health)
        ]
    def update_target(self, target_number):
        self.target_number = target_number
    
    def update_collectiables(self, collected_items):
        self.collected_items = collected_items 
    
    def update_health(self, remaining_health):
        self.health = remaining_health
        # Dynamically update health images based on remaining health
        self.health_images = [
            pygame.transform.scale(pygame.image.load(health_static.health_image), self.health_icon_size)
            for _ in range(self.health)
        ]

    def get_elapsed_time(self):
        current_time = pygame.time.get_ticks()
        return (current_time - self.time_start) // 100
    
    def draw_header(self, screen):
        pygame.draw.rect(screen, color_static.black, (0, 0, self.width, self.height))

        #elapsed time
        time_elapsed = self.get_elapsed_time()
        time_text = self.font.render(f"Time: {time_elapsed}s", True, color_static.white)
        screen.blit(time_text, (20, 20))

        exp = "Get all numbers that adds up to : " + str(self.target_number)
        #target number
        target_text = self.font.render(f"{exp}", True, color_static.white)
        screen.blit(target_text, (300, 30))

        #collected numbers
        collected_text = self.font.render("Collected Numbers:", True, color_static.white)
        screen.blit(collected_text, (300, 60))
        for idx, item in enumerate(self.collected_items):
            collected_item_text = self.font.render(item.label, True, color_static.white)
            screen.blit(collected_item_text, (600 + idx * 30, 60))  # Space out the collected items

        #health icons
        for i in range(self.health):
            x = 20 + i * (self.health_icon_size[0] + 5)
            y = self.height - self.health_icon_size[1] - 10
            screen.blit(self.health_images[i], (x, y))
