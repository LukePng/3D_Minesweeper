import pygame
import sys
import asyncio

from static.constants import *
from static.board import Board
from game_logic.game_screen import GameScreen
from game_logic.start_screen import StartScreen
from game_logic.end_screen import EndScreen
from game_logic.cheat_screen import CheatScreen

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("3D Minesweeper")
        self.difficulty = 0
        self.is_end = False
        self.hovering = False
        self.board = None



    def get_board(self):
        return self.board



    def set_hovering(self, new_hover):
        self.hovering = new_hover
    
    def get_hovering(self):
        return self.hovering



    def set_is_end(self, new_status):
        self.is_end = new_status
        
    def get_is_end(self):
        return self.is_end



    def set_difficulty(self, level):
        self.difficulty = level

    def get_difficulty(self):
        return self.difficulty



    def initialize_board(self):
        board_params = {0: (3, 2), 1: (5, 20), 2: (10, 100)}
        size, num_mines = board_params[self.difficulty]
        self.board = Board(size, num_mines)
        self.board.gen_board()



    def click_actions(self, event, board_size, curr_layer, first_click, cheat):
        mouse_pos = pygame.mouse.get_pos()

        available_width = SCREEN_WIDTH - 2 * SIDE_MARGIN
        available_height = SCREEN_HEIGHT - TOP_MARGIN - SIDE_MARGIN
        cell_size = min(available_width // board_size, available_height // board_size)

        left_margin = (SCREEN_WIDTH - cell_size * board_size) // 2
        top_margin = TOP_MARGIN + (available_height - cell_size * board_size) // 2

        adjusted_mouse_x = mouse_pos[0] - left_margin
        adjusted_mouse_y = mouse_pos[1] - top_margin

        if 0 <= adjusted_mouse_x < cell_size * board_size and 0 <= adjusted_mouse_y < cell_size * board_size:
            # Determine which cell was clicked
            x = adjusted_mouse_x // cell_size
            y = adjusted_mouse_y // cell_size

            X, Y = int(x), int(y)

            if 0 <= x < board_size and 0 <= y < board_size:
                if event.button == 1:  # Left-click
                    if self.board.get_board()[curr_layer][Y][X].get_is_flagged():
                        return  # Cell cannot be clicked onto if flagged
                    else:
                        if first_click:
                            while (self.board.get_board()[curr_layer][Y][X].get_adj_mines() != 0) or (self.board.get_board()[curr_layer][Y][X].get_is_mine()):
                                self.initialize_board()
                            
                            self.game_screen.set_first_click()

                        self.board.reveal_cell(curr_layer, Y, X)  # Reveal the cell

                        if (self.board.get_board()[curr_layer][Y][X].get_adj_mines() == 0) and (not self.board.get_board()[curr_layer][Y][X].get_is_mine()):
                            self.board.clear_zeros(curr_layer, Y, X)

                        # Check lose condition
                        if self.board.check_lose(curr_layer, Y, X):
                            self.display_end_screen("Game Over! You hit a mine.")
                            self.is_end == True

                        # Check win condition
                        elif self.board.check_win():
                            self.display_end_screen("Congratulations! You won!")
                            self.is_end == True
                
                        elif cheat:
                            self.board.reset_probability()
                            asyncio.run(self.board.calc_probability())
                            print('Done!')


                elif event.button == 3:  # Right-click
                    if self.board.get_board()[curr_layer][Y][X].get_is_revealed():
                        return
                    else:
                        self.board.get_board()[curr_layer][Y][X].flag()  # Flag the cell



    def rotation_actions(self, event):
        if event.key == pygame.K_w:
            self.board.rotate('x')

        elif event.key == pygame.K_s:
            self.board.rotate('x')
            self.board.rotate('x')
            self.board.rotate('x')

        elif event.key == pygame.K_a:
            self.board.rotate('y')

        elif event.key == pygame.K_d:
            self.board.rotate('y')
            self.board.rotate('y')
            self.board.rotate('y')

        elif event.key == pygame.K_r:
            self.board.rotate('z')

        elif event.key == pygame.K_f:
            self.board.rotate('z')
            self.board.rotate('z')
            self.board.rotate('z')



    def display_start_screen(self):
        self.is_end = False
        self.start_screen = StartScreen(self)
        self.start_screen.display()


    def run_game(self):
        self.initialize_board()  # Initialize the board
        self.game_screen = GameScreen(self, self.screen)
        self.game_screen.display_board()

    def display_cheat_screen(self):
        self.display_cheat_screen = CheatScreen(self, self.screen)
        self.cheat_screen.display()


    def display_end_screen(self, message):
        self.end_screen = EndScreen(self, self.screen)
        self.end_screen.display(message)



    #Starting programme
    def run(self):
        pygame.init()
        pygame.font.init()

        pygame.mixer.init()  # Ensure mixer is initialized
        try:
            pygame.mixer.music.load('src/assets/music/bgm.mp3')  # Load the music file from vsc
        except:
            pygame.mixer.music.load('assets\music\\bgm.mp3')  # Load the music file from commmand prompt 
        pygame.mixer.music.play(-1, 0.0)  # Loop indefinitely

        self.display_start_screen()

    def quit_game(self):
        pygame.quit()
        sys.exit()
    