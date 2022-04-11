import random

class Sudoku():

    # Create Empty Board
    def __init__(self):
        self.N = 9
        self._board = [[0 for i in range(self.N)] for j in range(self.N)]
        self._pencil_board = [[set() for i in range(self.N)] for j in range(self.N)]
        self._constants_board = [[False for i in range(self.N)] for j in range(self.N)]
        self.counter = 0

    # Return String representation of Board
    def __str__(self):
        result = ''
        for row in self._board:
            for col in row:
                result += str(col) + ' '
            result += '\n'
        return result
    
    # Change value at row and col to given value
    def change_board(self, row, col, value):
        if not self._constants_board[row][col]:
            self._board[row][col] = value
            self._pencil_board[row][col] = set()
            self.update_pencil(row, col, value)
    
    # Change values that were set as constants
    def set_constant(self, row, col, value):
        self._constants_board[row][col] = False
        self.change_board(row, col, value)
        self._constants_board[row][col] = True if value != 0 else False
        self.update_pencil(row, col, value)

    def update_pencil(self, row, col, value):
        for i in range(self.N):
            self._pencil_board[row][i].discard(value)
        for i in range(self.N):
            self._pencil_board[i][col].discard(value)
        for i in range((row // 3 * 3), ((row + 3) // 3 * 3)):
            for j in range((col // 3 * 3), ((col + 3) // 3 * 3)):
                self._pencil_board[i][j].discard(value)



    def pencil(self, row, col, value):
        if self._board[row][col] == 0:
            if value in self._pencil_board[row][col]:
                self._pencil_board[row][col].discard(value)
            else:
                self._pencil_board[row][col].add(value)

    def auto_pencil(self):
        self._pencil_board = [[set() for i in range(self.N)] for j in range(self.N)]
        for i in range(self.N):
            for j in range(self.N):
                if self._board[i][j] == 0:
                    for k in range(self.N):
                        if self._check_valid(i,j,k + 1):
                            self.pencil(i, j, k + 1)

    def get_board(self):
        return self._board

    # Return true if given move is valid, otherwise return false
    def _check_valid(self, row, col, value):
        for i in range(self.N):
            if value == self._board[row][i] and i != col:
                return False
        for i in range(self.N):
            if value == self._board[i][col] and i != row:
                return False
        for i in range((row // 3 * 3), ((row + 3) // 3 * 3)):
            for j in range((col // 3 * 3), ((col + 3) // 3 * 3)):
                if value == self._board[i][j] and i != row and j != col:
                    return False
        return True
    
    # Return true if board can take more values, returns false otherwise
    def check_valid_board(self):
        for i in range(self.N):
            for j in range(self.N):
                if self._board[i][j] != 0 and not self._check_valid(i, j, self._board[i][j]):
                    return False
        return True

    # Get list of conflicting cells
    def get_incorrect_cells(self):
        result = []
        for i in range(self.N):
            for j in range(self.N):
                if self._board[i][j] != 0 and not self._check_valid(i, j, self._board[i][j]):
                    result.append((i,j))
        return result

    # Finds closest empty cell
    def _find_empty(self):
        for i in range(self.N):
            for j in range(self.N):
                if self._board[i][j] == 0:
                    return i, j
        return self.N + 1, self.N + 1

    # Recursively calls itself, using back tracking algorithm
    def solve(self):
        self._pencil_board = [[set() for i in range(self.N)] for j in range(self.N)]
        row, col = self._find_empty()
        if row == self.N + 1:
            return True
        for i in range(1, self.N + 1):
            if self._check_valid(row, col, i):
                self._board[row][col] = i                
                self.counter += 1
                if self.solve():
                    return True
        self._board[row][col] = 0
        return False
    
    def clear(self):
        for i in range(self.N):
            for j in range(self.N):
                if not self._constants_board[i][j]:
                    self._board[i][j] = 0
                    self._pencil_board[i][j] = set()

    def clear_all(self):
        for i in range(self.N):
            for j in range(self.N):
                self._board[i][j] = 0
                self._constants_board[i][j] = False
                self._pencil_board[i][j] = set()
    
    def clear_pencil(self):
        self._pencil_board = [[set() for i in range(self.N)] for j in range(self.N)]

    # Generate board
    def generate_board(self, num_cells):
        
        # Empty Board
        self.clear_all()

        # Generate random diagonal
        for i in range(9):
            while self._board[i][i] == 0:
                val = random.randint(1,9)
                if self._check_valid(i, i, val):
                    self._board[i][i] = val

        # Complete Board
        self.solve()

        # Remove random cells
        while num_cells < 81:
            row = random.randint(1,9) - 1
            col = random.randint(1,9) - 1

            if self._board[row][col] != 0:
                self._board[row][col] = 0
                num_cells += 1

        # Set constants
        for i in range(9):
            for j in range(9):
                if self._board[i][j] != 0:
                    self._constants_board[i][j] = True
        



if __name__ == '__main__':
    x = Sudoku()
    x._board = [[0,6,0,0,0,0,0,3,2],
                [8,0,9,0,0,0,0,7,5],
                [0,0,0,6,0,0,8,0,0],
                [0,3,0,2,0,0,0,0,0],
                [4,0,6,0,1,0,0,0,0],
                [0,1,0,4,0,7,0,0,0],
                [2,0,3,0,7,0,0,5,8],
                [0,0,0,3,0,0,0,0,0],
                [7,0,0,0,0,0,0,9,0]]
    if x.solve():
        print('\033c')
        print(x)
    else:
        print('No solution found')