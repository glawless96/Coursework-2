import pygame
from button import Button
<<<<<<< Updated upstream
=======
from static import ColorData
color = ColorData()
clock = pygame.time.Clock()
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
        self.animation_progress = 0.0  # Progress between 0.0 and 1.0
        self.animation_duration = 0.5  # Duration in seconds
=======
        self.animation_progress = 0.0
        self.animation_duration = 0.5
        self.animation_type = None
        self.animated_rect = None
        self.animation_time = 0
        self.animation_step = 0
        self.animation_expression = ''
>>>>>>> Stashed changes

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
    
    def start_animation(self, animation_type, x, y, width, height):
        self.animation_type = animation_type
        self.animated_rect = pygame.Rect(x, y, width, height)

    def draw(self, screen, delta_time):
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
<<<<<<< Updated upstream
=======

        if self.animation_type and self.animated_rect and not self.animation_played:
            print('Playing addition animation')
            self.animate_operation(screen, self.animated_rect, delta_time)

    def animate_operation(self, screen, rect, delta_time):
        object_image_path = 'data\\images\\collectables\\collectable_1.png'
        operation_image_path = 'data\\images\\math_symbols\\addition.png'
        equals_image_path = 'data\\images\\math_symbols\\equals.png'
        if self.animation_type == "+":
            stepText=[
                "Example for Addition :",
                "I have 2 apples.",
                "Another person gives me 3 more apples.",
                "So, I have 5 apples!"
            ]
            self.play_math_animation(screen, rect, delta_time, object_image_path, operation_image_path, equals_image_path, 2, 3, stepText)
        if self.animation_type == "-":
            stepText=[
                "Example for Subtraction :",
                "I have 5 apples.",
                "I give 2 apples to another person.",
                "Now, I have 3 apples!"
            ]
            self.play_math_animation(screen, rect, delta_time, object_image_path, operation_image_path, equals_image_path, 5, 2, stepText)
        if self.animation_type == "*":
            stepText = [
                "Example for Multiplication:",
                "I have 2 baskets of apples.",
                "Each basket has 3 apples.",
                "So, I have 2 times 3 apples, which is 6 apples in total!"
            ]
            self.play_math_animation(screen, rect, delta_time, object_image_path, operation_image_path, equals_image_path, 2, 3, stepText)
        if self.animation_type == "/":
            stepText = [
                "Example for Division:",
                "I have 6 apples.",
                "I want to share them equally with 2 friends.",
                "So, each person gets 6 divided by 2 apples, which is 3 apples each!"
            ]
            self.play_math_animation(screen, rect, delta_time, object_image_path, operation_image_path, equals_image_path, 2, 3, stepText)
        
    def play_math_animation(self, screen, rect, delta_time, object_image_path, operation_image_path, equals_image_path, num1, num2, stepText = []):

        self.animation_expression = ''
        if not hasattr(self, 'object_image'):
            self.object_image = pygame.image.load( object_image_path ).convert_alpha()#'data\\images\\collectables\\collectable_1.png')
            self.object_image = pygame.transform.scale(self.object_image, (30, 30))

        if not hasattr(self, 'operation_image'):
            self.operation_image = pygame.image.load( operation_image_path ).convert_alpha() #'data\\images\\math_symbols\\addition.png')
            self.operation_image = pygame.transform.scale(self.operation_image, (30, 30))

        if not hasattr(self, 'equals_image'):
            self.equals_image = pygame.image.load( equals_image_path ).convert_alpha() #'data\\images\\math_symbols\\equals.png')
            self.equals_image = pygame.transform.scale(self.equals_image, (30, 30))

        # Step durations in seconds
        step_durations = [1, 3, 6, 8]
        total_steps = len(step_durations)

        if not hasattr(self, 'animation_step'):
            # Initialize animation state
            self.animation_step = 0
            self.animation_time = 0
    
        # Update animation time
        self.animation_time += delta_time
        # Advance steps if the duration for the current step is completed
        if self.animation_step < total_steps and self.animation_time >= step_durations[self.animation_step]:
            self.animation_step += 1
            self.animation_time = 0

        # Step 1: Display initial message
        self.display_text(screen, stepText[0], (20, 20), rect)

        # Step 2: Display initial apples
        if self.animation_step == 1:
            self.draw_centered_text(screen, stepText[1],70, rect)
            self.animation_expression = ' '+str(num1)+' '
            self.draw_row(screen, [self.object_image] * num1, rect, 100)

        # Step 3: Display additional apples
        elif self.animation_step == 2:
            self.draw_centered_text(screen, stepText[2], 70, rect)
            self.animation_expression = ' '+str(num1)+' '+self.animation_type+' '+str(num2)
            self.draw_row(
                screen,
                [self.object_image] * num1 + [self.operation_image] + [self.object_image] * num2,
                rect, 100
                )

        # Step 4: Display final result
        elif self.animation_step >= 3:

            results = {
                "+": num1 + num2,
                "-": num1 - num2,
                "*": num1 * num2,
                "/": num1 // num2 if num2 != 0 else "Undefined"  # Integer division
            }
            result = results.get(self.animation_type, "Undefined")
            
            self.draw_centered_text(screen, stepText[3], 70, rect)
            self.animation_expression = ' '+str(num1)+' '+self.animation_type+' '+str(num2)+' = '+str(result)+' '
            self.draw_row(
                screen,
                [self.object_image] * num1 + [self.operation_image] + [self.object_image] * num2 + [self.equals_image] + [self.object_image] * result ,
                rect, 100
            )

        self.draw_centered_text(screen, self.animation_expression, 150, rect)

    def display_text(self, screen, text, position, rect):
        text_surface = self.font.render(text, True, color.white)
        text_rect = text_surface.get_rect(topleft=(rect.x + position[0], rect.y + position[1]))
        screen.blit(text_surface, text_rect)

    def draw_centered_text(self, screen, text, y_offset, rect):
        text_surface = self.font.render(text, True, color.white)
        text_rect = text_surface.get_rect(center=(rect.centerx, rect.y + y_offset))
        screen.blit(text_surface, text_rect)

    def draw_row(self, screen, items, rect, y_offset, spacing=10, align="center", animation_duration=1.0):
        total_width = sum(item.get_rect().width for item in items) + spacing * (len(items) - 1)

        if align == "center":
            x_start = rect.centerx - total_width // 2
        elif align == "left":
            x_start = rect.x + 20
        elif align == "right":
            x_start = rect.right - total_width - 20
        else:
            raise ValueError("Invalid align value. Use 'center', 'left', or 'right'.")

        # Calculate how many items should be displayed based on the current animation progress
        num_items_to_display = int(len(items) * self.animation_progress)
        
        current_x = x_start
        for i in range(num_items_to_display):
            item = items[i]
            # Calculate the position for each item based on the current index
            item_rect = item.get_rect(topleft=(current_x, rect.y + y_offset))
            screen.blit(item, item_rect)
            current_x += item.get_rect().width + spacing
>>>>>>> Stashed changes
