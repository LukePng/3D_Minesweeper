# This file is to test for the functionality of board.py

import random
from collections import deque

from test.pure_python.cell_test import Cell


class Board:

    OFFSETS = [(-1, -1, -1), (-1, -1, 0), (-1, -1, 1),
                   (-1, 0, -1) , (-1, 0, 0) , (-1, 0, 1),
                   (-1, 1, -1) , (-1, 1, 0) , (-1, 1, 1),
                   (0, -1, -1) , (0, -1, 0) , (0, -1, 1),
                   (0, 0, -1)  ,              (0, 0, 1),
                   (0, 1, -1)  , (0, 1, 0)  , (0, 1, 1),
                   (1, -1, -1) , (1, -1, 0) , (1, -1, 1),
                   (1, 0, -1)  , (1, 0, 0)  , (1, 0, 1),
                   (1, 1, -1)  , (1, 1, 0)  , (1, 1, 1)]

    def __init__(self, size, num_mines):
        self._size = size
        self._num_mines = num_mines
        self._board = None
        self._size = size

    def gen_board(self):
        # Create a 3D array of Cell objects
        self._board = [[[Cell() for _ in range(self._size)] for _ in range(self._size)] for _ in range(self._size)]
        self.generate_mines()
        self.count_adjacent_mines()

    def get_board(self):
        return self._board
    
    def get_size(self):
        return self._size

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
        for z in range(self._size):
            for y in range(self._size):
                for x in range(self._size):
                    if self._board[z][y][x].is_mine:
                        continue

                    mine_count = 0
                    for dz, dy, dx in self.OFFSETS:
                        nz, ny, nx = z + dz, y + dy, x + dx
                        if 0 <= nz < self._size and 0 <= ny < self._size and 0 <= nx < self._size:
                            if self._board[nz][ny][nx].is_mine:
                                mine_count += 1

                    self._board[z][y][x].adjacent_mines = mine_count

    def rotate(self, orient):
        temp_arr = [[[None for _ in range(self._size)] for _ in range(self._size)] for _ in range(self._size)]
        if orient == 'x': # x-rotation aka front rotation, col is fixed
            

            for layer in range(self._size):
                for col in range(self._size):
                    for row in range(self._size):
                        temp_arr[layer][row][col] = self._board[row][self._size - 1 - layer][col]

        elif orient == 'y': # y-rotation aka side rotation
            for layer in range(self._size):
                for col in range(self._size):
                    for row in range(self._size):
                        temp_arr[layer][row][col] = self._board[col][row][self._size - 1 - layer]

        else: # z-rotation aka face rotation

            for layer in range(self._size):

                # Performing Transpose
                for i in range(self._size):
                    for j in range(i + 1, self._size):
                        self._board[layer][i][j], self._board[layer][j][i] = self._board[layer][j][i], self._board[layer][i][j]

                #Reversing Columns
                for i in range(self._size):
                    for j in range(self._size//2):
                        self._board[layer][i][j], self._board[layer][i][self._size - 1 - j] = self._board[layer][i][self._size - 1 - j], self._board[layer][i][j]

            return
        
        for z in range(self._size):
            for i in range(self._size):
                for j in range(self._size):
                    self._board[z][i][j] = temp_arr[z][i][j]

    def reveal_cell(self, z, y, x):
        if 0 <= z < self._size and 0 <= y < self._size and 0 <= x < self._size:
            cell = self._board[z][y][x]
            if not cell.is_revealed:
                cell.reveal()

    def display_complete_board(self): # Top-down view
        for i in range(self._size):
            print(f"Layer {i}:")
            for j in range(self._size):
                for k in range(self._size):
                    cell = self._board[i][j][k]
                    # Represent the cell in display
                    if cell.is_mine:
                        display = 'M'  # Mine
                    else:
                        display = cell.adjacent_mines
                    print(display, end=' ')
                print()  # New line for the next row
            print() 

    def map_board(self):
        three_D_Board = self._board
        map_2d = {}

        for i in range(self._size):
            map_2d[i] = three_D_Board[i]

        return map_2d       

    def display_map_board(self, curr_layer):
        mapped = self.map_board()
        curr_board_layer = mapped[curr_layer]
        for r in range(self._size):
            for c in range(self._size):
                if curr_board_layer[r][c].get_is_revealed():
                    if curr_board_layer[r][c].get_is_mine():
                        display = "M"

                    else:
                        display = curr_board_layer[r][c].get_adj_mines()

                elif curr_board_layer[r][c].get_is_flagged():
                    display = 'F'

                else:
                    display = 'C'

                print(display, end=' ')
                
            print() 
    
    def clear_zeros(self, h, r, c):
        queue = deque([(h, r, c)])
        self._board[h][r][c].set_reveal(False)

        while queue:
            curr_h, curr_r, curr_c = queue.popleft()

            if self._board[curr_h][curr_r][curr_c].is_revealed:
                continue
            
            self._board[curr_h][curr_r][curr_c].reveal()

            if self._board[curr_h][curr_r][curr_c].get_adj_mines() == 0:
                for dh, dr, dc in self.OFFSETS:
                    nh, nr, nc = curr_h + dh, curr_r + dr, curr_c + dc
                    if 0 <= nh < self._size and 0 <= nr < self._size and 0 <= nc < self._size:
                        if not self._board[nh][nr][nc].is_revealed:
                            queue.append((nh, nr, nc))

    def check_win(self):
        for h in range(self._size):
            for r in range(self._size):
                for c in range(self._size):
                    if (not self._board[h][r][c].get_is_mine()) and (not self._board[h][r][c].get_is_revealed()):
                        return False
        return True
    
    def check_lose(self, curr_layer, r, c):

        if self._board[curr_layer][r][c].get_is_mine() and self._board[curr_layer][r][c].get_is_revealed():
            return True
        
        return False

# Testing
# size = 3
# num_mines = 5
# board = Board(size, num_mines)
# board.gen_board()

# board.display_complete_board()

# print('-'*18)
# board.rotate('x')
# board.display_complete_board()
# print('-'*18)
# board.rotate('x')
# board.display_complete_board()
# print('-'*18)
# board.rotate('x')
# board.display_complete_board()

# board.get_board()[1][1][1].reveal()
# board.get_board()[1][1][2].reveal()
# board.get_board()[1][2][1].reveal()
# board.get_board()[1][0][0].reveal()
# board.get_board()[1][0][2].flag()
# board.get_board()[1][0][2].flag()

# board.display_map_board(1)

