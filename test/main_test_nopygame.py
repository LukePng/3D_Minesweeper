from board_test import Board

def create_board(difficulty):
    if difficulty == 0: #Easy
        board = Board(3, 2)

    elif difficulty == 1: #Medium
        board = Board(7, 10)

    else: #Hard
        board = Board(10, 35)

    return board


run = True

while run:
    print("Welcome to 3D Minesweeper! Please choose a difficulty")
    print("1 - Easy\t2 - Medium\t 3 - Hard\t4 - Quit")
    diff = int(input("Please enter the difficulty level: "))

    if diff == 4:
        run = False
        continue

    elif diff == 1:
        Minesweeper = create_board(0)
        
    elif diff == 2:
        Minesweeper = create_board(1)

    else:
        Minesweeper = create_board(2)

    Minesweeper.gen_board()

    game_end = False
    curr_layer = 0

    while not game_end:
        print(f"""
------------------------------------------------            
Current Layer: {curr_layer + 1}
""")
        Minesweeper.display_map_board(curr_layer)

        print("""
Enter "w" to move to a layer above, and "s" to move to a layer below
Enter in the format 'row, col, R' to reveal a cell 
Enter in the format 'row, col, F' to flag a cell
Enter x to rotate forwards
Enter y to rotate sideways
Enter z to turn the cube
""")
        choice = input('Enter Choice Here: ')

        if choice == 'w':
            if curr_layer == 0:
                print("You are currently at the top layer!")

            else:
                curr_layer -= 1

            continue

        elif choice == 's':
            if curr_layer == Minesweeper.get_size() - 1:
                print("You are currently at the bottom layer!")

            else:
                curr_layer += 1

            continue

        elif choice == 'x':
            Minesweeper.rotate('x')
            continue

        elif choice == 'y':
            Minesweeper.rotate('y')
            continue
        
        elif choice == 'z':
            Minesweeper.rotate('z')
            continue

        else:
            r, c, action = choice.split(', ')
            r = int(r) - 1
            c = int(c) - 1


            if action == 'R':
                if Minesweeper.get_board()[curr_layer][r][c].get_is_revealed(): 
                    print('The cell you are trying to reveal has already been revealed!')


                elif Minesweeper.get_board()[curr_layer][r][c].get_is_flagged():
                    print('The cell you are trying to reveal is flagged!')

                else:
                    
                    Minesweeper.get_board()[curr_layer][r][c].reveal()

                    if Minesweeper.check_lose(curr_layer, r, c):
                        print('Oh no, you have hit a mine! Try again next time')
                        Minesweeper.display_complete_board()
                        game_end = True

                    elif Minesweeper.get_board()[curr_layer][r][c].get_adj_mines() == 0:
                        Minesweeper.clear_zeros(curr_layer, r, c)
        
    
                    if Minesweeper.check_win():
                        Minesweeper.display_complete_board
                        print('Hooray! You have found all the mines! Congratulations!')
                        game_end = True
                
            
            else:
                if Minesweeper.get_board()[curr_layer][r][c].get_is_revealed(): 
                    print('The cell you are trying to flag has already been revealed!')
                else:
                    Minesweeper.get_board()[curr_layer][r][c].flag()

            

