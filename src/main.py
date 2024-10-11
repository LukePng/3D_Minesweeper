import pygame
from board import Board

# Constants
CELL_SIZE = 40
ARROW_SIZE = 30
WIDTH, HEIGHT = 600, 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

class MinesweeperGame:
    def __init__(self, board_size, num_mines):
        self.board = Board(board_size, num_mines)
        self.board.gen_board()
        self.current_layer = 0

    
# Example usage
if __name__ == "__main__":
    size = 5
    num_mines = 5
    game = MinesweeperGame(size, num_mines)
    game.run()
