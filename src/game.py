from board import Board
from button import Button

import pygame
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("3D Minesweeper")
        self.difficulty = 0
        self.selected_button = None  # Track which button is selected

    def set_easy(self):
        self.difficulty = 0

    def set_medium(self):
        self.difficulty = 1

    def set_hard(self):
        self.difficulty = 2

    def start_screen(self):
        font = pygame.font.Font(None, 74)
        title_text = font.render("Welcome to the Game", True, WHITE)

        # Create buttons for difficulty selection
        easy_button = Button("Easy", (SCREEN_WIDTH // 2, 300), GREEN, 50, self.set_easy, border_color=WHITE, border_width=3)
        medium_button = Button("Medium", (SCREEN_WIDTH // 2, 400), BLUE, 50, self.set_medium, border_color=WHITE, border_width=3)
        hard_button = Button("Hard", (SCREEN_WIDTH // 2, 500), RED, 50, self.set_hard, border_color=WHITE, border_width=3)
        
        # Create Start Game button
        start_button = Button("Start Game", (SCREEN_WIDTH // 2, 600), YELLOW, 50, action=self.run_game, border_color=WHITE, border_width=3)

        self.buttons = [easy_button, medium_button, hard_button, start_button]
        self.difficulty_buttons = [easy_button, medium_button, hard_button]

        running = True
        while running:
            self.screen.fill(BLACK)
            # Render title
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 150))

            # Draw buttons
            for button in self.buttons:
                button.draw(self.screen)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Check for mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button.is_clicked(mouse_pos):
                            if button in self.difficulty_buttons:
                                # Reset the color of all buttons and highlight the selected one
                                for b in self.difficulty_buttons:
                                    b.reset_color()
                                button.set_highlight(WHITE)  # Highlight the selected button
                                button.action()  # Set the difficulty, but don't move to next page
                            elif button.text == "Start Game":
                                button.action()  # Start the game
    
    def initialize_board(self):
        if self.difficulty == 0:
            size = 3  
            num_mines = 2 
        if self.difficulty == 1:
            size = 5
            num_mines = 25 
        if self.difficulty == 2:
            size = 10 
            num_mines = 100 
        self.board = Board(size, num_mines)  # Create a Board instance
        self.board.gen_board()  # Generate the board

    def draw_board(self):
        # Assuming each cell is represented by a rectangle on the screen
        cell_size = SCREEN_WIDTH // self.board.get_size()  # Calculate size of each cell
        for z in range(self.board.get_size()):
            for y in range(self.board.get_size()):
                for x in range(self.board.get_size()):
                    cell = self.board.get_board()[z][y][x]
                    # Set the color based on the cell state
                    if cell.is_mine:
                        color = RED if cell.is_revealed else BLACK  # Red for revealed mines
                    elif cell.is_revealed:
                        color = WHITE  # Revealed cells are white
                    else:
                        color = GREEN  # Unrevealed cells are green

                    # Draw the cell
                    pygame.draw.rect(self.screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))
                    if cell.is_revealed and not cell.is_mine:
                        # Draw the number of adjacent mines
                        font = pygame.font.Font(None, 36)
                        text_surface = font.render(str(cell.adjacent_mines), True, BLACK)
                        self.screen.blit(text_surface, (x * cell_size + cell_size // 4, y * cell_size + cell_size // 4))



    def run_game(self):
        print(f"Starting game at difficulty: {self.difficulty}")
        # You can now proceed to your game logic here or move to the next screen
        self.initialize_board()  # Initialize the board
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Determine which cell was clicked
                    x = mouse_pos[0] // (SCREEN_WIDTH // self.board.get_size())
                    y = mouse_pos[1] // (SCREEN_HEIGHT // self.board.get_size())
                    if 0 <= x < self.board.get_size() and 0 <= y < self.board.get_size():
                        self.board.reveal_cell(0, y, x)  # Reveal the cell at (0, y, x) layer
                    
            # Clear the screen
            self.screen.fill(BLACK)
            # Draw the board
            self.draw_board()
            pygame.display.flip()


    def run(self):
        pygame.init()
        pygame.font.init()

        self.start_screen()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()

        pygame.quit()
        sys.exit()

