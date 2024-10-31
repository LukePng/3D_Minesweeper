import random
import math
from collections import deque
import asyncio

from static.cell import Cell


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
    
    def get_num_mines(self):
        return self._num_mines
    
    def get_num_flags(self):
        cnt = 0
        for z in range(self._size):
            for y in range(self._size):
                for x in range(self._size):
                    if self._board[z][y][x].is_flagged:
                        cnt += 1

        return cnt



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

        temp_arr = None #Clearing up memory



    def reveal_cell(self, h, r, c):
        if 0 <= h < self._size and 0 <= r < self._size and 0 <= c < self._size:
            cell = self._board[h][r][c]
            if not cell.is_revealed:
                cell.reveal()



    def display_complete_board(self): # Reveals all the cells
        for i in range(self._size):
            for j in range(self._size):
                for k in range(self._size):
                    self._board[i][j][k].reveal()



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


    def find_external_revealed(self): #Used to find Unique external revealed cells
        external_layer = set()  # Store unique external revealed cells
        for h in range(self._size):
            for r in range(self._size):
                for c in range(self._size):
                    cell = self._board[h][r][c]
                    if cell.get_is_revealed():
                        for dh, dr, dc in self.OFFSETS:
                            nh, nr, nc = h + dh, r + dr, c + dc
                            # Check if adjacent cell is unrevealed and within bounds
                            if 0 <= nh < self._size and 0 <= nr < self._size and 0 <= nc < self._size:
                                if not self._board[nh][nr][nc].get_is_revealed():
                                    external_layer.add((h, r, c))
                                    break  # Move to the next revealed cell
        return external_layer
    
    def find_external_unrevealed(self): #Returns unique unrevealed outer layer, if they are not flagged
        external_layer = self.find_external_revealed()

        external_unrevealed = set()
        for key in external_layer:
            temp_set = set()
            for dh, dr, dc in self.OFFSETS:
                nh, nr, nc = key[0] + dh, key[1] + dr, key[2] + dc
                if 0 <= nh < self._size and 0 <= nr < self._size and 0 <= nc < self._size:
                    if not self._board[nh][nr][nc].get_is_revealed() and not self._board[nh][nr][nc].get_is_flagged():
                        temp_set.add((nh, nr, nc))
                        external_unrevealed.add((nh, nr, nc))


        return sorted(external_unrevealed) #Start from top layer, first row, first col. for layer -> for row -> for col

    def get_total_nonlocal_unrevealed(self):
        external_unrevealed = self.find_external_unrevealed()

        nonlocal_unrevealed_cnt = 0
        nonlocal_unrevealed = set()

        for h in range(self._size):
            for r in range(self._size):
                for c in range(self._size):
                    cell = self._board[h][r][c]
                    if not cell.get_is_revealed() and (h, r, c) not in external_unrevealed:
                        nonlocal_unrevealed_cnt += 1
                        nonlocal_unrevealed.add((h, r, c))

        return nonlocal_unrevealed_cnt, nonlocal_unrevealed
    

    async def find_possible_mine_layouts(self):
        # Gather external unrevealed cells as potential mine candidates
        potential_cells = self.find_external_unrevealed()
        layouts = []  # Store all valid layouts
        current_layout = {}

        async def backtrack(index, num_mines):

            if index == len(potential_cells):
                layouts.append(current_layout.copy())
                print('added!')
                return


            h, r, c = potential_cells[index]

            # Case 1: Assume no mine here
            current_layout[(h, r, c)] = False
            if self.is_valid_configuration(current_layout, (h, r, c)):
                await backtrack(index + 1, num_mines)

            # Case 2: Assume a mine here
            current_layout[(h, r, c)] = True
            if self.is_valid_configuration(current_layout, (h, r, c)):
                await backtrack(index + 1, num_mines - 1)

            # Undo the assumption for backtracking
            del current_layout[(h, r, c)]


        # Initialize the backtracking process
        await backtrack(0, self._num_mines)
        return layouts

    def is_valid_configuration(self, layout, curr_pos):
        h, r, c = curr_pos

        for dh, dr, dc in self.OFFSETS:
            nh, nr, nc = h + dh, r + dr, c + dc

            if 0 <= nh < self._size and 0 <= nr < self._size and 0 <= nc < self._size:
                cell = self._board[nh][nr][nc]
                adj_mine_cnt = cell.get_adj_mines()
                total_adj_unrevealed = 0
                adj_referenced = 0
                curr_adj_mines = 0

                if cell.get_is_revealed():
                    for adj_dh, adj_dr, adj_dc in self.OFFSETS:
                        adj_nh, adj_nr, adj_nc = nh + adj_dh, nr + adj_dr, nc + adj_dc

                        if 0 <= adj_nh < self._size and 0 <= adj_nr < self._size and 0 <= adj_nc < self._size:
                            if not self._board[adj_nh][adj_nr][adj_nc].get_is_revealed():
                                total_adj_unrevealed += 1

                            if self._board[adj_nh][adj_nr][adj_nc].get_is_flagged(): #POSSIBLE EDGE CASE: MORE FLAGS THAN ACTUAL
                                adj_mine_cnt -= 1

                        if (adj_nh, adj_nr, adj_nc) in layout:
                            adj_referenced += 1

                            if layout[(adj_nh, adj_nr, adj_nc)]:
                                curr_adj_mines += 1

                    # Verify if this revealed cell's count matches the board's expected mine count
                    if curr_adj_mines > adj_mine_cnt:
                        return False
                    
                    elif total_adj_unrevealed - adj_referenced + curr_adj_mines < adj_mine_cnt:
                        return False
                
        return True


    async def calc_probability(self):
        #for nonlocal unrevealed, number of different combinations = nCr, where n is the number of nonlocal unrevealed and r is the number of mines
        layouts = await self.find_possible_mine_layouts()
        total_poss_arr = 0

        non_local_pos = set()

        for layout in layouts:
            non_local_unrevealed, non_local_unrevealed_pos = self.get_total_nonlocal_unrevealed()

            num_mines_left =  self._num_mines
            for prob_mine in layout.values():
                if prob_mine == True:
                    num_mines_left -= 1

            if num_mines_left < 0:
                num_mines_left = 0

            poss_arr = math.comb(non_local_unrevealed, num_mines_left)
            total_poss_arr += poss_arr

            for pos, prob_mine in layout.items():
                if prob_mine == True:
                    self._board[pos[0]][pos[1]][pos[2]].set_mine_prob(self._board[pos[0]][pos[1]][pos[2]].get_mine_prob() + poss_arr)

            if non_local_unrevealed:
                if num_mines_left == 0:
                    num_mines_left += 1
                nonlocal_poss_ref = math.comb(non_local_unrevealed - 1, num_mines_left - 1)

                for pos in non_local_unrevealed_pos:
                    self._board[pos[0]][pos[1]][pos[2]].set_mine_prob(self._board[pos[0]][pos[1]][pos[2]].get_mine_prob() + nonlocal_poss_ref)
                    non_local_pos.add(pos)

        
        #Since all the different layouts have the same key, we only need the first layer
        for pos in layouts[0].keys():
            new_mine_prob = math.floor(100 - self._board[pos[0]][pos[1]][pos[2]].get_mine_prob() / total_poss_arr * 100) / 100

            self._board[pos[0]][pos[1]][pos[2]].set_mine_prob(new_mine_prob)

        if non_local_pos:
            for pos in non_local_pos:
                new_mine_prob = math.floor(100 - self._board[pos[0]][pos[1]][pos[2]].get_mine_prob() / total_poss_arr * 100) / 100

                self._board[pos[0]][pos[1]][pos[2]].set_mine_prob(new_mine_prob)


    def reset_probability(self):
        for h in range(self._size):
            for r in range(self._size):
                for c in range(self._size):
                    self._board[h][r][c].reset_mine_prob()