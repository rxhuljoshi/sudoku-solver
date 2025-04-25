from collections import defaultdict
import time

class OptimizedSudokuSolver:
    def __init__(self):
        self.possibilities = {}
        self.row_used = defaultdict(set)
        self.col_used = defaultdict(set)
        self.box_used = defaultdict(set)
        self.cell_to_box = {}
        self.board = None
        self.empty_cells = set()
    
    def initialize(self, board):
        self.board = [row[:] for row in board]
        
        for row in range(9):
            for col in range(9):
                box_idx = (row // 3) * 3 + (col // 3)
                self.cell_to_box[(row, col)] = box_idx
        
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
        
        for row, col in self.empty_cells:
            self.update_possibilities(row, col)
    
    def update_possibilities(self, row, col):
        if (row, col) not in self.empty_cells:
            return set()
            
        box_idx = self.cell_to_box[(row, col)]
        
        possible = set(str(d) for d in range(1, 10))
        
        possible -= self.row_used[row]
        possible -= self.col_used[col]
        possible -= self.box_used[box_idx]
        
        self.possibilities[(row, col)] = possible
        return possible
    
    def find_mrv_cell(self):
        if not self.empty_cells:
            return None
            
        return min(
            self.empty_cells, 
            key=lambda cell: len(self.possibilities.get(cell, set())) or float('inf')
        )
    
    def place_value(self, row, col, value):
        self.board[row][col] = value
        self.empty_cells.remove((row, col))
        self.possibilities.pop((row, col), None)
        
        box_idx = self.cell_to_box[(row, col)]
        self.row_used[row].add(value)
        self.col_used[col].add(value)
        self.box_used[box_idx].add(value)
        
        affected_cells = set()
        
        for c in range(9):
            if c != col and (row, c) in self.empty_cells:
                affected_cells.add((row, c))
        
        for r in range(9):
            if r != row and (r, col) in self.empty_cells:
                affected_cells.add((r, col))
        
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if (r != row or c != col) and (r, c) in self.empty_cells:
                    affected_cells.add((r, c))
        
        for r, c in affected_cells:
            self.update_possibilities(r, c)
    
    def remove_value(self, row, col, value):
        self.board[row][col] = "."
        self.empty_cells.add((row, col))
        
        box_idx = self.cell_to_box[(row, col)]
        self.row_used[row].remove(value)
        self.col_used[col].remove(value)
        self.box_used[box_idx].remove(value)
        
        self.update_possibilities(row, col)
        
        for r in range(9):
            for c in range(9):
                if (r, c) in self.empty_cells and (
                    r == row or c == col or self.cell_to_box[(r, c)] == box_idx
                ):
                    self.update_possibilities(r, c)
    
    def solve(self):
        cell = self.find_mrv_cell()
        
        if cell is None:
            return True
        
        row, col = cell
        
        for value in sorted(self.possibilities.get((row, col), [])):
            self.place_value(row, col, value)
            
            if self.solve():
                return True
            
            self.remove_value(row, col, value)
        
        return False
    
    def get_solution(self):
        return self.board


def solve_optimized(board):
    solver = OptimizedSudokuSolver()
    solver.initialize(board)
    
    start_time = time.time()
    result = solver.solve()
    end_time = time.time()
    
    if result:
        solution = solver.get_solution()
        for i in range(9):
            for j in range(9):
                board[i][j] = solution[i][j]
    
    print(f"Solved in {end_time - start_time:.4f} seconds")
    return result


if __name__ == "__main__":
    from sudoku_solver import print_board
    
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