import pygame
import sys

from static.button import Button
from static.constants import *



class GameScreen:
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen
        self.curr_layer = 0
        self.first_click = True
        self.board_size = self.game.get_board().get_size()

        self.give_up_button = Button("Give Up", (SCREEN_WIDTH - SIDE_MARGIN - 100, 100), RED, 30, action=self.give_up, border_color=WHITE, border_width=1)
        self.quit_button = Button("Quit Game", (SCREEN_WIDTH - SIDE_MARGIN - 100, 50), RED, 30, action=self.game.display_start_screen, border_color=WHITE, border_width=1)

        self.end_buttons = [self.give_up_button, self.quit_button]

        try:
            self.tiles_image = pygame.image.load("src\\assets\image\\tile.png").convert()
            self.flagged_image = pygame.image.load("src\\assets\image\\flagged_tile.png").convert()
            self.mine_image = pygame.image.load("src\\assets\image\\mine.png").convert()
        except:
            self.tiles_image = pygame.image.load("src/assets/image/tile.png").convert()
            self.flagged_image = pygame.image.load("src/assets/image/flagged_tile.png").convert()
            self.mine_image = pygame.image.load("src/assets/image/mine.png").convert()



    def set_first_click(self):
        self.first_click = False
    
    def get_first_click(self):
        return self.first_click



    def display_board(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if not self.game.get_is_end():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.give_up_button.is_clicked(pygame.mouse.get_pos()):
                            self.give_up_button.action()

                        elif self.quit_button.is_clicked(pygame.mouse.get_pos()):
                            self.quit_button.action()
                            
                        elif event.button in [1, 2, 3]:
                            self.game.click_actions(event, self.board_size, self.curr_layer, self.first_click)
                            

                        else:
                            # event.button 4 and 5 are for scrolling
                            if event.button == 4:
                                if self.curr_layer > 0:
                                    self.curr_layer -= 1

                            else:
                                if self.curr_layer < (self.board_size - 1):
                                    self.curr_layer += 1 


                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            if self.curr_layer == 0:
                                print("Already at the top!")
                            else:
                                self.curr_layer -= 1

                        elif event.key == pygame.K_DOWN:
                            if self.curr_layer == (self.board_size - 1):
                                print("Already at the bottom!")
                            else:
                                self.curr_layer += 1

                        else:
                            self.game.rotation_actions(event)


                else:  # Game is over; handle the end screen buttons
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        for button in self.end_buttons:
                            if button.is_clicked(mouse_pos):
                                if button.text == "New Puzzle":
                                    self.start_screen()  # Go back to start screen
                                    running = False  # End the current game loop
                                elif button.text == "View Board":
                                    self.display_complete_board()  # Show the complete board

            self.screen.fill(BLACK)

            if not self.game.get_is_end():
                self.draw_board()

            pygame.display.flip()
                


    def show_board(self):
            self.game.get_board().display_complete_board()
            self.curr_layer = 0

            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            if self.curr_layer == 0:
                                print("Already at the top!")
                            else:
                                self.curr_layer -= 1

                        elif event.key == pygame.K_DOWN:
                            if self.curr_layer == (self.game.get_board().get_size() - 1):
                                print("Already at the bottom!")
                            else:
                                self.curr_layer += 1

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.quit_button.is_clicked(pygame.mouse.get_pos()):
                            self.quit_button.action()

                self.screen.fill(BLACK)
                self.draw_board()
                pygame.display.flip()



    def draw_board(self):
        board_size = self.game.board.get_size()
        flags_left = self.game.board.get_num_mines() - self.game.board.get_num_flags()

        font = pygame.font.Font(None, 36)
        
        layer_text = font.render(f"Layer: {self.curr_layer + 1}/{board_size}", True, WHITE)
        flags_text = font.render(f"Flags left: {flags_left}", True, WHITE)

        self.screen.blit(layer_text, (SIDE_MARGIN, 50))
        self.screen.blit(flags_text, (SIDE_MARGIN, 100))
        
        self.quit_button.draw(self.screen)
        if not self.game.get_is_end():
            self.give_up_button.draw(self.screen)

        available_width = SCREEN_WIDTH - 2 * SIDE_MARGIN
        available_height = SCREEN_HEIGHT - TOP_MARGIN - SIDE_MARGIN
        
        cell_size = min(available_width // board_size, available_height // board_size)
        
        left_margin = (SCREEN_WIDTH - cell_size * board_size) // 2
        top_margin = TOP_MARGIN + (available_height - cell_size * board_size) // 2

        for y in range(board_size):
            for x in range(board_size):
                cell = self.game.board.get_board()[self.curr_layer][y][x]
        
                # color = BLUE if cell.is_flagged else GREEN if not cell.is_revealed else RED if cell.is_mine else WHITE
                rect = pygame.Rect(left_margin + x * cell_size, top_margin + y * cell_size, cell_size, cell_size)
                
                # pygame.draw.rect(self.screen, color, rect)
                # pygame.draw.rect(self.screen, WHITE, rect, 1)

                if cell.get_is_flagged() and not self.game.get_is_end(): # Flagged tiles will dissapear after game ends
                    image = pygame.transform.scale(self.flagged_image, (cell_size, cell_size))
                    self.screen.blit(image, rect)

                elif not cell.get_is_revealed():
                    image = pygame.transform.scale(self.tiles_image, (cell_size, cell_size))
                    self.screen.blit(image, rect)

                elif cell.get_is_mine():
                    image = pygame.transform.scale(self.mine_image, (cell_size, cell_size))
                    self.screen.blit(image, rect)
                    pygame.draw.rect(self.screen, DARKGREY, rect, 2)

                else: #If the tile does not contains a mine and is revealed
                    pygame.draw.rect(self.screen, GREY, rect)
                    pygame.draw.rect(self.screen, DARKGREY, rect, 2)

                if cell.get_is_revealed() and not cell.get_is_mine():
                    text_surface = font.render(str(cell.adjacent_mines), True, BLACK)
                    text_rect = text_surface.get_rect(center=(rect.centerx, rect.centery))
        
                    self.screen.blit(text_surface, text_rect)



    def give_up(self):
        self.game.display_end_screen("You gave up. Better luck next time!")
