class Cell:
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.adjacent_mines = 0
        self.is_flagged = False

    def reveal(self):
        self.is_revealed = True

    def set_reveal(self, new_state):
        self.is_revealed = new_state #A boolean operator

    def flag(self):
        self.is_flagged = not self.get_is_flagged()

    def get_adj_mines(self):
        return self.adjacent_mines
    
    def get_is_mine(self):
        return self.is_mine
    
    def get_is_revealed(self):
        return self.is_revealed
    
    def get_is_flagged(self):
        return self.is_flagged
    