def solve_sudoku(board):
    # Main solving function using backtracking algorithm
    empty_cell = find_empty(board)
    
    if not empty_cell:
        return True
    
    row, col = empty_cell
    
    for digit in range(1, 10):
        str_digit = str(digit)
        
        if is_valid(board, row, col, str_digit):
            # Try placing this digit and see if it leads to a solution
            board[row][col] = str_digit
            
            if solve_sudoku(board):
                return True
            
            # If we get here, this digit didn't work, so backtrack
            board[row][col] = "."
    
    return False

def find_empty(board):
    # Find first empty cell in the board (represented by '.')
    for row in range(9):
        for col in range(9):
            if board[row][col] == ".":
                return (row, col)
    return None

def is_valid(board, row, col, digit):
    # Check if digit can be placed at board[row][col] according to Sudoku rules
    
    # Check row for conflicts
    for x in range(9):
        if board[row][x] == digit:
            return False
    
    # Check column for conflicts
    for x in range(9):
        if board[x][col] == digit:
            return False
    
    # Check 3x3 box for conflicts
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == digit:
                return False
    
    return True

def print_board(board):
    # Print the board with row/column separators for better readability
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            
            if j == 8:
                print(board[i][j])
            else:
                print(board[i][j], end=" ")

if __name__ == "__main__":
    # Example board - dots represent empty cells
    board = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"]
    ]
    
    print("Sudoku Puzzle:")
    print_board(board)
    
    solve_sudoku(board)
    
    print("\nSolution:")
    print_board(board) 