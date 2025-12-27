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

    def __init__(self, dimension, num_mines):
        self.dim = dimension
        self.size = dimension ** 3
        self.num_mines = num_mines
        self.board = [Cell() for _ in range(self.size)]
        self.revealed_ctr = 0
        # Pre-calculating neighbors to prevent the "wrap-around" bug and speeds up loops
        self.adj_map = self._build_adjacency_map()

    def _build_adjacency_map(self):
        #Maps every flat index to its valid 3D neighbor indices once
        adj_map = {}
        for idx in range(self.size):
            z = idx // (self.dim ** 2)
            y = (idx // self.dim) % self.dim
            x = idx % self.dim
            
            neighbors = []
            for dz, dy, dx in self.OFFSETS:
                nz, ny, nx = z + dz, y + dy, x + dx
                if 0 <= nz < self.dim and 0 <= ny < self.dim and 0 <= nx < self.dim:
                    neighbors.append(nz * self.dim**2 + ny * self.dim + nx)
            adj_map[idx] = neighbors
        return adj_map

#==============GETTER/SETTER METHODS==============#
    def get_num_flags(self):
        cnt = 0
        for cell in self.board:
            if cell.is_flagged:
                cnt += 1
        return cnt
    
    def get_size(self):
        return self.size
    
    def get_dim(self):
        return self.dim
    
    def get_num_mines(self):
        return self.num_mines
    
    def get_board(self):
        return self.board
    
    def get_revealed_ctr(self):
        return self.revealed_ctr
    
    def add_revealed_ctr(self):
        self.revealed_ctr += 1

    def flatten_coord(self, x, y, z):
        return z * self.dim ** 2 + y * self.dim + x
    
    def get_cell(self, x, y, z):
        return self.board[self.flatten_coord(x, y, z)]
#==============BOARD LOGIC==============#
    def gen_board(self):
        # Create a 3D array of Cell objects
        self.generate_mines()
        self.count_adjacent_mines()

    def generate_mines(self):
        # Optimized to use random.sample for unique flat indices
        mine_indices = random.sample(range(self.size), self.num_mines)
        for idx in mine_indices:
            self.board[idx].is_mine = True

    def count_adjacent_mines(self):
        for idx in range(self.size):
            if self.board[idx].is_mine:
                continue

            mine_count = 0
            for neighbor_idx in self.adj_map[idx]:
                if self.board[neighbor_idx].is_mine:
                    mine_count += 1

            self.board[idx].adjacent_mines = mine_count

    def reveal_cell(self, z, y, x):
        idx = self.flatten_coord(x, y, z)
        if 0 <= idx < self.size:
            if not self.board[idx].is_revealed:
                self.board[idx].reveal()

    def display_complete_board(self): # Reveals all the cells
        for cell in self.board:
            cell.reveal()

    def clear_zeros(self, z, y, x):
        idx = self.flatten_coord(x, y, z)
        if idx == -1 or self.board[idx].get_is_revealed():
            return

        queue = deque([idx])
        
        self.board[idx].reveal()
        self.revealed_ctr += 1

        while queue:
            curr_idx = queue.popleft()
            
            # Only spread if the current revealed cell is a "0"
            if self.board[curr_idx].get_adj_mines() == 0:
                for neighbor_idx in self.adj_map[curr_idx]:
                    neighbor = self.board[neighbor_idx]
                    
                    # If neighbor isn't revealed and isn't a mine
                    if not neighbor.get_is_revealed() and not neighbor.get_is_mine():
                        # REVEAL IT NOW before adding to queue to prevent duplicates
                        neighbor.reveal()
                        self.revealed_ctr += 1
                        
                        # Only add to queue to keep spreading if the neighbor is also a 0
                        if neighbor.get_adj_mines() == 0:
                            queue.append(neighbor_idx)

    def rotate(self, orient):
        temp_arr = [None] * self.size

        for idx in range(self.size):
            x = idx % self.dim
            y = idx // self.dim % self.dim
            z = idx // self.dim // self.dim

            if orient == 'x': # x-rotation aka front rotation, col is fixed
                nz, ny, nx = y, (self.dim - 1 - z), x 

            elif orient == 'y': # y-rotation aka side rotation
                nz, ny, nx = x, y, (self.dim - 1 - z)

            else: #  z-rotation aka face rotation
                nz, ny, nx = z, x, (self.dim - 1 - y)

            new_idx = self.flatten_coord(nx, ny, nz)
            temp_arr[new_idx] = self.board[idx]
        
        for idx in range(self.size):
            self.board[idx] = temp_arr[idx]

        temp_arr = None #Clearing up memory

    def check_win(self):
        print(self.revealed_ctr)
        print(self.size, self.num_mines)
        return self.revealed_ctr == self.size - self.num_mines

    def check_lose(self, curr_layer, y, x):
        idx = self.flatten_coord(x, y, curr_layer)
        if self.board[idx].get_is_mine() and self.board[idx].get_is_revealed():
            return True
        return False

    def find_external_revealed(self): #Used to find Unique external revealed cells
        external_layer = set()  # Store unique external revealed cells
        for idx in range(self.size):
            cell = self.board[idx]
            if cell.get_is_revealed():
                for neighbor_idx in self.adj_map[idx]:
                    # Check if adjacent cell is unrevealed
                    if not self.board[neighbor_idx].get_is_revealed():
                        external_layer.add(idx)
                        break  # Move to the next revealed cell
        return external_layer
    
    def find_external_unrevealed(self): #Returns unique unrevealed outer layer, if they are not flagged
        external_layer = self.find_external_revealed()

        external_unrevealed = set()
        for idx in external_layer:
            for neighbor_idx in self.adj_map[idx]:
                if not self.board[neighbor_idx].get_is_revealed() and not self.board[neighbor_idx].get_is_flagged():
                    external_unrevealed.add(neighbor_idx)

        return sorted(external_unrevealed)
    
    def get_total_nonlocal_unrevealed(self):
        external_unrevealed = set(self.find_external_unrevealed())

        nonlocal_unrevealed_cnt = 0
        nonlocal_unrevealed = set()

        for idx in range(self.size):
            cell = self.board[idx]
            if not cell.get_is_revealed() and idx not in external_unrevealed:
                nonlocal_unrevealed_cnt += 1
                nonlocal_unrevealed.add(idx)

        return nonlocal_unrevealed_cnt, nonlocal_unrevealed

#==============AUTOSOLVER==============#
    async def find_possible_mine_layouts(self):
        potential_cells = self.find_external_unrevealed()
        layouts = []
        current_layout = {}

        async def backtrack(pos, mines_to_place):

            if pos == len(potential_cells):
                layouts.append(current_layout.copy())
                return

            idx = potential_cells[pos]

            # Case 1: Assume No Mine
            current_layout[idx] = False
            # Aggressive Pruning: Does this 'False' make a number impossible to satisfy?
            if self.is_valid_configuration(current_layout, idx):
                await backtrack(pos + 1, mines_to_place)

            # Case 2: Assume Mine
            if mines_to_place > 0:
                current_layout[idx] = True
                # Aggressive Pruning: Does this 'True' exceed any revealed numbers?
                if self.is_valid_configuration(current_layout, idx):
                    await backtrack(pos + 1, mines_to_place - 1)

            del current_layout[idx]

        await backtrack(0, self.num_mines)
        return layouts

    def is_valid_configuration(self, layout, curr_idx):
        # We check every revealed number touching the cell we just toggled
        for neighbor_idx in self.adj_map[curr_idx]:
            target_cell = self.board[neighbor_idx]
            
            if target_cell.get_is_revealed():
                target_mines = target_cell.get_adj_mines()
                
                current_mines = 0
                possible_future_mines = 0

                # Look at ALL neighbors of the revealed number
                for n_idx in self.adj_map[neighbor_idx]:
                    neighbor = self.board[n_idx]
                    
                    if neighbor.get_is_flagged():
                        current_mines += 1
                    elif n_idx in layout:
                        if layout[n_idx]:
                            current_mines += 1
                    elif not neighbor.get_is_revealed():
                        # This cell hasn't been assigned yet by the backtrack
                        possible_future_mines += 1

                # RULE 1: Too many mines already assigned/flagged
                if current_mines > target_mines:
                    return False
                
                # RULE 2 (Aggressive Pruning): 
                # Even if every remaining unassigned cell is a mine, 
                # we still can't reach the target number.
                if current_mines + possible_future_mines < target_mines:
                    return False
                
        return True

    async def calc_probability(self):
        layouts = await self.find_possible_mine_layouts()
        if not layouts: return
        
        total_poss_arr = 0
        non_local_idx_list = set()
        non_local_unrevealed_ctr, non_local_unrevealed_pos = self.get_total_nonlocal_unrevealed()

        for layout in layouts:
            num_mines_left = self.num_mines - sum(layout.values())

            if num_mines_left < 0:
                num_mines_left = 0

            poss_arr = math.comb(non_local_unrevealed_ctr, num_mines_left)
            total_poss_arr += poss_arr

            for idx, prob_mine in layout.items():
                if prob_mine:
                    self.board[idx].set_mine_prob(self.board[idx].get_mine_prob() + poss_arr)

            if non_local_unrevealed_ctr > 0 and num_mines_left > 0:
                nonlocal_poss_ref = math.comb(non_local_unrevealed_ctr - 1, num_mines_left - 1)
                for idx in non_local_unrevealed_pos:
                    self.board[idx].set_mine_prob(self.board[idx].get_mine_prob() + nonlocal_poss_ref)
                    non_local_idx_list.add(idx)

        # Finalize probabilities
        for idx in layouts[0].keys():
            new_mine_prob = math.floor(100 - self.board[idx].get_mine_prob() / total_poss_arr * 100) / 100
            self.board[idx].set_mine_prob(new_mine_prob)

        for idx in non_local_idx_list:
            new_mine_prob = math.floor(100 - self.board[idx].get_mine_prob() / total_poss_arr * 100) / 100
            self.board[idx].set_mine_prob(new_mine_prob)

    def reset_probability(self):
        for idx in range(self.size):
            self.board[idx].reset_mine_prob()

 