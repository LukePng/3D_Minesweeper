
def map_ex_revealed(self):
    mapped_ex_revealed = {}
    ex_revealed = self.find_external_revealed()

    for i in ex_revealed:
        h, r, c = ex_revealed[i]
        temp_lst = []

        for dh, dr, dc in self.OFFSETS:
            nh, nr, nc = h + dh, r + dr, c + dc

            if not self._board[nh][nr][nc].get_is_revealed():
                temp_lst.append((nh, nr, nc))

        mapped_ex_revealed[(h, r, c)] = temp_lst



def linalg_solver(self):
    pass