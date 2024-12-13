import pygame
from button import Button

class PopUp:
    def __init__(self, x, y, width, height, bg_color=(200, 200, 200), text_color=(0, 0, 0), border_radius=15, border_width=2, shadow_offset=5):
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

    def hide(self):
        self.visible = False

    def update(self, mouse_pos, delta_time):
        if self.visible:
            self.animation_progress = min(self.animation_progress + delta_time / self.animation_duration, 1.0)
            for button in self.buttons:
                button.update_hover(mouse_pos)

    def draw(self, screen):
        if not self.visible:
            return

        shadow_rect = self.rect.move(self.shadow_offset, self.shadow_offset)
        pygame.draw.rect(screen, (50, 50, 50), shadow_rect, border_radius=self.border_radius)

        scale = self.animation_progress
        animated_rect = self.rect.inflate(
            -int(self.rect.width * (1 - scale)), -int(self.rect.height * (1 - scale))
        )

        pygame.draw.rect(screen, self.bg_color, animated_rect, border_radius=self.border_radius)
        pygame.draw.rect(screen, (0, 0, 0), animated_rect, width=self.border_width, border_radius=self.border_radius)

        if self.title:
            title_surface = self.title["font"].render(self.title["text"], True, self.title["color"])
            title_rect = title_surface.get_rect(center=(animated_rect.centerx, animated_rect.y + 40))
            screen.blit(title_surface, title_rect)

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

        current_y = animated_rect.y + 90
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

        for button in self.buttons:
            button.draw(screen)
