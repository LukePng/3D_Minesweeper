import pygame
import sys

from static.constants import *
from static.button import Button
from game_logic.game_screen import GameScreen

class EndScreen:
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen
        self.game_screen = GameScreen(self.game, self.screen)

        # Create buttons for end screen
        self.end_buttons = [
            Button("New Puzzle", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50), GREEN, 50, action=self.game.display_start_screen, border_color=WHITE, border_width=3),
            Button("View Board", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150), BLUE, 50, action=self.game_screen.show_board, border_color=WHITE, border_width=3)
        ]


    def display(self, message):
        #Display the end screen with buttons for New Puzzle and View Board
        font = pygame.font.Font(None, 74)
        text_surface = font.render(message, True, RED)
        self.screen.fill(BLACK)
        self.screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

        # Draw buttons
        for button in self.end_buttons:
            button.draw(self.screen)

        pygame.display.flip()
        # Wait for button actions
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in self.end_buttons:
                        if button.is_clicked(mouse_pos):
                            self.game.set_is_end(True)
                            button.action()  # Perform the action for the clicked button