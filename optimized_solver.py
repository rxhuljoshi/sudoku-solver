from collections import defaultdict
import time

class OptimizedSudokuSolver:
    # Class that implements an enhanced solving algorithm using constraint propagation
    def __init__(self):
        # Initialize data structures for tracking constraints and possibilities
        self.possibilities = {}  # Stores possible values for each cell
        self.row_used = defaultdict(set)  # Values used in each row
        self.col_used = defaultdict(set)  # Values used in each column
        self.box_used = defaultdict(set)  # Values used in each 3x3 box
        self.cell_to_box = {}  # Maps cell coordinates to box index
        self.board = None  # The Sudoku board
        self.empty_cells = set()  # Set of empty cell coordinates
    
    def initialize(self, board):
        # Set up initial state and calculate constraints from the board
        self.board = [row[:] for row in board]
        
        # Map each cell to its corresponding 3x3 box
        for row in range(9):
            for col in range(9):
                box_idx = (row // 3) * 3 + (col // 3)
                self.cell_to_box[(row, col)] = box_idx
        
        # Track which values are already used in each row, column and box
        for row in range(9):
            for col in range(9):
                value = board[row][col]
                if value != ".":
                    self.row_used[row].add(value)
                    self.col_used[col].add(value)
                    box_idx = self.cell_to_box[(row, col)]
                    self.box_used[box_idx].add(value)
                else:
                    self.empty_cells.add((row, col))
        
        # Calculate initial possibilities for each empty cell
        for row, col in self.empty_cells:
            self.update_possibilities(row, col)
    
    def update_possibilities(self, row, col):
        # Calculate what values can legally be placed in a cell
        if (row, col) not in self.empty_cells:
            return set()
            
        box_idx = self.cell_to_box[(row, col)]
        
        # Start with all digits 1-9
        possible = set(str(d) for d in range(1, 10))
        
        # Remove values that would violate constraints
        possible -= self.row_used[row]
        possible -= self.col_used[col]
        possible -= self.box_used[box_idx]
        
        self.possibilities[(row, col)] = possible
        return possible
    
    def find_mrv_cell(self):
        # Find the cell with minimum remaining values (most constrained)
        if not self.empty_cells:
            return None
            
        # Return the cell with the fewest possible values
        return min(
            self.empty_cells, 
            key=lambda cell: len(self.possibilities.get(cell, set())) or float('inf')
        )
    
    def place_value(self, row, col, value):
        # Assign a value to a cell and update all constraints
        self.board[row][col] = value
        self.empty_cells.remove((row, col))
        self.possibilities.pop((row, col), None)
        
        # Update constraint sets
        box_idx = self.cell_to_box[(row, col)]
        self.row_used[row].add(value)
        self.col_used[col].add(value)
        self.box_used[box_idx].add(value)
        
        # Find cells affected by this placement
        affected_cells = set()
        
        # Cells in the same row
        for c in range(9):
            if c != col and (row, c) in self.empty_cells:
                affected_cells.add((row, c))
        
        # Cells in the same column
        for r in range(9):
            if r != row and (r, col) in self.empty_cells:
                affected_cells.add((r, col))
        
        # Cells in the same 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if (r != row or c != col) and (r, c) in self.empty_cells:
                    affected_cells.add((r, c))
        
        # Update possibilities for all affected cells
        for r, c in affected_cells:
            self.update_possibilities(r, c)
    
    def remove_value(self, row, col, value):
        # Remove a value during backtracking, reversing constraints
        self.board[row][col] = "."
        self.empty_cells.add((row, col))
        
        # Update constraint sets
        box_idx = self.cell_to_box[(row, col)]
        self.row_used[row].remove(value)
        self.col_used[col].remove(value)
        self.box_used[box_idx].remove(value)
        
        # Recalculate possibilities for this cell
        self.update_possibilities(row, col)
        
        # Update affected cells in the same row, column, or box
        for r in range(9):
            for c in range(9):
                if (r, c) in self.empty_cells and (
                    r == row or c == col or self.cell_to_box[(r, c)] == box_idx
                ):
                    self.update_possibilities(r, c)
    
    def solve(self):
        # Main solving function using backtracking with MRV heuristic
        cell = self.find_mrv_cell()
        
        if cell is None:
            return True  # Puzzle is solved
        
        row, col = cell
        
        # Try values from the pre-calculated possibilities
        for value in sorted(self.possibilities.get((row, col), [])):
            self.place_value(row, col, value)
            
            if self.solve():
                return True
            
            # Backtrack if this choice doesn't lead to a solution
            self.remove_value(row, col, value)
        
        return False
    
    def get_solution(self):
        # Return the solved board
        return self.board


def solve_optimized(board):
    # Wrapper function to solve a board using the optimized solver
    solver = OptimizedSudokuSolver()
    solver.initialize(board)
    
    # Measure solving time
    start_time = time.time()
    result = solver.solve()
    end_time = time.time()
    
    # Copy solution back to the original board
    if result:
        solution = solver.get_solution()
        for i in range(9):
            for j in range(9):
                board[i][j] = solution[i][j]
    
    print(f"Solved in {end_time - start_time:.4f} seconds")
    return result


if __name__ == "__main__":
    from sudoku_solver import print_board
    
    # Example board for testing
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
    
    solve_optimized(board)
    
    print("\nSolution:")
    print_board(board) 