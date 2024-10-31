def _old_is_valid(self, layout):
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