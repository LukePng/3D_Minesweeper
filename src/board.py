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

    def generate_mines(self):
        placed_mines = 0
        while placed_mines < self._num_mines:
            # Generate random coordinates
            z = random.randint(0, self._size - 1)
            y = random.randint(0, self._size - 1)
            x = random.randint(0, self._size - 1)

            # Check if the mine is already placed at that location
            if not self._board[z][y][x].is_mine:
                self._board[z][y][x].is_mine = True  # Place a mine
                placed_mines += 1

    def count_adjacent_mines(self):
        # Define the offsets for neighboring cells (3D)
        offsets = [
            (-1, -1, -1), (-1, -1, 0), (-1, -1, 1),
            (-1, 0, -1) , (-1, 0, 0) , (-1, 0, 1),
            (-1, 1, -1) , (-1, 1, 0) , (-1, 1, 1),
            (0, -1, -1) , (0, -1, 0) , (0, -1, 1),
            (0, 0, -1)  ,              (0, 0, 1),
            (0, 1, -1)  , (0, 1, 0)  , (0, 1, 1),
            (1, -1, -1) , (1, -1, 0) , (1, -1, 1),
            (1, 0, -1)  , (1, 0, 0)  , (1, 0, 1),
            (1, 1, -1)  , (1, 1, 0)  , (1, 1, 1)
        ]
        for z in range(self._size):
            for y in range(self._size):
                for x in range(self._size):
                    if self._board[z][y][x].is_mine:
                        continue  # Skip mines

                    # Count adjacent mines
                    mine_count = 0
                    for dz, dy, dx in offsets:
                        nz, ny, nx = z + dz, y + dy, x + dx
                        if 0 <= nz < self._size and 0 <= ny < self._size and 0 <= nx < self._size:
                            if self._board[nz][ny][nx].is_mine:
                                mine_count += 1

                    self._board[z][y][x].adjacent_mines = mine_count


    def get_size(self):
        return self._size

    def show_tiles(self):  # Displaying a 3D Array
        for i in range(self._size):
            print(f"Layer {i}:")
            for j in range(self._size):
                for k in range(self._size):
                    cell = self._board[i][j][k]
                    # Represent the cell in display
                    if cell.is_mine:
                        display_char = 'M'  # Mine
                    elif cell.is_revealed:
                        display_char = 'R'  # Revealed
                    else:
                        display_char = 'C'  # Covered
                    print(display_char, end=' ')
                print()  # New line for the next row
            print()  # New line for the next layer

    def show_numbers(self):
        self.count_adjacent_mines()
        for i in range(self._size):
            print(f"Layer {i}:")
            for j in range(self._size):
                for k in range(self._size):
                    cell = self._board[i][j][k]
                    # Represent the cell in display
                    if cell.is_mine:
                        display_char = 'M'  # Mine
                    else:
                        display_char = cell.adjacent_mines
                    print(display_char, end=' ')
                print()  # New line for the next row
            print() 

# Example usage
size = 5
num_mines = 25
board = Board(size, num_mines)
board.gen_board()
board.show_numbers()


                
    