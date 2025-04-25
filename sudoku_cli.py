from sudoku_solver import solve_sudoku, print_board
from optimized_solver import solve_optimized
import time
import copy
import sudoku

def parse_board_input():
    # Get a 9x9 Sudoku board from user input, validating each row
    print("Enter the Sudoku board row by row (use '.' for empty cells).")
    board = []
    
    for i in range(9):
        while True:
            row_input = input(f"Row {i+1}: ")
            
            # Make sure input is valid: 9 characters, all either digits or dots
            if len(row_input) != 9 or not all(c in "123456789." for c in row_input):
                print("Invalid input! Each row must contain 9 characters (digits 1-9 or '.').")
                continue
            
            board.append(list(row_input))
            break
    
    return board

def load_example():
    # Use the sudoku library to generate puzzles based on difficulty
    try:
        # Attempt to use the 'sudoku' library to generate puzzles
        pass  # Replace this with actual logic if needed
    except ImportError:
        # Handle the case where the 'py-sudoku' package is not installed
        print("The 'py-sudoku' package is required. Install it with: pip install py-sudoku")
        print("Falling back to predefined examples...")
        return load_predefined_example()
    
    print("Select difficulty level:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    
    # Get user choice and generate a puzzle with corresponding difficulty
    while True:
        choice = input("Enter choice (1/2/3): ")
        if choice == "1":
            # Generate an easy puzzle
            puzzle = sudoku.generate(difficulty=0.3)
            return convert_puzzle_format(puzzle)
        elif choice == "2":
            # Generate a medium puzzle
            puzzle = sudoku.generate(difficulty=0.5)
            return convert_puzzle_format(puzzle)
        elif choice == "3":
            # Generate a hard puzzle
            puzzle = sudoku.generate(difficulty=0.7)
            return convert_puzzle_format(puzzle)
        else:
            print("Invalid choice. Try again.")

def convert_puzzle_format(puzzle):
    # Convert puzzle from sudoku library format to our expected format
    result = []
    for row in puzzle.board:
        new_row = []
        for cell in row:
            if cell == 0:  # Empty cells are typically represented as 0
                new_row.append(".")
            else:
                new_row.append(str(cell))
        result.append(new_row)
    return result

def load_predefined_example():
    # Fallback function with predefined examples
    examples = {
        "easy": [
            ["5", "3", ".", ".", "7", ".", ".", ".", "."],
            ["6", ".", ".", "1", "9", "5", ".", ".", "."],
            [".", "9", "8", ".", ".", ".", ".", "6", "."],
            ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
            ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
            ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
            [".", "6", ".", ".", ".", ".", "2", "8", "."],
            [".", ".", ".", "4", "1", "9", ".", ".", "5"],
            [".", ".", ".", ".", "8", ".", ".", "7", "9"]
        ],
        "medium": [
            [".", ".", "9", "7", "4", "8", ".", ".", "."],
            ["7", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", "2", ".", "1", ".", "9", ".", ".", "."],
            [".", ".", "7", ".", ".", ".", "2", "4", "."],
            [".", "6", "4", ".", "1", ".", "5", "9", "."],
            [".", "9", "8", ".", ".", ".", "3", ".", "."],
            [".", ".", ".", "8", ".", "3", ".", "2", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "6"],
            [".", ".", ".", "2", "7", "5", "9", ".", "."]
        ],
        "hard": [
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", "3", ".", "8", "5"],
            [".", ".", "1", ".", "2", ".", ".", ".", "."],
            [".", ".", ".", "5", ".", "7", ".", ".", "."],
            [".", ".", "4", ".", ".", ".", "1", ".", "."],
            [".", "9", ".", ".", ".", ".", ".", ".", "."],
            ["5", ".", ".", ".", ".", ".", ".", "7", "3"],
            [".", ".", "2", ".", "1", ".", ".", ".", "."],
            [".", ".", ".", ".", "4", ".", ".", ".", "9"]
        ]
    }
    
    # Get user choice and return the corresponding puzzle
    while True:
        choice = input("Enter choice (1/2/3): ")
        if choice == "1":
            return examples["easy"]
        elif choice == "2":
            return examples["medium"]
        elif choice == "3":
            return examples["hard"]
        else:
            print("Invalid choice. Try again.")

def main():
    # Main program that handles the interface and solving process
    print("=== SUDOKU SOLVER ===")
    
    # Let the user choose between example puzzles or custom input
    print("\nOptions:")
    print("1. Use example puzzle")
    print("2. Enter your own puzzle")
    
    while True:
        choice = input("\nChoice (1/2): ")
        
        if choice == "1":
            board = load_example()
            break
        elif choice == "2":
            board = parse_board_input()
            break
        else:
            print("Invalid choice. Try again.")
    
    # Display the input puzzle
    print("\nInput Puzzle:")
    print_board(board)
    
    # Let the user choose which solver to use
    print("\nSolver method:")
    print("1. Basic solver")
    print("2. Optimized solver (faster)")
    
    while True:
        solver_choice = input("\nChoice (1/2): ")
        
        if solver_choice in ["1", "2"]:
            break
        else:
            print("Invalid choice. Try again.")
    
    # Make a copy of the board so we don't modify the original
    board_copy = copy.deepcopy(board)
    
    print("\nSolving...")
    start_time = time.time()
    
    # Solve using the selected algorithm
    if solver_choice == "1":
        result = solve_sudoku(board_copy)
        end_time = time.time()
        print(f"Basic solver time: {end_time - start_time:.4f} seconds")
    else:
        result = solve_optimized(board_copy)
    
    # Display the solution or error message
    if result:
        print("\nSolution:")
        print_board(board_copy)
    else:
        print("\nNo solution exists!")

if __name__ == "__main__":
    main() 