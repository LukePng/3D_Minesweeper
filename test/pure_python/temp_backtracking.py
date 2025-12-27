import math
import asyncio

async def find_possible_mine_layouts(self):
        # Gather external unrevealed cells as potential mine candidates
    potential_cells = self.find_external_unrevealed()
    layouts = []  # Store all valid layouts
    current_layout = {}

    async def backtrack(index, num_mines):
        
        if is_valid_configuration(current_layout):
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
            await backtrack(index + 1, num_mines)

        # Undo the assumption for backtracking
        del current_layout[(h, r, c)]


    # Initialize the backtracking process
    for num_mines in range(len(potential_cells)): 
        if num_mines > self._num_mines:
            continue # Number of mines is more than the total on the board, therefore fails

        else:
            for idx in range(num_mines):
                current_layout[potential_cells[idx]] == True

            
            await backtrack(num_mines, num_mines)

    return layouts


#### BETTER BACKTRACKING ALGORITHMN
"""
Instead of parsing through all the different possibilities through backtracking, divide and conquer with a set amount of mines

For i in range(total number of external mines):
    backtracking(total number of mines)

tasks = [async_task(i) for i in range(5)]
await asyncio.gather(*tasks)
    
Before, need to traverse through all the possibilities, able to run multiple backtracking methods at a same time by async

However, this change defines the number of mines possible, from no mines to all mines, and everything can be run asynchronously

Total number of possibilities = nCr

Total number of external unrevealed cells = n
Number of mines = r (to be given into the function)



"""

def is_valid_configuration(self, layout):
    """
    Helper function to check if the current mine layout configuration is valid.
    It ensures the adjacent mine counts for revealed cells match the board's requirements.
    """
    for h, r, c in self.find_external_revealed():
        adj_mine_cnt = self._board[h][r][c].get_adj_mines()
        total_adj_unrevealed = 0
        adj_referenced = 0
        curr_adj_mines = 0
        
        
        for dh, dr, dc in self.OFFSETS:
            nh, nr, nc = h + dh, r + dr, c + dc


            if 0 <= nh < self._size and 0 <= nr < self._size and 0 <= nc < self._size:
                if not self._board[nh][nr][nc].get_is_revealed():
                    total_adj_unrevealed += 1

                if self._board[nh][nr][nc].get_is_flagged(): #POSSIBLE EDGE CASE: MORE FLAGS THAN ACTUAL
                    adj_mine_cnt -= 1



            if (nh, nr, nc) in layout:
            

                adj_referenced += 1
                if layout[(nh, nr, nc)]:
                    curr_adj_mines += 1
        # Verify if this revealed cell's count matches the board's expected mine count
        if curr_adj_mines > adj_mine_cnt:
            return False
        
        elif total_adj_unrevealed - adj_referenced + curr_adj_mines < adj_mine_cnt:
            return False

            
    return True