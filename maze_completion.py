import pygame
import question_wizard  # Import main.py to transition to the main game when required

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors and font
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font = pygame.font.Font(None, 36)

def question_screen(screen, collected_numbers):    
    # Run the setup screen to collect numbers, display instructions, etc.
    clock = pygame.time.Clock()
    setup_screen_active = True

    while setup_screen_active:
        screen.fill(WHITE)
        title = font.render("You completed the maze!", True, BLACK)
        instruction = font.render("Press SPACE to start the math challenge!", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
        screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, HEIGHT // 2))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Press SPACE to continue to the question screen
                    setup_screen_active = False
        
        pygame.display.flip()
        clock.tick(30)

    print('maze comp ',collected_numbers)    
    #start question wizard
    question_wizard.start_question_wizard(screen, collected_numbers)
