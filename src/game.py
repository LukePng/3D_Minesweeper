### TO DO LIST ###
# 1. GIVE UP button
# 3. EXIT GAME button

from board import Board
from button import Button

import pygame
import sys

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

SIDE_MARGIN = 50
TOP_MARGIN = 200

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("3D Minesweeper")
        self.difficulty = 0
        self.selected_button = None

    #Miscellanous Functions
    def set_easy(self):
        self.difficulty = 0

    def set_medium(self):
        self.difficulty = 1

    def set_hard(self):
        self.difficulty = 2

    def give_up(self):
        self.display_end_screen("You gave up. Better luck next time!", True)

    def click_actions(self, event, board_size, curr_layer, first_click):
        mouse_pos = pygame.mouse.get_pos()

        available_width = SCREEN_WIDTH - 2 * SIDE_MARGIN
        available_height = SCREEN_HEIGHT - TOP_MARGIN - SIDE_MARGIN
        cell_size = min(available_width // board_size, available_height // board_size)

        left_margin = (SCREEN_WIDTH - cell_size * board_size) // 2
        top_margin = TOP_MARGIN + (available_height - cell_size * board_size) // 2

        adjusted_mouse_x = mouse_pos[0] - left_margin
        adjusted_mouse_y = mouse_pos[1] - top_margin

        if 0 <= adjusted_mouse_x < cell_size * board_size and 0 <= adjusted_mouse_y < cell_size * board_size:
            # Determine which cell was clicked
            x = adjusted_mouse_x // cell_size
            y = adjusted_mouse_y // cell_size

            X, Y = int(x), int(y)

            if 0 <= x < board_size and 0 <= y < board_size:
                if event.button == 1:  # Left-click
                    if self.board.get_board()[curr_layer][Y][X].is_flagged:
                        return  # Cell cannot be clicked onto if flagged
                    else:
                        if first_click:
                            while (self.board.get_board()[curr_layer][Y][X].get_adj_mines() != 0) or (self.board.get_board()[curr_layer][Y][X].is_mine):
                                self.initialize_board()
                            
                            first_click = False

                        self.board.reveal_cell(curr_layer, Y, X)  # Reveal the cell

                        if (self.board.get_board()[curr_layer][Y][X].get_adj_mines() == 0) and (not self.board.get_board()[curr_layer][Y][X].is_mine):
                            self.board.clear_zeros(curr_layer, Y, X)

                        # Check lose condition
                        if self.board.check_lose(curr_layer, Y, X):
                            self.display_end_screen("Game Over! You hit a mine.", True)
                            game_over = True

                        # Check win condition
                        if self.board.check_win():
                            self.display_end_screen("Congratulations! You won!", False)
                            game_over = True

                elif event.button == 3:  # Right-click
                    self.board.get_board()[curr_layer][Y][X].flag()  # Flag the cell

    def rotation_actions(self, event):
        if event.key == pygame.K_w:
            self.board.rotate('x')

        elif event.key == pygame.K_s:
            self.board.rotate('x')
            self.board.rotate('x')
            self.board.rotate('x')

        elif event.key == pygame.K_a:
            self.board.rotate('y')

        elif event.key == pygame.K_d:
            self.board.rotate('y')
            self.board.rotate('y')
            self.board.rotate('y')

        elif event.key == pygame.K_r:
            self.board.rotate('z')

        elif event.key == pygame.K_f:
            self.board.rotate('z')
            self.board.rotate('z')
            self.board.rotate('z')

    #Generating Different display screens
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
                                button.action()  # Set the difficulty
                            elif button.text == "Start Game":
                                button.action()  # Start the game

    def display_end_screen(self, message, is_end):
        #Display the end screen with buttons for New Puzzle and View Board
        font = pygame.font.Font(None, 74)
        text_surface = font.render(message, True, RED)
        self.screen.fill(BLACK)
        self.screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

        # Create buttons for end screen
        self.end_buttons = [
            Button("New Puzzle", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50), GREEN, 50, action=self.start_screen, border_color=WHITE, border_width=3),
            Button("View Board", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150), BLUE, 50, action=self.show_board, border_color=WHITE, border_width=3)
        ]

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
                            button.action()  # Perform the action for the clicked button

    def show_board(self):
        self.board.display_complete_board()
        curr_layer = 0

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            if curr_layer == 0:
                                print("Already at the top!")
                            else:
                                curr_layer = curr_layer - 1

                        elif event.key == pygame.K_DOWN:
                            if curr_layer == (self.board.get_size() - 1):
                                print("Already at the bottom!")
                            else:
                                curr_layer = curr_layer + 1

                self.screen.fill(BLACK)
                self.draw_board(curr_layer)  # Optionally, you can pass a layer here
                pygame.display.flip()

    #Generating Board
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

    def draw_board(self, layer=0):
        board_size = self.board.get_size()
        flags_left = self.board.get_num_mines() - self.board.get_num_flags()  # Calculate flags left
        # Create a font object for drawing text
        font = pygame.font.Font(None, 36)  # You can adjust the font size as needed

        layer_text = font.render(f"Layer: {layer + 1}/{board_size}", True, WHITE)
        flags_text = font.render(f"Flags left: {flags_left}", True, WHITE)

        self.screen.blit(layer_text, (SIDE_MARGIN, 50))  # Position the layer text
        self.screen.blit(flags_text, (SIDE_MARGIN, 100))  # Position the flags text

        give_up_button = Button("Give Up", (SCREEN_WIDTH - SIDE_MARGIN - 100, 50), RED, 30, action=self.give_up, border_color=WHITE, border_width=2)

        give_up_button.draw(self.screen)

        available_width = SCREEN_WIDTH - 2 * SIDE_MARGIN
        available_height = SCREEN_HEIGHT - TOP_MARGIN - SIDE_MARGIN

        cell_size = min(available_width // board_size, available_height // board_size)

        left_margin = (SCREEN_WIDTH - cell_size * board_size) // 2
        top_margin = TOP_MARGIN + (available_height - cell_size * board_size) // 2

        for y in range(board_size):
            for x in range(board_size):
                cell = self.board.get_board()[layer][y][x]
                if not cell.is_revealed:
                    color = BLUE if cell.is_flagged else GREEN #flag is blue, unflagged and unrevealed is green
                
                elif cell.is_mine:
                    color = RED #mine is red

                else:
                    color = WHITE #safe is whtie

                # Calculate cell position
                rect = pygame.Rect(
                    left_margin + x * cell_size, 
                    top_margin + y * cell_size, 
                    cell_size, 
                    cell_size
                )
                
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

                if cell.is_revealed and not cell.is_mine:
                    font = pygame.font.Font(None, 36)
                    text_surface = font.render(str(cell.adjacent_mines), True, BLACK)
                    text_rect = text_surface.get_rect()
                                    
                    # Center the text in the cell
                    text_rect.center = (
                        left_margin + x * cell_size + cell_size // 2,
                        top_margin + y * cell_size + cell_size // 2
                     )
                
                    # Blit the text surface at the new centered position
                    self.screen.blit(text_surface, text_rect)

    #Main Game
    def run_game(self):
        self.initialize_board()  # Initialize the board
        curr_layer = 0 #initialising first layer at 0
        board_size = self.board.get_size()
        game_over = False
        first_click = True
        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if not game_over:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button in [1, 2, 3]:
                            self.click_actions(event, board_size, curr_layer, first_click)
                            first_click = False

                        else:
                            # event.button 4 and 5 are for scrolling
                            if event.button == 4:
                                if curr_layer > 0:
                                    curr_layer -= 1

                            else:
                                if curr_layer < (board_size - 1):
                                    curr_layer += 1 


                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            if curr_layer == 0:
                                print("Already at the top!")
                            else:
                                curr_layer -= 1

                        elif event.key == pygame.K_DOWN:
                            if curr_layer == (board_size - 1):
                                print("Already at the bottom!")
                            else:
                                curr_layer += 1

                        else:
                            self.rotation_actions(event)


                else:  # Game is over; handle the end screen buttons
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        for button in self.end_buttons:
                            if button.is_clicked(mouse_pos):
                                if button.text == "New Puzzle":
                                    self.start_screen()  # Go back to start screen
                                    running = False  # End the current game loop
                                elif button.text == "View Board":
                                    self.display_complete_board()  # Show the complete board

                self.screen.fill(BLACK)
                if not game_over:
                    self.draw_board(curr_layer)
                pygame.display.flip()

        pygame.quit()
        sys.exit()

    #Starting programme
    def run(self):
        pygame.init()
        pygame.font.init()

        #pygame.mixer.init()  # Ensure mixer is initialized
        #pygame.mixer.music.load('src/assets/music/bgm.mp3')  # Load the music file
        #pygame.mixer.music.play(-1, 0.0)  # Loop indefinitely

        self.start_screen()

