import random

class Cell:
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.adjacent_mines = 0

    def reveal(self):
        self.is_revealed = True


class Board:
    def __init__(self, size, num_mines):
        self._size = size
        self._num_mines = num_mines
        self._board = None

    def gen_board(self):
        # Create a 3D array of Cell objects
        self._board = [[[Cell() for _ in range(self._size)] for _ in range(self._size)] for _ in range(self._size)]
        self.generate_mines()
        self.count_adjacent_mines()

    def generate_mines(self):
        placed_mines = 0
        while placed_mines < self._num_mines:
            z = random.randint(0, self._size - 1)
            y = random.randint(0, self._size - 1)
            x = random.randint(0, self._size - 1)

            if not self._board[z][y][x].is_mine:
                self._board[z][y][x].is_mine = True
                placed_mines += 1

    def count_adjacent_mines(self):
        offsets = [(-1, -1, -1), (-1, -1, 0), (-1, -1, 1),
                   (-1, 0, -1) , (-1, 0, 0) , (-1, 0, 1),
                   (-1, 1, -1) , (-1, 1, 0) , (-1, 1, 1),
                   (0, -1, -1) , (0, -1, 0) , (0, -1, 1),
                   (0, 0, -1)  ,              (0, 0, 1),
                   (0, 1, -1)  , (0, 1, 0)  , (0, 1, 1),
                   (1, -1, -1) , (1, -1, 0) , (1, -1, 1),
                   (1, 0, -1)  , (1, 0, 0)  , (1, 0, 1),
                   (1, 1, -1)  , (1, 1, 0)  , (1, 1, 1)]

        for z in range(self._size):
            for y in range(self._size):
                for x in range(self._size):
                    if self._board[z][y][x].is_mine:
                        continue

                    mine_count = 0
                    for dz, dy, dx in offsets:
                        nz, ny, nx = z + dz, y + dy, x + dx
                        if 0 <= nz < self._size and 0 <= ny < self._size and 0 <= nx < self._size:
                            if self._board[nz][ny][nx].is_mine:
                                mine_count += 1

                    self._board[z][y][x].adjacent_mines = mine_count

    def reveal_cell(self, z, y, x):
        if 0 <= z < self._size and 0 <= y < self._size and 0 <= x < self._size:
            cell = self._board[z][y][x]
            if not cell.is_revealed:
                cell.reveal()


if __name__ == "__main__":
    # Example usage
    size = 5
    num_mines = 5
    board = Board(size, num_mines)
    board.gen_board()
