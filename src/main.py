import pygame as pg
from board import Board

# Constants for the screen size, cell size, and margin
screen_WIDTH, screen_HEIGHT = 1000, 600
CELL_SIZE = 40
MARGIN = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

pg.init()
screen = pg.display.set_mode((screen_WIDTH, screen_HEIGHT))
pg.display.set_caption("3D Minesweeper")

# Font for text rendering
font = pg.font.SysFont(None, 40)

def create_board(difficulty):
    if difficulty == 0:  # Easy
        board = Board(3, 2)
    elif difficulty == 1:  # Medium
        board = Board(7, 66)
    else:  # Hard
        board = Board(10, 250)
    return board

def draw_board(Minesweeper, curr_layer):
    """Draw the board of the current layer on the screen."""
    board = Minesweeper.get_board()[curr_layer]
    for row in range(Minesweeper.get_size()):
        for col in range(Minesweeper.get_size()):
            x = col * (CELL_SIZE + MARGIN)
            y = row * (CELL_SIZE + MARGIN) + 100  # Adjust for the header

            cell = board[row][col]

            # Determine the color of the cell based on its state
            if cell.get_is_revealed():
                color = GRAY
                if cell.get_is_mine():
                    color = RED  # Revealed mine is red
            elif cell.get_is_flagged():
                color = BLUE  # Flagged cells are blue
            else:
                color = WHITE  # Unrevealed cells are white

            # Draw the cell (filled rectangle)
            pg.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))

            # Draw the border for visibility
            pg.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 2)  # Border width 2

            # If the cell is revealed and not a mine, display the adjacent mines count
            if cell.get_is_revealed() and not cell.get_is_mine() and cell.get_adj_mines() > 0:
                text = font.render(str(cell.get_adj_mines()), True, BLACK)
                screen.blit(text, (x + CELL_SIZE // 3, y + CELL_SIZE // 3))

def draw_difficulty_selection():
    """Draw difficulty selection options on the screen."""
    options = ["1 - Easy", "2 - Medium", "3 - Hard", "4 - Quit"]
    for i, option in enumerate(options):
        text = font.render(option, True, BLACK)
        screen.blit(text, (50, 50 + i * 30))  # Adjust Y position for each option

def draw_current_layer(curr_layer):
    """Draw the current layer information on the screen."""
    layer_text = f"Current Layer: {curr_layer + 1}"
    text = font.render(layer_text, True, BLACK)
    screen.blit(text, (50, 20))  # Display current layer at the top

def draw_message(message):
    """Draw a message on the screen."""
    text = font.render(message, True, RED)
    screen.blit(text, (screen_WIDTH // 2 - text.get_width() // 2, screen_HEIGHT - 50))

def main():
    run = True
    difficulty = None

    while run:
        # Display the welcome message and difficulty choice
        screen.fill(WHITE)
        draw_difficulty_selection()
        pg.display.flip()

        # Wait for difficulty choice
        while difficulty is None:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

                # Handle difficulty selection
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        difficulty = 0
                    elif event.key == pg.K_2:
                        difficulty = 1
                    elif event.key == pg.K_3:
                        difficulty = 2
                    elif event.key == pg.K_4:
                        run = False
                        difficulty = None

    if difficulty is not None:
        Minesweeper = create_board(difficulty)
        Minesweeper.gen_board()

        game_end = False
        curr_layer = 0

        # Game loop
        while not game_end:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    game_end = True

                # Handle left click (reveal) and right click (flag)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()
                    clicked_row = (mouse_pos[1] - 100) // (CELL_SIZE + MARGIN)
                    clicked_col = mouse_pos[0] // (CELL_SIZE + MARGIN)

                    if event.button == 1:  # Left click (Reveal)
                        if 0 <= clicked_row < Minesweeper.get_size() and 0 <= clicked_col < Minesweeper.get_size():
                            if not Minesweeper.get_board()[curr_layer][clicked_row][clicked_col].get_is_revealed():
                                Minesweeper.reveal_cell(curr_layer, clicked_row, clicked_col)
                                
                                if Minesweeper.check_lose(curr_layer, clicked_row, clicked_col):
                                    draw_message('Oh no, you hit a mine!')
                                    Minesweeper.display_complete_board()
                                    game_end = True

                                elif Minesweeper.get_board()[curr_layer][clicked_row][clicked_col].get_adj_mines() == 0:
                                    Minesweeper.clear_zeros(curr_layer, clicked_row, clicked_col)

                                if Minesweeper.check_win():
                                    draw_message('Congratulations, you won!')
                                    game_end = True

                    elif event.button == 3:  # Right click (Flag)
                        if 0 <= clicked_row < Minesweeper.get_size() and 0 <= clicked_col < Minesweeper.get_size():
                            Minesweeper.get_board()[curr_layer][clicked_row][clicked_col].flag()

                # Handle layer switching with 'W' and 'S'
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_w:  # Move up a layer
                        if curr_layer > 0:
                            curr_layer -= 1
                        else:
                            draw_message("You are at the top layer!")

                    elif event.key == pg.K_s:  # Move down a layer
                        if curr_layer < Minesweeper.get_size() - 1:
                            curr_layer += 1
                        else:
                            draw_message("You are at the bottom layer!")

            # Draw updated board and handle rendering
            screen.fill(WHITE)
            draw_board(Minesweeper, curr_layer)
            draw_current_layer(curr_layer)
            pg.display.flip()

if __name__ == "__main__":
    main()
    pg.quit()
