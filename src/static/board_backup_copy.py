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
        self.size = size
        self.num_mines = num_mines
        self.board = None
        self.revealed_ctr = 0

    
    def get_num_flags(self):
        cnt = 0
        for z in range(self.size):
            for y in range(self.size):
                for x in range(self.size):
                    if self.board[z][y][x].is_flagged:
                        cnt += 1
        return cnt
    
    def get_size(self):
        return self.size
    
    def get_num_mines(self):
        return self.num_mines
    
    def get_board(self):
        return self.board
    
    def get_revealed_ctr(self):
        return self.revealed_ctr
    
    def add_revealed_ctr(self):
        self.revealed_ctr += 1


    def gen_board(self):
        # Create a 3D array of Cell objects
        self.board = [[[Cell() for _ in range(self.size)] for _ in range(self.size)] for _ in range(self.size)]
        self.generate_mines()
        self.count_adjacent_mines()


    def generate_mines(self):
        placed_mines = 0
        while placed_mines < self.num_mines:
            z = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            x = random.randint(0, self.size - 1)

            if not self.board[z][y][x].is_mine:
                self.board[z][y][x].is_mine = True
                placed_mines += 1



    def count_adjacent_mines(self):
        for z in range(self.size):
            for y in range(self.size):
                for x in range(self.size):
                    if self.board[z][y][x].is_mine:
                        continue

                    mine_count = 0
                    for dz, dy, dx in self.OFFSETS:
                        nz, ny, nx = z + dz, y + dy, x + dx
                        if 0 <= nz < self.size and 0 <= ny < self.size and 0 <= nx < self.size:
                            if self.board[nz][ny][nx].is_mine:
                                mine_count += 1

                    self.board[z][y][x].adjacent_mines = mine_count



    def rotate(self, orient):
        temp_arr = [[[None for _ in range(self.size)] for _ in range(self.size)] for _ in range(self.size)]
        if orient == 'x': # x-rotation aka front rotation, col is fixed
            

            for layer in range(self.size):
                for col in range(self.size):
                    for row in range(self.size):
                        temp_arr[layer][row][col] = self.board[row][self.size - 1 - layer][col]

        elif orient == 'y': # y-rotation aka side rotation
            for layer in range(self.size):
                for col in range(self.size):
                    for row in range(self.size):
                        temp_arr[layer][row][col] = self.board[col][row][self.size - 1 - layer]

        else: # z-rotation aka face rotation

            for layer in range(self.size):

                # Performing Transpose
                for i in range(self.size):
                    for j in range(i + 1, self.size):
                        self.board[layer][i][j], self.board[layer][j][i] = self.board[layer][j][i], self.board[layer][i][j]

                #Reversing Columns
                for i in range(self.size):
                    for j in range(self.size//2):
                        self.board[layer][i][j], self.board[layer][i][self.size - 1 - j] = self.board[layer][i][self.size - 1 - j], self.board[layer][i][j]

            return
        
        for z in range(self.size):
            for i in range(self.size):
                for j in range(self.size):
                    self.board[z][i][j] = temp_arr[z][i][j]

        temp_arr = None #Clearing up memory



    def reveal_cell(self, h, r, c):
        if 0 <= h < self.size and 0 <= r < self.size and 0 <= c < self.size:
            cell = self.board[h][r][c]
            if not cell.is_revealed:
                cell.reveal()



    def display_complete_board(self): # Reveals all the cells
        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    self.board[i][j][k].reveal()



    def clear_zeros(self, h, r, c):
        queue = deque([(h, r, c)])
        self.board[h][r][c].set_reveal(False)

        while queue:
            curr_h, curr_r, curr_c = queue.popleft()

            if self.board[curr_h][curr_r][curr_c].is_revealed:
                continue
            
            self.board[curr_h][curr_r][curr_c].reveal()
            self.revealed_ctr += 1

            if self.board[curr_h][curr_r][curr_c].get_adj_mines() == 0:
                for dh, dr, dc in self.OFFSETS:
                    nh, nr, nc = curr_h + dh, curr_r + dr, curr_c + dc
                    if 0 <= nh < self.size and 0 <= nr < self.size and 0 <= nc < self.size:
                        if not self.board[nh][nr][nc].is_revealed:
                            queue.append((nh, nr, nc))




    def check_win(self):
        return self.revealed_ctr == self.size ** 3 - self.num_mines



    def check_lose(self, curr_layer, r, c):

        if self.board[curr_layer][r][c].get_is_mine() and self.board[curr_layer][r][c].get_is_revealed():
            return True
        
        return False


    def find_external_revealed(self): #Used to find Unique external revealed cells
        external_layer = set()  # Store unique external revealed cells
        for h in range(self.size):
            for r in range(self.size):
                for c in range(self.size):
                    cell = self.board[h][r][c]
                    if cell.get_is_revealed():
                        for dh, dr, dc in self.OFFSETS:
                            nh, nr, nc = h + dh, r + dr, c + dc
                            # Check if adjacent cell is unrevealed and within bounds
                            if 0 <= nh < self.size and 0 <= nr < self.size and 0 <= nc < self.size:
                                if not self.board[nh][nr][nc].get_is_revealed():
                                    external_layer.add((h, r, c))
                                    break  # Move to the next revealed cell
        return external_layer
    
    def find_external_unrevealed(self): #Returns unique unrevealed outer layer, if they are not flagged
        external_layer = self.find_external_revealed()

        external_unrevealed = set()
        for key in external_layer:
            #temp_set = set()
            for dh, dr, dc in self.OFFSETS:
                nh, nr, nc = key[0] + dh, key[1] + dr, key[2] + dc
                if 0 <= nh < self.size and 0 <= nr < self.size and 0 <= nc < self.size:
                    if not self.board[nh][nr][nc].get_is_revealed() and not self.board[nh][nr][nc].get_is_flagged():
                        #temp_set.add((nh, nr, nc))
                        external_unrevealed.add((nh, nr, nc))


        return sorted(external_unrevealed) #Start from top layer, first row, first col. for layer -> for row -> for col

    def get_total_nonlocal_unrevealed(self):
        external_unrevealed = self.find_external_unrevealed()

        nonlocal_unrevealed_cnt = 0
        nonlocal_unrevealed = set()

        for h in range(self.size):
            for r in range(self.size):
                for c in range(self.size):
                    cell = self.board[h][r][c]
                    if not cell.get_is_revealed() and (h, r, c) not in external_unrevealed:
                        nonlocal_unrevealed_cnt += 1
                        nonlocal_unrevealed.add((h, r, c))

        return nonlocal_unrevealed_cnt, nonlocal_unrevealed
    
    def linear_alg_solver(self):
        # To be implemented to try and reduce runtime
        pass
        
    

    async def find_possible_mine_layouts(self):
        # Gather external unrevealed cells as potential mine candidates
        potential_cells = self.find_external_unrevealed()
        layouts = []  # Store all valid layouts
        current_layout = {}

        async def backtrack(index, num_mines):

            if index == len(potential_cells):
                layouts.append(current_layout.copy())
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

            del current_layout[(h, r, c)]

        await backtrack(0, self.num_mines)
        return layouts

    def is_valid_configuration(self, layout, curr_pos):
        h, r, c = curr_pos

        for dh, dr, dc in self.OFFSETS:
            nh, nr, nc = h + dh, r + dr, c + dc

            if 0 <= nh < self.size and 0 <= nr < self.size and 0 <= nc < self.size:
                cell = self.board[nh][nr][nc]
                adj_mine_cnt = cell.get_adj_mines()
                total_adj_unrevealed = 0
                adj_referenced = 0
                curr_adj_mines = 0

                if cell.get_is_revealed():
                    for adj_dh, adj_dr, adj_dc in self.OFFSETS:
                        adj_nh, adj_nr, adj_nc = nh + adj_dh, nr + adj_dr, nc + adj_dc

                        if 0 <= adj_nh < self.size and 0 <= adj_nr < self.size and 0 <= adj_nc < self.size:
                            if not self.board[adj_nh][adj_nr][adj_nc].get_is_revealed():
                                total_adj_unrevealed += 1

                            if self.board[adj_nh][adj_nr][adj_nc].get_is_flagged(): #POSSIBLE EDGE CASE: MORE FLAGS THAN ACTUAL
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
        layouts = await self.find_possible_mine_layouts()
        total_poss_arr = 0

        non_local_pos = set()
        
        
        non_local_unrevealed, non_local_unrevealed_pos = self.get_total_nonlocal_unrevealed()
        for layout in layouts:

            num_mines_left =  self.num_mines
            for prob_mine in layout.values():
                if prob_mine == True:
                    num_mines_left -= 1

            if num_mines_left < 0:
                num_mines_left = 0

            poss_arr = math.comb(non_local_unrevealed, num_mines_left)
            total_poss_arr += poss_arr

            for pos, prob_mine in layout.items():
                if prob_mine == True:
                    self.board[pos[0]][pos[1]][pos[2]].set_mine_prob(self.board[pos[0]][pos[1]][pos[2]].get_mine_prob() + poss_arr)

            if non_local_unrevealed:
                if num_mines_left == 0:
                    num_mines_left += 1
                nonlocal_poss_ref = math.comb(non_local_unrevealed - 1, num_mines_left - 1)

                for pos in non_local_unrevealed_pos:
                    self.board[pos[0]][pos[1]][pos[2]].set_mine_prob(self.board[pos[0]][pos[1]][pos[2]].get_mine_prob() + nonlocal_poss_ref)
                    non_local_pos.add(pos)

        
        #Since all the different layouts have the same key, we only need the first layer
        for pos in layouts[0].keys():
            new_mine_prob = math.floor(100 - self.board[pos[0]][pos[1]][pos[2]].get_mine_prob() / total_poss_arr * 100) / 100

            self.board[pos[0]][pos[1]][pos[2]].set_mine_prob(new_mine_prob)

        if non_local_pos:
            for pos in non_local_pos:
                new_mine_prob = math.floor(100 - self.board[pos[0]][pos[1]][pos[2]].get_mine_prob() / total_poss_arr * 100) / 100

                self.board[pos[0]][pos[1]][pos[2]].set_mine_prob(new_mine_prob)


    def reset_probability(self):
        for h in range(self.size):
            for r in range(self.size):
                for c in range(self.size):
                    self.board[h][r][c].reset_mine_prob()