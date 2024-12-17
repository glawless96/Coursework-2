import pygame
from button import Button
from static import ColorData
color = ColorData()
clock = pygame.time.Clock()

class PopUp:
    def __init__(self, x, y, width, height, bg_color=(200, 200, 200), text_color=(255, 255, 255), border_radius=15, border_width=2, shadow_offset=5):
        pygame.font.init()

        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, 36)
        self.bg_color = bg_color
        self.text_color = text_color
        self.title = ""
        self.message = []
        self.buttons = []
        self.visible = False
        self.border_radius = border_radius
        self.border_width = border_width
        self.shadow_offset = shadow_offset

        # Animation attributes
        self.animation_progress = 0.0
        self.animation_duration = 0.5
        self.animation_type = None
        self.animation_manager = None
        self.animated_rect = None
        self.animation_played = False
        self.animation_time = 0

    def set_message(self, message, font=None, font_size=None, font_style=None, color=None, spacing=30, x=None, y=None, align="center", border_color=None, border_width=0, padding=5, border_group=None):
        if font_size:
            font = pygame.font.Font(None, font_size)
        if font_style:
            font.set_bold("bold" in font_style)
            font.set_italic("italic" in font_style)

        self.message.append({
            "text": message,
            "font": font if font else self.font,
            "color": color if color else self.text_color,
            "spacing": spacing,
            "x": x,
            "y": y,
            "align": align,
            "border_color": border_color,
            "border_width": border_width,
            "padding": padding,
            "border_group": border_group
        })

    def reset_messages(self):
        self.message = []

    def set_title(self, title, font=None, font_size=None, font_style=None, color=None):
        if font_size:
            font = pygame.font.Font(None, font_size)
        if font_style:
            font.set_bold("bold" in font_style)
            font.set_italic("italic" in font_style)

        self.title = {
            "text": title,
            "font": font if font else self.font,
            "color": color if color else self.text_color,
        }

    def add_button(self, x_offset, y_offset, width, height, **kwargs):
        button_x = self.rect.centerx + x_offset - width // 2
        button_y = self.rect.centery + y_offset - height // 2
        button = Button(button_x, button_y, width, height, **kwargs)
        self.buttons.append(button)

    def show(self):
        self.visible = True
        self.animation_progress = 0.0
        self.animation_played = False

    def hide(self):
        self.visible = False

    def update(self, mouse_pos, delta_time):
        if self.visible:
            self.animation_progress = min(self.animation_progress + delta_time / self.animation_duration, 1.0)
            for button in self.buttons:
                button.update_hover(mouse_pos)

    def start_animation(self, animation_type, x, y, width, height):
        self.animation_type = animation_type
        self.animated_rect = pygame.Rect(x, y, width, height)

    def draw(self, screen, delta_time):
        if not self.visible:
            return

        # Create a semi-transparent background layer
        overlay = pygame.Surface((self.rect[2], self.rect[3]), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent black
        screen.blit(overlay, (self.rect[0], self.rect[1]))

        # Draw animated popup rectangle
        scale = self.animation_progress
        animated_rect = self.rect.inflate(
            -int(self.rect.width * (1 - scale)), -int(self.rect.height * (1 - scale))
        )
        # pygame.draw.rect(screen, self.bg_color, animated_rect, border_radius=self.border_radius)
        pygame.draw.rect(screen, (0, 0, 0), animated_rect, width=self.border_width, border_radius=self.border_radius)

        # Draw title
        if self.title:
            title_surface = self.title["font"].render(self.title["text"], True, self.title["color"])
            title_rect = title_surface.get_rect(center=(animated_rect.centerx, animated_rect.y + 40))
            screen.blit(title_surface, title_rect)

        # Draw non-grouped messages
        current_y = animated_rect.y + 90
        for msg in self.message:
            if msg["border_group"] is not None:
                continue

            font = msg["font"]
            text_surface = font.render(msg["text"], True, msg["color"])
            text_width, text_height = text_surface.get_size()

            if msg["x"] is not None and msg["y"] is not None:
                x_pos = animated_rect.x + msg["x"]
                y_pos = animated_rect.y + msg["y"]
            else:
                if msg["align"] == "left":
                    x_pos = animated_rect.x + 20
                elif msg["align"] == "right":
                    x_pos = animated_rect.right - text_width - 20
                else:
                    x_pos = animated_rect.centerx - text_width // 2
                y_pos = current_y
                current_y += msg["spacing"]

            screen.blit(text_surface, (x_pos, y_pos))

        # Draw grouped messages
        border_groups = {}
        for msg in self.message:
            group = msg["border_group"]
            if group is not None:
                if group not in border_groups:
                    border_groups[group] = {
                        "border_color": msg["border_color"],
                        "border_width": msg["border_width"],
                        "padding": msg["padding"],
                        "messages": []
                    }
                border_groups[group]["messages"].append(msg)

        for group, style in border_groups.items():
            messages = style["messages"]
            padding = style["padding"]
            border_color = style["border_color"]
            border_width = style["border_width"]

            max_width = max(msg["font"].size(msg["text"])[0] for msg in messages)
            total_height = sum(msg["spacing"] for msg in messages)

            group_rect = pygame.Rect(
                animated_rect.centerx - max_width // 2 - padding,
                current_y - padding,
                max_width + 2 * padding,
                total_height + 2 * padding
            )
            pygame.draw.rect(screen, border_color, group_rect, width=border_width, border_radius=5)

            y_offset = group_rect.y + padding
            for msg in messages:
                font = msg["font"]
                text_surface = font.render(msg["text"], True, msg["color"])
                text_rect = text_surface.get_rect(midtop=(group_rect.centerx, y_offset))
                screen.blit(text_surface, text_rect)
                y_offset += msg["spacing"]

            current_y = group_rect.bottom + 10

        # Draw buttons
        for button in self.buttons:
            button.draw(screen)

        if self.animation_type and self.animated_rect and not self.animation_played:
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
        step_durations = [1, 1.5, 1.5, 4]
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
