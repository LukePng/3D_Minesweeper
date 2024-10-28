import pygame

# Button Class
class Button:
    def __init__(self, text, pos, color, font_size, action=None, border_color=pygame.Color("white"), border_width=1):
        self.text = text
        self.pos = pos
        self.default_color = color  # Store the default color for highlighting
        self.color = color  # Current color of the button (changes on selection)
        self.font = pygame.font.Font(None, font_size)
        self.action = action  # Function to call when the button is clicked
        self.border_color = border_color
        self.border_width = border_width

        # Render the text and get its rectangle
        self.rendered_text = self.font.render(self.text, True, self.color)
        self.rect = self.rendered_text.get_rect(center=pos)

    def draw(self, screen):
        self.rendered_text = self.font.render(self.text, True, self.color)
        pygame.draw.rect(screen, self.border_color, self.rect.inflate(self.border_width * 2, self.border_width * 2), self.border_width)
        screen.blit(self.rendered_text, self.rect)

    def is_clicked(self, mouse_pos): # For Clicking
        return self.rect.collidepoint(mouse_pos)

    def set_highlight(self, highlight_color):
        self.color = highlight_color

    def reset_color(self):
        self.color = self.default_color

    def is_hovered(self, mouse_pos): # For Hovering
        return self.rect.collidepoint(mouse_pos)

