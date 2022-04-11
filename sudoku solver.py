import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import sys
import pygame
import threading
from sudoku import Sudoku
from buttons import ToggleButton

def main():
    pygame.init()
    
    # Create and initialize window
    screen = pygame.display.set_mode((821, 950))
    pygame.display.set_caption('Nishant\'s Sudoku Solver')
    background = pygame.Surface((821,950))

    # Fonts
    script_dir = os.path.dirname(__file__)
    font_dir = './assets/font/PressStart2P-Regular.ttf'
    font = pygame.font.Font(os.path.join(script_dir, font_dir), 40)
    pencil_font = pygame.font.Font(os.path.join(script_dir, font_dir), 10)
    text_font = pygame.font.Font(os.path.join(script_dir, font_dir), 12)

    # Create buttons at correct locations
    buttons = []
    for i in range(10, 731, 90):
            for j in range(10, 731, 90):
                buttons.append(ToggleButton(background, (255, 255, 255), (200, 200, 200), (j, i, 81, 81), font, pencil_font))
    
    # List of unicode values that can be pressed (\x08 and x7f are backspace and delete keys)
    number_list = ['1','2','3','4','5','6','7','8','9', '\x08', '\x7f']

    # Create Board Class
    sudoku_board = Sudoku()

    # Set some initial values for board
    sudoku_board._board =   [[0,0,3,0,0,0,0,0,0],
                            [8,0,9,4,6,0,7,0,2],
                            [2,0,0,0,1,8,6,0,0],
                            [0,0,0,0,0,6,0,7,0],
                            [0,0,8,0,0,0,4,0,0],
                            [0,7,0,8,0,0,0,0,0],
                            [0,0,2,9,4,0,0,0,5],
                            [4,0,6,0,3,2,8,0,7],
                            [0,0,0,0,0,0,2,0,0]]
    
    for row in range(9):
        for col in range(9):
            if sudoku_board._board[row][col] != 0:
                sudoku_board._constants_board[row][col] = True


    # Create Pygame clock
    clock = pygame.time.Clock()

    # Create timer event
    

    # Create thread to run solve function
    thread = threading.Thread(target = sudoku_board.solve)
    thread.daemon = True
    has_run = False

    # Constant and Pencil Toggle
    constant = False
    pencil = False

    # Gameloop
    while True:
        
        # Event Loop
        for event in pygame.event.get():

            # Quit call. If sudoku is being solved, join thread and then quit
            if event.type == pygame.QUIT:
                if thread.is_alive(): 
                    thread.join(timeout=0.01)
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.KEYDOWN and not thread.is_alive():
                    if event.key == pygame.K_RETURN and sudoku_board.check_valid_board():
                        thread.start()
                        has_run = True
                    for button in buttons:
                        if button.clicked and event.unicode in number_list:

                            # Backspace or Delete pressed, delete number at button
                            if event.unicode in ['\x08', '\x7f']:
                                button.value = '0'
                                sudoku_board.change_board(button.coords[0], button.coords[1], 0)

                                if constant:
                                    sudoku_board.set_constant(button.coords[0], button.coords[1], 0)
                            else:                              
                                if constant:
                                    sudoku_board.set_constant(button.coords[0], button.coords[1], int(event.unicode))
                                    button.value = event.unicode
                                elif pencil:
                                    sudoku_board.pencil(button.coords[0], button.coords[1], int(event.unicode))
                                    button.value = '0'
                                else:
                                    sudoku_board.change_board(button.coords[0], button.coords[1], int(event.unicode))
                                    button.value = event.unicode
                    
                    if event.unicode == 'c':
                        if constant:
                            sudoku_board.clear_all()
                        elif pencil:
                            sudoku_board.clear_pencil()
                        else:
                            sudoku_board.clear()

                    if event.unicode == 'i':
                        sudoku_board.auto_pencil()

                    # Toggle Pencil mode
                    if event.unicode == 'p' and not constant:
                        pencil = not(pencil)

                    # Toggle Constant mode
                    if event.unicode == 'o' and not pencil:
                        constant = not(constant)

                    # Generate new board
                    if event.unicode == 'g':
                        sudoku_board.generate_board(28)

                    if event.key == pygame.K_ESCAPE: 
                        thread.join(timeout=0.01)

        # If thread has run and finished, join thread and create new one
        if not thread.is_alive() and has_run:
            thread.join()
            thread = threading.Thread(target= sudoku_board.solve)
            thread.daemon = True
            has_run = False

        # Fill screen and draw outlines
        screen.fill((0,0,0))
        pygame.draw.rect(background, (180,180,180), (10,10, 801, 801))
        for i in [(271, 10, 9, 801),(541, 10, 9, 801),(10, 271, 801, 9),(10, 541, 801, 9)]:
            pygame.draw.rect(background, (0,0,0), i)
        
        # Go through every button and update them
        temp = 0
        for i in range(9):
            for j in range(9):
                buttons[temp].change_value(str(sudoku_board._board[i][j]))
                buttons[temp].constant = sudoku_board._constants_board[i][j]
                buttons[temp].pencil_values = sudoku_board._pencil_board[i][j]
                buttons[temp].update()
                buttons[temp].coords = (i,j)
                temp += 1

        # Update incorrect cells
        incorrect_cells = sudoku_board.get_incorrect_cells()
        for coords in incorrect_cells:
            for button in buttons:
                if button.coords == coords:
                    button.incorrect = True

        # Draw all buttons
        for button in buttons:
            button.draw()
        screen.blit(background, (0, 0))
        
        # Render text
        text_surface = text_font.render('enter - solve    bkspc/del - delete    c - clear    g - generate', True, (255, 255, 255))
        text_rect = text_surface.get_rect(topleft = (10, 830))
        screen.blit(text_surface, text_rect)
        text_surface = text_font.render('Press cell and then number to input number', True, (255, 255, 255))
        text_rect = text_surface.get_rect(topleft = (10, 850))
        screen.blit(text_surface, text_rect)
        text_surface = text_font.render('auto pencil - i', True, (255, 255, 255))
        text_rect = text_surface.get_rect(topleft = (10, 870))
        screen.blit(text_surface, text_rect)
        text_surface = text_font.render('edit pencil - p', True, (0, 255, 0) if pencil else (255, 255, 255))
        text_rect = text_surface.get_rect(topleft = (210, 870))
        screen.blit(text_surface, text_rect)
        text_surface = text_font.render('edit constants - o', True, (0, 255, 0) if constant else (255, 255, 255))
        text_rect = text_surface.get_rect(topleft = (410, 870))
        screen.blit(text_surface, text_rect)

        pygame.display.update()
        clock.tick(120)



if __name__ == '__main__':
    main()
    