import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 128, 255)
BUTTON_HOVER_COLOR = (0, 255, 255)
BUTTON_SELECTED_COLOR = (255, 0, 0)  # Color for selected button
TITLE_COLOR = (255, 255, 0)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Starting Page")

# Load fonts
title_font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 36)

# Define button properties
button_width = 200
button_height_large = 80
button_height_small = 50
button_y_start = HEIGHT // 4
button_y_spacing_large = 100
button_y_spacing_small = 60
difficulty_buttons = ["Easy", "Medium", "Hard"]
selected_difficulty = None

# Define buttons
buttons = [
    {"text": "Start Game", "rect": pygame.Rect((WIDTH - button_width) // 2, button_y_start, button_width, button_height_large)},
    {"text": "Quit Game", "rect": pygame.Rect((WIDTH - button_width) // 2, button_y_start + button_y_spacing_large + 60, button_width, button_height_small)},
]

# Create difficulty buttons in a single row
for i, difficulty in enumerate(difficulty_buttons):
    buttons.insert(1 + i, {"text": difficulty, "rect": pygame.Rect((WIDTH - (len(difficulty_buttons) * (button_width + 20) - 20)) // 2 + i * (button_width + 20), button_y_start + button_y_spacing_large, button_width, button_height_small)})

def draw_rounded_rect(surface, color, rect, radius):
    """Draw a rounded rectangle."""
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def draw_title():
    title_surface = title_font.render("Minesweeper", True, TITLE_COLOR)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4 - 50))  # Position above buttons
    screen.blit(title_surface, title_rect)

def draw_buttons():
    for button in buttons:
        if button["rect"].collidepoint(pygame.mouse.get_pos()):
            draw_rounded_rect(screen, BUTTON_HOVER_COLOR, button["rect"], 15)
        else:
            # Change color if selected
            if button["text"] == selected_difficulty:
                draw_rounded_rect(screen, BUTTON_SELECTED_COLOR, button["rect"], 15)
            else:
                draw_rounded_rect(screen, BUTTON_COLOR, button["rect"], 15)

        text_surface = button_font.render(button["text"], True, WHITE)
        text_rect = text_surface.get_rect(center=button["rect"].center)
        screen.blit(text_surface, text_rect)

# Main loop
def main():
    global selected_difficulty
    while True:
        screen.fill(BLACK)
        draw_title()
        draw_buttons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                for button in buttons:
                    if button["rect"].collidepoint(event.pos):
                        handle_button_click(button["text"])

        pygame.display.flip()

def handle_button_click(button_text):
    global selected_difficulty
    if button_text == "Start Game":
        if selected_difficulty:
            print(f"Starting game with difficulty: {selected_difficulty}")  # Replace with actual game start logic
            game_start()
        else:
            print("Please select a difficulty level.")
    elif button_text in difficulty_buttons:
        selected_difficulty = button_text  # Set the selected difficulty
        print(f"Difficulty set to: {selected_difficulty}")
    elif button_text == "Quit Game":
        pygame.quit()
        sys.exit()

def game_start():
    pass

if __name__ == "__main__":
    main()
