import pygame

def handle_collision(player_pos, player_size, numbers, collected_numbers):
   
    player_rect = pygame.Rect(*player_pos, player_size, player_size)  
    for num in numbers[:]:  
        num_rect = pygame.Rect(*num["pos"], player_size, player_size) 
        if player_rect.colliderect(num_rect):  
            collected_numbers.append(num["value"])  
            numbers.remove(num)  
