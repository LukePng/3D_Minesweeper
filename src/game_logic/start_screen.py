import pygame

from static.constants import *
from static.button import Button

class StartScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.buttons = self.create_buttons()

    def create_buttons(self):
        return [
            Button("Easy", (SCREEN_WIDTH // 2, 300), GREEN, 50, action=lambda: self.set_difficulty(0), border_color=WHITE, border_width=3),
            Button("Medium", (SCREEN_WIDTH // 2, 400), BLUE, 50, action=lambda: self.set_difficulty(1), border_color=WHITE, border_width=3),
            Button("Hard", (SCREEN_WIDTH // 2, 500), RED, 50, action=lambda: self.set_difficulty(2), border_color=WHITE, border_width=3),
            Button("Start Game", (SCREEN_WIDTH // 2, 600), YELLOW, 50, action=self.game.run_game, border_color=WHITE, border_width=3)
        ]

    def set_difficulty(self, level):
        self.game.set_difficulty(level)
        for button in self.buttons:
            button.reset_color()
            
        self.buttons[level].set_highlight(WHITE)

    def display(self):
        font = pygame.font.Font(None, 74)
        title_text = font.render("Welcome to the Game", True, WHITE)
        running = True

        while running:
            self.screen.fill(BLACK)
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 150))

            mouse_pos = pygame.mouse.get_pos()
            self.game.get_hovering = False

            for button in self.buttons:
                button.draw(self.screen)
                if button.is_hovered(mouse_pos):
                    self.game.set_hovering(True)

            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if self.game.get_hovering else pygame.SYSTEM_CURSOR_ARROW)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.quit_game()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button.is_clicked(mouse_pos):
                            button.action()